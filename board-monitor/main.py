"""
Board Monitor - 게시판 모니터링 애플리케이션
DC인사이드 게시판을 감시하여 특정 키워드가 포함된 새 글에 대해 Pushover 알림을 전송합니다.

사용 방법:
    python main.py

설정:
    config.ini 파일을 수정하여 감시할 게시판 URL, 키워드, Pushover 인증정보 등을 설정하세요.
"""
from src.monitor import BoardMonitor
import os

CONFIG_FILE = os.getenv('BOARD_MONITOR_CONFIG', 'config.ini')

def main() -> None:
    """메인 엔트리 포인트"""
    # 설정 파일 경로를 명시적으로 전달하여 유연성 확보
    monitor = BoardMonitor(config_path=CONFIG_FILE)
    monitor.run()


if __name__ == "__main__":
    main()
