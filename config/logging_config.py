import os
import logging


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # cyan
        'INFO': '\033[32m',      # green
        'WARNING': '\033[33m',   # yellow
        'ERROR': '\033[31m',     # red
        'CRITICAL': '\033[35m',  # magenta
    }
    RESET = '\033[0m'
    
    # Spacing after each log level to align with uvicorn
    SPACING = {
        'DEBUG': '    ',     # DEBUG:    (5 chars + 3 spaces = 8)
        'INFO': '     ',     # INFO:     (4 chars + 4 spaces = 8) 
        'WARNING': '  ',     # WARNING:  (7 chars + 1 space = 8)
        'ERROR': '    ',     # ERROR:    (5 chars + 3 spaces = 8)
        'CRITICAL': ' ',     # CRITICAL: (8 chars + 0 spaces = 8)
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        spacing = self.SPACING.get(record.levelname, '    ')
        colored_level = f"{log_color}{record.levelname}{self.RESET}:{spacing}"
        
        # Replace the levelname in the record
        original_levelname = record.levelname
        record.levelname = colored_level
        result = super().format(record)
        record.levelname = original_levelname  # Restore original
        return result


def setup_logging():
    """Configure logging with colors and uvicorn-style format"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter("%(levelname)s%(name)s: %(message)s"))

    logging.basicConfig(
        level=getattr(logging, log_level),
        handlers=[handler]
    )