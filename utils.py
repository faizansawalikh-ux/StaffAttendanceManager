"""
Utility functions for Staff Attendance Manager.
Includes logging, validation, and helper functions.
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Any
import json

from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT, BACKUP_DIR, DATABASE_FILE

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class Logger:
    """Centralized logging utility."""

    @staticmethod
    def info(message: str, module: str = "App") -> None:
        """Log info message."""
        logger.info(f"[{module}] {message}")

    @staticmethod
    def warning(message: str, module: str = "App") -> None:
        """Log warning message."""
        logger.warning(f"[{module}] {message}")

    @staticmethod
    def error(message: str, module: str = "App", exception: Optional[Exception] = None) -> None:
        """Log error message with optional exception."""
        if exception:
            logger.error(f"[{module}] {message}", exc_info=True)
        else:
            logger.error(f"[{module}] {message}")

    @staticmethod
    def debug(message: str, module: str = "App") -> None:
        """Log debug message."""
        logger.debug(f"[{module}] {message}")


class Validator:
    """Input validation utilities."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        import re
        phone = phone.replace(" ", "").replace("-", "")
        return bool(re.match(r'^\+?1?\d{9,15}$', phone))

    @staticmethod
    def validate_employee_id(emp_id: str) -> bool:
        """Validate employee ID format."""
        return bool(emp_id and len(emp_id.strip()) > 0)

    @staticmethod
    def validate_date(date_str: str, date_format: str = "%d-%m-%Y") -> bool:
        """Validate date format."""
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input."""
        return text.strip().replace('"', "'") if text else ""


class DateTimeUtil:
    """DateTime utility functions."""

    @staticmethod
    def get_current_date() -> str:
        """Get current date in DD-MM-YYYY format."""
        return datetime.now().strftime("%d-%m-%Y")

    @staticmethod
    def get_current_time() -> str:
        """Get current time in HH:MM:SS format."""
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def get_current_datetime() -> str:
        """Get current date-time in DD-MM-YYYY HH:MM:SS format."""
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    @staticmethod
    def format_date(date: datetime, date_format: str = "%d-%m-%Y") -> str:
        """Format datetime object to string."""
        return date.strftime(date_format)

    @staticmethod
    def parse_date(date_str: str, date_format: str = "%d-%m-%Y") -> Optional[datetime]:
        """Parse date string to datetime object."""
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            return None

    @staticmethod
    def get_month_year() -> str:
        """Get current month and year in MM-YYYY format."""
        return datetime.now().strftime("%m-%Y")

    @staticmethod
    def date_range(start_date: str, end_date: str) -> List[str]:
        """Get list of dates between start and end date."""
        from datetime import timedelta
        start = DateTimeUtil.parse_date(start_date)
        end = DateTimeUtil.parse_date(end_date)

        if not start or not end:
            return []

        dates = []
        current = start
        while current <= end:
            dates.append(DateTimeUtil.format_date(current))
            current += timedelta(days=1)

        return dates


class BackupUtil:
    """Backup and restore utilities."""

    @staticmethod
    def create_backup(source: Path, backup_dir: Path = BACKUP_DIR) -> Optional[Path]:
        """Create backup of database file."""
        try:
            if not source.exists():
                Logger.warning(f"Source file not found: {source}")
                return None

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.xlsx"
            backup_path = backup_dir / backup_name

            shutil.copy2(source, backup_path)
            Logger.info(f"Backup created: {backup_path}", "BackupUtil")
            return backup_path
        except Exception as e:
            Logger.error(f"Failed to create backup", "BackupUtil", exception=e)
            return None

    @staticmethod
    def restore_backup(backup_path: Path, target_path: Path = DATABASE_FILE) -> bool:
        """Restore from backup file."""
        try:
            if not backup_path.exists():
                Logger.error(f"Backup file not found: {backup_path}", "BackupUtil")
                return False

            shutil.copy2(backup_path, target_path)
            Logger.info(f"Restored from backup: {backup_path}", "BackupUtil")
            return True
        except Exception as e:
            Logger.error(f"Failed to restore backup", "BackupUtil", exception=e)
            return False

    @staticmethod
    def get_backups(backup_dir: Path = BACKUP_DIR) -> List[Path]:
        """Get list of all backups sorted by newest first."""
        try:
            backups = sorted(
                backup_dir.glob("backup_*.xlsx"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            return backups
        except Exception as e:
            Logger.error("Failed to get backups", "BackupUtil", exception=e)
            return []

    @staticmethod
    def cleanup_old_backups(backup_dir: Path = BACKUP_DIR, max_backups: int = 10) -> None:
        """Remove old backups keeping only recent ones."""
        try:
            backups = BackupUtil.get_backups(backup_dir)
            if len(backups) > max_backups:
                for old_backup in backups[max_backups:]:
                    old_backup.unlink()
                    Logger.info(f"Deleted old backup: {old_backup.name}", "BackupUtil")
        except Exception as e:
            Logger.error("Failed to cleanup backups", "BackupUtil", exception=e)


class FileUtil:
    """File utility functions."""

    @staticmethod
    def get_file_size_mb(file_path: Path) -> float:
        """Get file size in MB."""
        try:
            return file_path.stat().st_size / (1024 * 1024)
        except Exception:
            return 0.0

    @staticmethod
    def validate_image_file(file_path: Path, max_size_mb: float = 5) -> tuple:
        """Validate image file size and format."""
        from config import SUPPORTED_IMAGE_FORMATS

        if not file_path.exists():
            return False, "File not found"

        if file_path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
            return False, f"Unsupported format. Supported: {', '.join(SUPPORTED_IMAGE_FORMATS)}"

        size_mb = FileUtil.get_file_size_mb(file_path)
        if size_mb > max_size_mb:
            return False, f"File size exceeds {max_size_mb}MB limit"

        return True, "Valid"

    @staticmethod
    def ensure_directory(directory: Path) -> None:
        """Ensure directory exists, create if not."""
        directory.mkdir(parents=True, exist_ok=True)


class DataUtil:
    """Data processing utilities."""

    @staticmethod
    def serialize_to_json(data: Any) -> str:
        """Serialize data to JSON string."""
        try:
            return json.dumps(data, default=str)
        except Exception as e:
            Logger.error("Failed to serialize data to JSON", "DataUtil", exception=e)
            return "{}"

    @staticmethod
    def deserialize_from_json(json_str: str) -> Any:
        """Deserialize JSON string to Python object."""
        try:
            return json.loads(json_str)
        except Exception as e:
            Logger.error("Failed to deserialize JSON", "DataUtil", exception=e)
            return {}


# Global logger instance
app_logger = Logger()
