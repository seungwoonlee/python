"""
스크래퍼 모듈
웹 페이지 수집 및 관리
"""
import requests
from typing import Optional
from src.logger import Logger


class Scraper:
    """웹 스크래퍼 클래스"""
    
    def __init__(self, timeout: int = 10, user_agent: Optional[str] = None):
        """
        스크래퍼 초기화
        
        Args:
            timeout: 요청 타임아웃 (초)
            user_agent: User-Agent 헤더값
        """
        self.timeout = timeout
        self.user_agent = user_agent or (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36'
        )
        self.logger = Logger.get_logger()
    
    def fetch(self, url: str) -> Optional[str]:
        """
        웹 페이지 내용 수집
        
        Args:
            url: 대상 URL
            
        Returns:
            HTML 문자열 또는 None (실패 시)
        """
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            self.logger.debug(f"웹 페이지 수집 성공: {url}")
            return response.text
        except requests.exceptions.Timeout:
            self.logger.error(f"요청 타임아웃: {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"연결 오류: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP 오류: {e}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"요청 오류: {e}")
            return None
