"""
로거 모듈
구조화된 로깅 설정
"""
import logging
from typing import Optional


class Logger:
    """로깅 관리 클래스"""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def setup(cls, level: str = 'INFO', log_file: Optional[str] = None) -> logging.Logger:
        """
        로거 설정
        
        Args:
            level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: 로그 파일 경로 (선택사항)
            
        Returns:
            설정된 logger 객체
        """
        if cls._logger is not None:
            return cls._logger
        
        cls._logger = logging.getLogger('BoardMonitor')
        cls._logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)
        
        # 파일 핸들러 (선택사항)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            file_handler.setFormatter(formatter)
            cls._logger.addHandler(file_handler)
        
        return cls._logger
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """로거 객체 조회"""
        if cls._logger is None:
            cls.setup()
        return cls._logger
