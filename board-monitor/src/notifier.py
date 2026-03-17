"""
알림 모듈
Pushover를 통한 알림 전송
"""
from typing import Optional
from pushover import Pushover
from src.logger import Logger


class NotificationManager:
    """알림 관리 클래스"""
    
    def __init__(self, user_key: str, api_token: str):
        """
        알림 관리자 초기화
        
        Args:
            user_key: Pushover 사용자 키
            api_token: Pushover API 토큰
        """
        self.logger = Logger.get_logger()
        self.user_key = user_key
        
        try:
            self.client = Pushover(token=api_token, user=user_key)
            self.logger.info("Pushover 클라이언트 초기화 완료")
        except Exception as e:
            self.logger.error(f"Pushover 클라이언트 초기화 실패: {e}")
            raise
    
    def send(
        self,
        post_id: str,
        title: str,
        link: str,
        keyword: Optional[str] = None
    ) -> bool:
        """
        Pushover를 통해 알림 전송
        
        Args:
            post_id: 게시글 ID
            title: 게시글 제목
            link: 게시글 링크
            keyword: 매칭된 키워드 (선택사항)
            
        Returns:
            전송 성공 여부
        """
        try:
            notification_title = f"새 글 발견! [#{post_id}]"
            message = f"{title}\n\n매칭 키워드: {keyword}\n\n{link}" if keyword else f"{title}\n\n{link}"
            
            # Pushover의 notify 메서드 사용
            # notify(message, title=None, priority=0, sound=None, url=None, url_title=None, device=None)
            self.client.notify(
                message=message,
                title=notification_title,
                url=link,
                url_title="게시글 보기"
            )
            self.logger.info(f"알림 전송 완료: [{post_id}] {title}")
            return True
        except Exception as e:
            self.logger.error(f"Pushover 알림 전송 실패 [{post_id}]: {e}")
            return False
