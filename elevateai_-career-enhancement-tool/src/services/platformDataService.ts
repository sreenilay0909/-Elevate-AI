import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/v1';

export interface PlatformData {
  platform: string;
  data: Record<string, any>;
  lastUpdated?: string;
  fetchStatus: string;
  errorMessage?: string;
}

export interface FetchResponse {
  platform: string;
  status: string;
  data?: Record<string, any>;
  error?: string;
  lastUpdated?: string;
}

export interface FetchAllResponse {
  results: FetchResponse[];
  total: number;
  successful: number;
  failed: number;
}

class PlatformDataService {
  private getAuthHeader() {
    const token = localStorage.getItem('auth_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async fetchPlatformData(platform: string): Promise<FetchResponse> {
    const response = await axios.post(
      `${API_URL}/platforms/fetch/${platform}`,
      {},
      { headers: this.getAuthHeader() }
    );
    return response.data;
  }

  async fetchAllPlatforms(): Promise<FetchAllResponse> {
    const response = await axios.post(
      `${API_URL}/platforms/fetch-all`,
      {},
      { headers: this.getAuthHeader() }
    );
    return response.data;
  }

  async getPlatformData(platform: string): Promise<PlatformData> {
    const response = await axios.get(
      `${API_URL}/platforms/data/${platform}`,
      { headers: this.getAuthHeader() }
    );
    return response.data;
  }

  async getAllPlatformData(): Promise<PlatformData[]> {
    const response = await axios.get(
      `${API_URL}/platforms/data`,
      { headers: this.getAuthHeader() }
    );
    return response.data;
  }
}

export default new PlatformDataService();
