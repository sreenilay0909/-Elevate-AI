"""Base platform service with common functionality"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class BasePlatformService(ABC):
    """Base class for all platform services"""
    
    def __init__(self):
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Return the platform name"""
        pass
    
    @abstractmethod
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """
        Fetch data for a user from the platform
        
        Returns:
            dict: Platform-specific data
        Raises:
            ValueError: If username is invalid or not found
            Exception: For other errors
        """
        pass
    
    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        if not username or not isinstance(username, str):
            return False
        if len(username) < 1 or len(username) > 100:
            return False
        return True
    
    def safe_get(self, url: str, headers: Optional[Dict] = None, timeout: int = 10) -> requests.Response:
        """
        Make a safe GET request with error handling
        
        Args:
            url: URL to fetch
            headers: Optional headers
            timeout: Request timeout in seconds
            
        Returns:
            Response object
            
        Raises:
            ValueError: If request fails
        """
        # Default headers to mimic a real browser
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        # Merge with provided headers
        if headers:
            default_headers.update(headers)
        
        try:
            response = self.session.get(url, headers=default_headers, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"User not found on {self.get_platform_name()}")
            elif e.response.status_code == 429:
                raise ValueError(f"Rate limit exceeded for {self.get_platform_name()}")
            elif e.response.status_code == 403:
                raise ValueError(f"Access forbidden - {self.get_platform_name()} may be blocking automated requests")
            else:
                raise ValueError(f"HTTP error: {e}")
        except requests.exceptions.Timeout:
            raise ValueError(f"Request timeout for {self.get_platform_name()}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request failed: {e}")
    
    def extract_number(self, text: str) -> int:
        """Extract number from text, handling K/M suffixes"""
        if not text:
            return 0
        
        text = text.strip().replace(',', '')
        
        try:
            if 'K' in text.upper():
                return int(float(text.upper().replace('K', '')) * 1000)
            elif 'M' in text.upper():
                return int(float(text.upper().replace('M', '')) * 1000000)
            else:
                return int(float(text))
        except (ValueError, AttributeError):
            return 0
