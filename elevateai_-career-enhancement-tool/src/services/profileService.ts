import axios from 'axios';

const API_URL = `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/api/v1`;

export interface ProfileData {
  id: number;
  userId: number;
  username: string;
  name: string;
  email: string;
  githubUsername?: string;
  leetcodeUsername?: string;
  geeksforgeeksUsername?: string;
  codechefUsername?: string;
  hackerrankUsername?: string;
  devpostUsername?: string;
  devtoUsername?: string;
  linkedinUrl?: string;
  resumeUrl?: string;
  portfolioUrl?: string;
  
  // Personal Information
  fullName?: string;
  gender?: string;
  profilePictureUrl?: string;
  contactNumber?: string;
  bio?: string;
  
  // Education
  collegeName?: string;
  degree?: string;
  fieldOfStudy?: string;
  currentYear?: string;
  graduationYear?: number;
  
  // Skills
  skills?: string;
  
  createdAt: string;
  updatedAt?: string;
}

export interface PublicProfileData {
  username: string;
  name: string;
  email: string;
  githubUsername?: string;
  leetcodeUsername?: string;
  geeksforgeeksUsername?: string;
  codechefUsername?: string;
  hackerrankUsername?: string;
  devpostUsername?: string;
  devtoUsername?: string;
  linkedinUrl?: string;
  portfolioUrl?: string;
  resumeUrl?: string;
  
  // Personal Information
  fullName?: string;
  gender?: string;
  profilePictureUrl?: string;
  contactNumber?: string;
  bio?: string;
  
  // Education
  collegeName?: string;
  degree?: string;
  fieldOfStudy?: string;
  currentYear?: string;
  graduationYear?: number;
  
  // Skills
  skills?: string;
  
  createdAt: string;
}

export interface ProfileUpdateData {
  githubUsername?: string;
  leetcodeUsername?: string;
  geeksforgeeksUsername?: string;
  codechefUsername?: string;
  hackerrankUsername?: string;
  devpostUsername?: string;
  devtoUsername?: string;
  linkedinUrl?: string;
  resumeUrl?: string;
  portfolioUrl?: string;
  
  // Personal Information
  fullName?: string;
  gender?: string;
  profilePictureUrl?: string;
  contactNumber?: string;
  bio?: string;
  
  // Education
  collegeName?: string;
  degree?: string;
  fieldOfStudy?: string;
  currentYear?: string;
  graduationYear?: number;
  
  // Skills
  skills?: string;
}

class ProfileService {
  private getAuthHeader() {
    const token = localStorage.getItem('auth_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async getMyProfile(): Promise<ProfileData> {
    const response = await axios.get(`${API_URL}/profiles/me`, {
      headers: this.getAuthHeader(),
    });
    return response.data;
  }

  async updateMyProfile(data: ProfileUpdateData): Promise<ProfileData> {
    const response = await axios.put(`${API_URL}/profiles/me`, data, {
      headers: this.getAuthHeader(),
    });
    return response.data;
  }

  async getPublicProfile(username: string): Promise<PublicProfileData> {
    const response = await axios.get(`${API_URL}/profiles/${username}`);
    return response.data;
  }

  async searchUsers(query: string): Promise<Array<{
    username: string;
    name: string;
    fullName?: string;
    bio?: string;
    collegeName?: string;
  }>> {
    if (!query || query.length < 2) return [];
    const response = await axios.get(`${API_URL}/profiles/search/users`, {
      params: { q: query }
    });
    return response.data;
  }
}

export default new ProfileService();
