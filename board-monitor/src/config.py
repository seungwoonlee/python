"""
설정 관리 모듈
config.ini 파일 로드 및 검증
"""
import configparser
import os
from typing import Optional


class ConfigManager:
    """설정 파일 관리 클래스"""
    
    DEFAULT_CONFIG = {
        'TARGET': {
            'URL': 'https://gall.dcinside.com/board/lists/?id=pridepc_new4',
            'POST_SELECTOR': '.ub-content.us-post',
            'TITLE_SELECTOR': '.gall_tit a',
            'LINK_SELECTOR': '.gall_tit a',
            'ID_SELECTOR': '.gall_num',
        },
        'FILTER': {
            'KEYWORDS': '4070, 4080, 4090, 특가',
        },
        'PUSHOVER': {
            'USER_KEY': '',
            'API_TOKEN': '',
        },
        'APP': {
            'CHECK_INTERVAL_SECONDS': '60',
            'MAX_TRACKED_IDS': '500',
            'REQUEST_TIMEOUT': '10',
            'LOG_LEVEL': 'INFO',
        }
    }
    
    def __init__(self, config_path: str = 'config.ini'):
        """
        설정 관리자 초기화
        
        Args:
            config_path: config.ini 파일 경로
        """
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self) -> None:
        """config.ini 파일 로드 또는 기본값 사용"""
        if os.path.exists(self.config_path):
            try:
                self.config.read(self.config_path, encoding='utf-8')
            except Exception as e:
                raise RuntimeError(f"설정 파일 읽기 실패: {e}")
        else:
            # 기본값으로 config 초기화
            self._init_default_config()
    
    def _init_default_config(self) -> None:
        """기본 설정값으로 config 초기화"""
        for section, values in self.DEFAULT_CONFIG.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in values.items():
                self.config.set(section, key, value)
    
    def get(self, section: str, key: str, default: Optional[str] = None) -> str:
        """
        설정값 조회 (환경변수 우선)
        
        Args:
            section: 섹션 이름
            key: 키 이름
            default: 기본값
            
        Returns:
            설정값
        """
        # 환경변수 확인 (예: BOARD_MONITOR_PUSHOVER_USER_KEY)
        env_var = f"BOARD_MONITOR_{section}_{key}".upper()
        env_value = os.getenv(env_var)
        if env_value:
            return env_value
        
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if default is not None:
                return default
            raise ValueError(f"설정을 찾을 수 없음: [{section}] {key}")
    
    def get_int(self, section: str, key: str, default: Optional[int] = None) -> int:
        """
        정수 설정값 조회
        
        Args:
            section: 섹션 이름
            key: 키 이름
            default: 기본값
            
        Returns:
            정수 설정값
        """
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            if default is not None:
                return default
            raise ValueError(f"정수 설정을 찾을 수 없음: [{section}] {key}")
    
    def validate(self) -> None:
        """필수 설정값 검증"""
        required_settings = [
            ('TARGET', 'URL'),
            ('TARGET', 'POST_SELECTOR'),
            ('FILTER', 'KEYWORDS'),
            ('PUSHOVER', 'USER_KEY'),
            ('PUSHOVER', 'API_TOKEN'),
        ]
        
        for section, key in required_settings:
            # 먼저 환경변수 확인
            env_var = f"BOARD_MONITOR_{section}_{key}".upper()
            env_value = os.getenv(env_var)
            
            if env_value:
                continue  # 환경변수가 있으면 통과
            
            # 설정 파일에서 확인
            value = self.get(section, key, default=None)
            if not value or (section == 'PUSHOVER' and value.startswith('여기에')):
                raise ValueError(
                    f"필수 설정이 없습니다: [{section}] {key}\n"
                    f"설정 방법:\n"
                    f"  1. config.ini에 값 입력\n"
                    f"  2. 또는 환경변수 설정: {env_var}=값"
                )
    
    def save_default_config(self) -> None:
        """기본 설정을 config.ini 파일로 저장"""
        self._init_default_config()
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            raise RuntimeError(f"설정 파일 저장 실패: {e}")
