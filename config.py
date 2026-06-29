"""
Configuration module for Staff Attendance Manager application.
Centralizes all application settings and constants.
"""

from pathlib import Path

# Application Information
APP_NAME = "Staff Attendance Manager"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Company"

# Paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
IMAGES_DIR = ASSETS_DIR / "images"
EXPORTS_DIR = BASE_DIR / "exports"
BACKUP_DIR = BASE_DIR / "backup"
DATABASE_DIR = BASE_DIR / "data"

# Create directories if they don't exist
for directory in [ASSETS_DIR, ICONS_DIR, IMAGES_DIR, EXPORTS_DIR, BACKUP_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database Configuration
DATABASE_FILE = DATABASE_DIR / "attendance_data.xlsx"
BACKUP_RETENTION_DAYS = 30
MAX_BACKUPS = 10

# UI Configuration
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# Colors - Modern Dark Theme with Blue Accent
COLORS = {
    "primary": "#0078D4",  # Microsoft Blue
    "primary_dark": "#005A9E",
    "primary_light": "#107C10",
    "background": "#1E1E1E",  # Dark background
    "surface": "#252526",  # Card background
    "surface_light": "#2D2D30",  # Lighter surface
    "text_primary": "#FFFFFF",
    "text_secondary": "#B4B4B4",
    "text_disabled": "#808080",
    "success": "#107C10",
    "warning": "#FFB900",
    "danger": "#E81123",
    "border": "#3E3E42",
}

# Fonts
FONT_FAMILY = "Segoe UI"
FONT_SIZES = {
    "h1": 24,
    "h2": 20,
    "h3": 16,
    "body": 11,
    "small": 9,
    "caption": 8,
}

# Attendance Status
ATTENDANCE_STATUS = {
    "present": "Present",
    "absent": "Absent",
    "inside": "Inside",
    "outside": "Outside",
    "on_leave": "On Leave",
}

# Department Templates
DEFAULT_DEPARTMENTS = [
    "Administration",
    "IT",
    "Human Resources",
    "Sales",
    "Marketing",
    "Finance",
    "Operations",
    "Customer Service",
]

# Designation Templates
DEFAULT_DESIGNATIONS = [
    "Manager",
    "Senior Executive",
    "Executive",
    "Junior Executive",
    "Internship",
    "Contractual",
]

# Backup Configuration
BACKUP_FREQUENCY_MINUTES = 30
AUTO_BACKUP_ENABLED = True

# Excel Sheet Names
EXCEL_SHEETS = {
    "employees": "Employees",
    "attendance": "Attendance",
    "movement_log": "MovementLog",
    "daily_report": "DailyReport",
    "monthly_report": "MonthlyReport",
    "dashboard_data": "DashboardData",
}

# Report Settings
REPORT_DATE_FORMAT = "%d-%m-%Y"
REPORT_TIME_FORMAT = "%H:%M:%S"
REPORT_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"

# Search Configuration
SEARCH_FIELDS = ["employee_id", "name", "department", "phone", "status"]
SEARCH_DEBOUNCE_MS = 300

# File Size Limits
MAX_PHOTO_SIZE_MB = 5
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp"]

# Performance
BATCH_SIZE = 100
CACHE_TIMEOUT_SECONDS = 300

# Logging
LOG_FILE = BASE_DIR / "logs" / "attendance_manager.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Pagination
ITEMS_PER_PAGE = 50
MAX_RECENT_ACTIVITIES = 20
