/**
 * AI Analysis Service
 * Handles AI-powered analysis and chatbot functionality
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

interface ChatMessage {
  role: string;
  content: string;
}

interface AnalysisResponse {
  platform: string;
  username: string;
  percentileRank: number;
  globalRanking: string;
  overallScore: number;
  strengths: Array<{
    topic: string;
    score: number;
    description: string;
  }>;
  weaknesses: Array<{
    topic: string;
    score: number;
    description: string;
  }>;
  recommendations: string[];
  weeklyPlan: {
    day1: string;
    day2: string;
    day3: string;
    day4: string;
    day5: string;
    day6: string;
    day7: string;
  };
  keyMetrics: Array<{
    name: string;
    value: string;
    benchmark: string;
    status: 'good' | 'average' | 'needs_improvement';
  }>;
  topicBreakdown?: Array<{
    topic: string;
    solved: number;
    total: number;
    proficiency: number;
  }>;
  analyzedAt: string;
}

interface ChatResponse {
  answer: string;
  platform: string;
}

/**
 * Get AI analysis for a platform
 */
export const getAnalysis = async (platform: string): Promise<AnalysisResponse> => {
  const token = localStorage.getItem('auth_token');
  
  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${API_BASE_URL}/ai/analyze/${platform}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get analysis');
  }

  return response.json();
};

/**
 * Chat with platform-specific AI assistant
 */
export const chatWithPlatform = async (
  platform: string,
  question: string,
  chatHistory?: ChatMessage[]
): Promise<ChatResponse> => {
  const token = localStorage.getItem('auth_token');
  
  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${API_BASE_URL}/ai/chat/${platform}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question,
      chatHistory: chatHistory || [],
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get chat response');
  }

  return response.json();
};

export type { AnalysisResponse, ChatMessage, ChatResponse };
