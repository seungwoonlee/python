"""
메인 애플리케이션
게시판 모니터링 및 알림 워크플로우
"""
import time
import signal
import sys
from typing import Optional
from src.config import ConfigManager
from src.logger import Logger
from src.scraper import Scraper
from src.parser import Parser
from src.filter import Filter
from src.notifier import NotificationManager


class BoardMonitor:
    """게시판 모니터링 메인 클래스"""
    
    def __init__(self, config_path: str = 'config.ini'):
        """
        보드 모니터 초기화
        
        Args:
            config_path: 설정 파일 경로
        """
        self.config_manager = ConfigManager(config_path)
        self.scraper: Optional[Scraper] = None
        self.parser: Optional[Parser] = None
        self.filter: Optional[Filter] = None
        self.notifier: Optional[NotificationManager] = None
        self.logger: Optional[Logger] = None
        self.running = True
    
    def setup(self) -> bool:
        """
        애플리케이션 초기화
        
        Returns:
            초기화 성공 여부
        """
        try:
            # 로거 설정
            log_level = self.config_manager.get('APP', 'LOG_LEVEL', 'INFO')
            self.logger = Logger.setup(level=log_level, log_file='board_monitor.log')
            self.logger = Logger.get_logger()
            
            self.logger.info("="*60)
            self.logger.info("게시판 모니터 시작")
            self.logger.info("="*60)
            
            # 필수 설정 검증
            self.config_manager.validate()
            self.logger.info("설정 검증 완료")
            
            # 각 컴포넌트 초기화
            timeout = self.config_manager.get_int('APP', 'REQUEST_TIMEOUT', 10)
            self.scraper = Scraper(timeout=timeout)
            self.parser = Parser()
            
            # 키워드 필터 설정
            keywords_str = self.config_manager.get('FILTER', 'KEYWORDS')
            keywords = [k.strip() for k in keywords_str.split(',')]
            max_tracked = self.config_manager.get_int('APP', 'MAX_TRACKED_IDS', 500)
            self.filter = Filter(keywords=keywords, max_tracked_ids=max_tracked)
            self.logger.info(f"감시 키워드: {keywords}")
            
            # Pushover 알림 설정
            user_key = self.config_manager.get('PUSHOVER', 'USER_KEY')
            api_token = self.config_manager.get('PUSHOVER', 'API_TOKEN')
            self.notifier = NotificationManager(user_key, api_token)
            
            # 시그널 핸들러 등록
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            self.logger.info("애플리케이션 초기화 완료")
            return True
        
        except Exception as e:
            print(f"초기화 실패: {e}", file=sys.stderr)
            return False
    
    def run(self) -> None:
        """메인 모니터링 루프"""
        if not self.setup():
            sys.exit(1)
        
        target_url = self.config_manager.get('TARGET', 'URL')
        post_selector = self.config_manager.get('TARGET', 'POST_SELECTOR')
        title_selector = self.config_manager.get('TARGET', 'TITLE_SELECTOR')
        link_selector = self.config_manager.get('TARGET', 'LINK_SELECTOR')
        id_selector = self.config_manager.get('TARGET', 'ID_SELECTOR')
        check_interval = self.config_manager.get_int('APP', 'CHECK_INTERVAL_SECONDS', 60)
        
        self.logger.info(f"감시 대상 URL: {target_url}")
        self.logger.info(f"체크 간격: {check_interval}초")
        self.logger.info("모니터링 시작...")
        
        try:
            while self.running:
                try:
                    self._monitor_once(
                        target_url,
                        post_selector,
                        title_selector,
                        link_selector,
                        id_selector
                    )
                    time.sleep(check_interval)
                except Exception as e:
                    self.logger.error(f"모니터링 사이클 중 오류: {e}", exc_info=True)
                    time.sleep(check_interval)
        except KeyboardInterrupt:
            self.logger.info("사용자에 의해 중단되었습니다.")
        finally:
            self._cleanup()
    
    def _monitor_once(
        self,
        target_url: str,
        post_selector: str,
        title_selector: str,
        link_selector: str,
        id_selector: str
    ) -> None:
        """
        한 번의 모니터링 사이클 실행
        
        Args:
            target_url: 감시할 URL
            post_selector: 게시글 CSS Selector
            title_selector: 제목 CSS Selector
            link_selector: 링크 CSS Selector
            id_selector: ID CSS Selector
        """
        # 웹 페이지 수집
        html_content = self.scraper.fetch(target_url)
        if not html_content:
            self.logger.warning("웹 페이지를 가져오지 못했습니다. 다음 주기에 재시도합니다.")
            return
        
        # 게시글 파싱
        posts = self.parser.parse_posts(
            html_content,
            post_selector,
            title_selector,
            link_selector,
            id_selector
        )
        
        if not posts:
            self.logger.warning("파싱된 게시글이 없습니다.")
            return
        
        # 첫 실행 시 초기화
        if self.filter.is_first_run:
            post_ids = [post.id for post in posts]
            self.filter.initialize_with_ids(post_ids)
            return
        
        # 새 게시글 확인 및 알림 (오래된 글부터 확인)
        new_post_count = 0
        for post in reversed(posts):
            if not self.filter.is_already_notified(post.id):
                # 키워드 매칭 확인
                matched_keyword = None
                for keyword in self.filter.keywords:
                    if keyword.lower() in post.title.lower():
                        matched_keyword = keyword
                        break
                
                if matched_keyword:
                    self.logger.info(
                        f"새 글 발견! [ID: {post.id}] {post.title} "
                        f"(키워드: {matched_keyword})"
                    )
                    self.notifier.send(post.id, post.title, post.link, matched_keyword)
                    new_post_count += 1
                
                # 확인한 글 추가
                self.filter.add_notified_id(post.id)
        
        if new_post_count > 0:
            self.logger.info(f"이번 주기에 {new_post_count}개의 새 글을 발견했습니다.")
        else:
            self.logger.debug("새 글이 없습니다.")
    
    def _signal_handler(self, signum, frame) -> None:
        """
        시그널 핸들러 (Ctrl+C, SIGTERM 처리)
        
        Args:
            signum: 신호 번호
            frame: 프레임 객체
        """
        self.logger.info(f"신호 {signum} 수신. 애플리케이션을 종료합니다...")
        self.running = False
    
    def _cleanup(self) -> None:
        """리소스 정리"""
        self.logger.info("="*60)
        self.logger.info("게시판 모니터 종료")
        self.logger.info("="*60)


def main() -> None:
    """메인 엔트리 포인트"""
    monitor = BoardMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
