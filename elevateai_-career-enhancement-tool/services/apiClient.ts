// API Client for Backend Integration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ProfileRequest {
  github_username?: string;
  leetcode_username?: string;
  linkedin_url?: string;
  resume_text?: string;
  target_role?: string;
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error: any) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Analysis endpoints
  async analyzeGitHub(username: string) {
    return this.request(`/api/v1/analyze/github/${username}`);
  }

  async analyzeLeetCode(username: string) {
    return this.request(`/api/v1/analyze/leetcode/${username}`);
  }

  async analyzeComplete(data: ProfileRequest) {
    return this.request('/api/v1/analyze/complete', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async analyzeWithResume(
    githubUsername: string | null,
    leetcodeUsername: string | null,
    linkedinUrl: string | null,
    targetRole: string,
    resumeFile: File
  ) {
    const formData = new FormData();
    
    if (githubUsername) formData.append('github_username', githubUsername);
    if (leetcodeUsername) formData.append('leetcode_username', leetcodeUsername);
    if (linkedinUrl) formData.append('linkedin_url', linkedinUrl);
    formData.append('target_role', targetRole);
    formData.append('resume_file', resumeFile);

    const url = `${this.baseURL}/api/v1/analyze/complete-with-resume`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header - browser will set it with boundary
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error: any) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async analyzeResumeOnly(resumeFile: File) {
    const formData = new FormData();
    formData.append('resume_file', resumeFile);

    const url = `${this.baseURL}/api/v1/analyze/resume-only`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error: any) {
      console.error('API Error:', error);
      throw error;
    }
  }
}

export const apiClient = new APIClient(API_BASE_URL);
export type { ProfileRequest };
