
export interface ProfileData {
  github?: string;
  leetcode?: string;
  linkedin?: string;
  naukri?: string;
  resumeText?: string;
  targetRole?: string;
}

export interface PlatformScore {
  name: string;
  score: number;
  total: number;
  metrics: { name: string; value: number }[];
  highlights: string[];
}

export interface Recommendation {
  title: string;
  description: string;
  priority: 'High' | 'Medium' | 'Low';
  category: 'Skill' | 'Project' | 'Certification' | 'Networking';
}

export interface LearningRoadmap {
  phase: string;
  tasks: string[];
  resources: { name: string; url: string }[];
}

export interface JobListing {
  title: string;
  company: string;
  location: string;
  salary?: string;
  url: string;
  matchScore: number;
  source: string;
}

export interface AnalysisResult {
  compositeScore: number;
  platformScores: PlatformScore[];
  marketAnalysis: {
    demandScore: number;
    trendingSkills: string[];
    salaryEstimate: string;
    topCompanies: string[];
  };
  recommendations: Recommendation[];
  roadmap: LearningRoadmap[];
  jobMatch: {
    role: string;
    fitPercent: number;
    gaps: string[];
  };
  jobListings?: JobListing[];
}
