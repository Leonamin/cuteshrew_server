import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "cuteshrew", level: str = "INFO") -> logging.Logger:
    """
    로거 설정
    
    Args:
        name: 로거 이름
        level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        설정된 로거
    """
    # 로그 레벨 설정
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(log_levels.get(level.upper(), logging.INFO))
    
    # 이미 핸들러가 있으면 제거 (중복 방지)
    if logger.handlers:
        logger.handlers.clear()
    
    # 포맷터 설정
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러 (logs 디렉토리에 저장)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{name}_{today}.log"
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# 전역 로거 인스턴스
logger = setup_logger("cuteshrew", "DEBUG")


def get_logger(name: str = None) -> logging.Logger:
    """
    로거 인스턴스 반환
    
    Args:
        name: 로거 이름 (None이면 기본 로거 반환)
    
    Returns:
        로거 인스턴스
    """
    if name:
        return setup_logger(name, "DEBUG")
    return logger 