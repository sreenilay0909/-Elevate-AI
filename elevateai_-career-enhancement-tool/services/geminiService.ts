
import { apiClient } from './apiClient';
import { ProfileData, AnalysisResult } from '../types';

export const analyzeProfile = async (
  data: ProfileData, 
  resumeFile?: File | null
): Promise<AnalysisResult> => {
  try {
    let result;
    
    // If resume file is provided, use the file upload endpoint
    if (resumeFile) {
      result = await apiClient.analyzeWithResume(
        data.github || null,
        data.leetcode || null,
        data.linkedin || null,
        data.targetRole || 'Software Engineer',
        resumeFile
      );
    } else {
      // Otherwise use the regular endpoint
      result = await apiClient.analyzeComplete({
        github_username: data.github,
        leetcode_username: data.leetcode,
        linkedin_url: data.linkedin,
        resume_text: data.resumeText,
        target_role: data.targetRole || 'Software Engineer',
      });
    }

    return result as AnalysisResult;
  } catch (error: any) {
    console.error('Analysis failed:', error);
    throw new Error(error.message || 'Profile analysis failed. Please check your inputs and try again.');
  }
};

// Keep fetchRelevantJobs for backward compatibility (will be moved to backend later)
export const fetchRelevantJobs = async (targetRole: string, skills: string[]) => {
  // This will be handled by backend in future
  return [];
};
