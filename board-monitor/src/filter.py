"""
필터 모듈
키워드 필터링 및 중복 관리
"""
from typing import List, Set
from src.logger import Logger


class Filter:
    """필터 관리 클래스"""
    
    def __init__(self, keywords: List[str], max_tracked_ids: int = 500):
        """
        필터 초기화
        
        Args:
            keywords: 감시할 키워드 목록
            max_tracked_ids: 추적할 최대 게시글 ID 개수
        """
        self.keywords = [kw.strip().lower() for kw in keywords if kw.strip()]
        self.max_tracked_ids = max_tracked_ids
        self.notified_post_ids: Set[str] = set()
        self.logger = Logger.get_logger()
        self.is_first_run = True
    
    def is_keyword_match(self, text: str) -> bool:
        """
        텍스트에 키워드가 포함되어 있는지 확인
        
        Args:
            text: 검사할 텍스트
            
        Returns:
            매칭 여부
        """
        text_lower = text.lower()
        for keyword in self.keywords:
            if keyword in text_lower:
                return True
        return False
    
    def add_notified_id(self, post_id: str) -> None:
        """
        이미 알림을 보낸 게시글 ID 추가
        
        Args:
            post_id: 게시글 ID
        """
        self.notified_post_ids.add(post_id)
        self._cleanup_old_ids()
    
    def is_already_notified(self, post_id: str) -> bool:
        """
        이미 알림을 보냈는지 확인
        
        Args:
            post_id: 게시글 ID
            
        Returns:
            알림 여부
        """
        return post_id in self.notified_post_ids
    
    def initialize_with_ids(self, post_ids: List[str]) -> None:
        """
        초기 게시글 ID 목록으로 초기화 (첫 실행 시)
        
        Args:
            post_ids: 게시글 ID 목록
        """
        self.notified_post_ids = set(post_ids)
        self.is_first_run = False
        self.logger.info(f"필터 초기화 완료. {len(self.notified_post_ids)}개의 게시글을 기준으로 감시를 시작합니다.")
    
    def _cleanup_old_ids(self) -> None:
        """오래된 ID 정리 (메모리 절약)"""
        if len(self.notified_post_ids) > self.max_tracked_ids:
            try:
                # 숫자 ID인 경우만 정렬
                sorted_ids = sorted(
                    [pid for pid in self.notified_post_ids if pid.isdigit()],
                    key=int,
                    reverse=True
                )
                # 새로운 ID 500개만 유지
                self.notified_post_ids = set(sorted_ids[:self.max_tracked_ids])
                self.logger.debug(
                    f"추적 ID 정리 완료. 현재 {len(self.notified_post_ids)}개의 ID를 추적하고 있습니다."
                )
            except Exception as e:
                self.logger.warning(f"ID 정리 중 오류: {e}")
