"""Simple AI Analysis Test"""
from app.services.ai_analysis_service import AIAnalysisService
from app.db.database import SessionLocal
from app.models.platform_data import PlatformData
from app.models.user import User
import json

# Get database session
db = SessionLocal()

# Get user
user = db.query(User).filter(User.username == 'sreenilay').first()
if not user:
    print("User not found")
    exit(1)

print(f"Testing AI analysis for user: {user.username}")

# Get GitHub platform data
platform_data = db.query(PlatformData).filter(
    PlatformData.user_id == user.id,
    PlatformData.platform_name == 'github'
).first()

if not platform_data:
    print("No GitHub data found")
    exit(1)

print(f"Found GitHub data for username: {platform_data.data.get('username')}")
print(f"Data: {json.dumps(platform_data.data, indent=2)[:200]}...")

# Test AI analysis
print("\nTesting AI analysis...")
try:
    ai_service = AIAnalysisService()
    analysis = ai_service.analyze_platform_data(
        platform='github',
        user_data=platform_data.data,
        username=platform_data.data.get('username', 'unknown')
    )
    
    print("\n✓ AI Analysis successful!")
    print(f"\nAnalysis Summary:")
    print(f"  Platform: {analysis['platform']}")
    print(f"  Username: {analysis['username']}")
    print(f"  Overall Score: {analysis['overallScore']}/100")
    print(f"  Percentile Rank: {analysis['percentileRank']}%")
    print(f"  Global Ranking: {analysis['globalRanking']}")
    print(f"\n  Strengths: {len(analysis['strengths'])} areas")
    for s in analysis['strengths'][:2]:
        print(f"    - {s['topic']}: {s['score']}/100")
    print(f"\n  Weaknesses: {len(analysis['weaknesses'])} areas")
    for w in analysis['weaknesses'][:2]:
        print(f"    - {w['topic']}: {w['score']}/100")
    print(f"\n  Recommendations: {len(analysis['recommendations'])} items")
    for r in analysis['recommendations'][:2]:
        print(f"    - {r[:80]}...")
    
    print("\n✓ Test completed successfully!")
    
except Exception as e:
    import traceback
    print(f"\n✗ Error: {e}")
    print(traceback.format_exc())

db.close()
