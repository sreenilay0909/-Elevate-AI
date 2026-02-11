# Platform Data Integration - Design Document

## Architecture Overview

```
┌─────────────┐
│   Frontend  │
│  Dashboard  │
└──────┬──────┘
       │ HTTP Requests
       ▼
┌─────────────────────────┐
│   Platform Data API     │
│  /api/v1/platforms/*    │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Platform Services      │
│  - GitHub Service       │
│  - LeetCode Service     │
│  - GeeksforGeeks Svc    │
│  - CodeChef Service     │
│  - HackerRank Service   │
│  - DevPost Service      │
│  - Dev.to Service       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  External APIs/Scraping │
│  - GitHub API           │
│  - LeetCode GraphQL     │
│  - Web Scraping (BS4)   │
│  - Dev.to API           │
└─────────────────────────┘
```

---

## Database Design

### platform_data Table
```sql
CREATE TABLE platform_data (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    platform_name VARCHAR(50),  -- 'github', 'leetcode', etc.
    data JSON,                  -- Platform-specific statistics
    last_updated TIMESTAMP,
    fetch_status VARCHAR(20),   -- 'success', 'error', 'pending'
    error_message VARCHAR(500),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(user_id, platform_name)
);
```

### Data JSON Structure Examples

**GitHub:**
```json
{
  "repositories": 42,
  "stars": 156,
  "commits_last_year": 1234,
  "top_languages": ["TypeScript", "Python", "JavaScript"],
  "contribution_streak": 45
}
```

**LeetCode:**
```json
{
  "total_solved": 250,
  "easy_solved": 100,
  "medium_solved": 120,
  "hard_solved": 30,
  "acceptance_rate": 65.5,
  "ranking": 12345,
  "streak": 15
}
```

---

## API Design

### 1. Fetch Single Platform Data
```
POST /api/v1/platforms/fetch/{platform}
Authorization: Bearer <token>

Response:
{
  "platform": "github",
  "status": "success",
  "data": { ... },
  "last_updated": "2024-01-15T10:30:00Z"
}
```

### 2. Fetch All Platforms
```
POST /api/v1/platforms/fetch-all
Authorization: Bearer <token>

Response:
{
  "results": [
    {
      "platform": "github",
      "status": "success",
      "data": { ... }
    },
    {
      "platform": "leetcode",
      "status": "error",
      "error": "Username not found"
    }
  ]
}
```

### 3. Get Platform Data
```
GET /api/v1/platforms/data/{platform}
Authorization: Bearer <token>

Response:
{
  "platform": "github",
  "data": { ... },
  "last_updated": "2024-01-15T10:30:00Z",
  "fetch_status": "success"
}
```

### 4. Get All Platform Data
```
GET /api/v1/platforms/data
Authorization: Bearer <token>

Response:
{
  "platforms": [
    {
      "platform": "github",
      "data": { ... },
      "last_updated": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

## Service Layer Design

### Base Platform Service Interface
```python
class BasePlatformService:
    def fetch_user_data(self, username: str) -> dict:
        """Fetch data for a user from the platform"""
        raise NotImplementedError
    
    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        raise NotImplementedError
    
    def get_platform_name(self) -> str:
        """Return platform name"""
        raise NotImplementedError
```

### Individual Services

#### 1. GitHub Service
- **Method:** GitHub REST API v3
- **Authentication:** Personal Access Token
- **Endpoints:**
  - `/users/{username}` - User info
  - `/users/{username}/repos` - Repositories
  - `/search/commits` - Commit count
- **Rate Limit:** 5000 requests/hour (authenticated)

#### 2. LeetCode Service
- **Method:** GraphQL API (unofficial)
- **Authentication:** None required
- **Endpoint:** `https://leetcode.com/graphql`
- **Query:** User profile and statistics
- **Rate Limit:** Unknown, implement backoff

#### 3. GeeksforGeeks Service
- **Method:** Web Scraping
- **URL:** `https://auth.geeksforgeeks.org/user/{username}`
- **Parser:** BeautifulSoup4
- **Data:** HTML parsing for stats
- **Rate Limit:** Implement delays

#### 4. CodeChef Service
- **Method:** Web Scraping (or API if available)
- **URL:** `https://www.codechef.com/users/{username}`
- **Parser:** BeautifulSoup4
- **Data:** Profile page parsing
- **Rate Limit:** Implement delays

#### 5. HackerRank Service
- **Method:** Web Scraping
- **URL:** `https://www.hackerrank.com/{username}`
- **Parser:** BeautifulSoup4
- **Data:** Profile page parsing
- **Rate Limit:** Implement delays

#### 6. DevPost Service
- **Method:** Web Scraping
- **URL:** `https://devpost.com/{username}`
- **Parser:** BeautifulSoup4
- **Data:** Profile page parsing
- **Rate Limit:** Implement delays

#### 7. Dev.to Service
- **Method:** Official REST API
- **URL:** `https://dev.to/api/users/by_username?url={username}`
- **Authentication:** Optional API key
- **Rate Limit:** 10 requests/second

---

## Frontend Design

### Platform Card Component
```typescript
interface PlatformCardProps {
  platform: string;
  username: string;
  data: PlatformData | null;
  lastUpdated: string | null;
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
}
```

### Platform Data Service
```typescript
class PlatformDataService {
  async fetchPlatformData(platform: string): Promise<PlatformData>
  async fetchAllPlatforms(): Promise<PlatformData[]>
  async getPlatformData(platform: string): Promise<PlatformData>
  async getAllPlatformData(): Promise<PlatformData[]>
}
```

### UI States
1. **Loading** - Spinner with "Fetching data..."
2. **Success** - Display statistics
3. **Error** - Error message with retry button
4. **No Data** - "Click refresh to load data"
5. **Stale** - Warning if data >24 hours old

---

## Error Handling Strategy

### Error Types
1. **Username Not Found** - 404 from platform
2. **Rate Limit Exceeded** - 429 from platform
3. **Network Error** - Connection timeout
4. **Parse Error** - Failed to extract data
5. **Authentication Error** - Invalid API key

### Error Responses
```python
{
  "status": "error",
  "error_type": "username_not_found",
  "message": "Profile not found on GitHub",
  "retry_after": null
}
```

### Retry Logic
- Exponential backoff for rate limits
- Max 3 retries for network errors
- No retry for 404 errors
- User-initiated retry for all errors

---

## Performance Optimization

### Caching Strategy
- Cache platform data for 1 hour
- Invalidate on manual refresh
- Store in database with timestamp

### Concurrent Fetching
- Use asyncio for parallel requests
- Timeout after 10 seconds per platform
- Continue on individual failures

### Rate Limiting
- Implement request delays for scraping
- Respect API rate limits
- Queue requests if needed

---

## Security Considerations

### API Keys
- Store in environment variables
- Never expose in frontend
- Rotate regularly

### Input Validation
- Sanitize usernames
- Prevent injection attacks
- Validate data formats

### Rate Limiting
- Limit refresh frequency (1 per minute per user)
- Prevent abuse with cooldown periods
- Log suspicious activity

---

## Testing Strategy

### Unit Tests
- Test each service independently
- Mock external API calls
- Test error handling

### Integration Tests
- Test API endpoints
- Test database operations
- Test concurrent fetching

### E2E Tests
- Test complete user flow
- Test refresh functionality
- Test error scenarios

---

## Deployment Considerations

### Environment Variables
```
GITHUB_TOKEN=<token>
DEVTO_API_KEY=<key>
```

### Dependencies
```
beautifulsoup4==4.12.3
lxml==5.1.0
requests==2.31.0
aiohttp==3.9.1
```

### Monitoring
- Log all fetch attempts
- Track success/failure rates
- Monitor response times
- Alert on high error rates

---

## Future Enhancements

### Phase 2.5
- Auto-refresh with Celery
- Background job scheduling
- Redis caching

### Phase 2.6
- Historical data tracking
- Progress charts
- Trend analysis

### Phase 2.7
- AI-powered insights
- Personalized recommendations
- Skill gap analysis
