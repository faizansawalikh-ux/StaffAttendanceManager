"""
Database management for Staff Attendance Manager.
Handles data persistence and synchronization between memory and Excel.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from threading import Lock
from datetime import datetime

from config import DATABASE_FILE, BACKUP_FREQUENCY_MINUTES
from utils import Logger, BackupUtil, DateTimeUtil
from excel_manager import ExcelManager
from employee import Employee, EmployeeManager
from attendance import AttendanceManager, MovementLog


class DatabaseManager:
    """Manages database operations and data synchronization."""

    def __init__(self, database_file: Path = DATABASE_FILE):
        """Initialize database manager."""
        self.database_file = database_file
        self.excel_manager = ExcelManager(database_file)
        self.employee_manager = EmployeeManager()
        self.attendance_manager = AttendanceManager()
        self.logger = Logger()
        self.lock = Lock()
        self.last_backup = None

        self._initialize_database()

    def _initialize_database(self) -> None:
        """Initialize database if it doesn't exist."""
        try:
            if not self.database_file.exists():
                success = self.excel_manager.initialize_workbook()
                if success:
                    self.logger.info("Database initialized", "DatabaseManager")
                else:
                    self.logger.error("Failed to initialize database", "DatabaseManager")
            else:
                self._load_all_data()
        except Exception as e:
            self.logger.error("Database initialization error", "DatabaseManager", exception=e)

    def add_employee(self, employee: Employee) -> tuple:
        """Add employee to database."""
        with self.lock:
            try:
                success, msg = self.employee_manager.add_employee(employee)
                if not success:
                    return False, msg

                if not self.excel_manager.add_employee_record(employee):
                    self.logger.error("Failed to save employee to Excel", "DatabaseManager")
                    return False, "Failed to save to database"

                self._auto_backup()
                return True, "Employee added successfully"
            except Exception as e:
                self.logger.error("Error adding employee", "DatabaseManager", exception=e)
                return False, "Database error"

    def update_employee(self, employee_id: str, employee: Employee) -> tuple:
        """Update employee in database."""
        with self.lock:
            try:
                success, msg = self.employee_manager.update_employee(employee_id, employee)
                if not success:
                    return False, msg

                if not self.excel_manager.update_employee_record(employee_id, employee):
                    return False, "Failed to update database"

                self._auto_backup()
                return True, "Employee updated successfully"
            except Exception as e:
                self.logger.error("Error updating employee", "DatabaseManager", exception=e)
                return False, "Database error"

    def delete_employee(self, employee_id: str) -> tuple:
        """Delete employee from database."""
        with self.lock:
            try:
                success, msg = self.employee_manager.delete_employee(employee_id)
                if not success:
                    return False, msg

                if not self.excel_manager.delete_employee_record(employee_id):
                    return False, "Failed to delete from database"

                self._auto_backup()
                return True, "Employee deleted successfully"
            except Exception as e:
                self.logger.error("Error deleting employee", "DatabaseManager", exception=e)
                return False, "Database error"

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID."""
        return self.employee_manager.get_employee(employee_id)

    def get_all_employees(self) -> List[Employee]:
        """Get all employees."""
        return self.employee_manager.get_all_employees()

    def search_employees(self, query: str) -> List[Employee]:
        """Search employees."""
        return self.employee_manager.search_employees(query)

    def mark_present(self, employee_id: str, name: str) -> tuple:
        """Mark employee as present."""
        with self.lock:
            try:
                success, msg = self.attendance_manager.mark_present(employee_id, name)
                if not success:
                    return False, msg

                record = self._get_latest_attendance_record(employee_id)
                if record:
                    if not self.excel_manager.add_attendance_record(record.to_dict()):
                        self.logger.warning("Failed to save attendance to Excel", "DatabaseManager")

                self._auto_backup()
                return True, msg
            except Exception as e:
                self.logger.error("Error marking present", "DatabaseManager", exception=e)
                return False, "Database error"

    def go_outside(self, employee_id: str, name: str) -> tuple:
        """Mark employee as going outside."""
        with self.lock:
            try:
                success, msg = self.attendance_manager.go_outside(employee_id, name)
                if not success:
                    return False, msg

                log = self._get_latest_movement_log(employee_id)
                if log:
                    if not self.excel_manager.add_movement_log(log.to_dict()):
                        self.logger.warning("Failed to save movement log to Excel", "DatabaseManager")

                self._auto_backup()
                return True, msg
            except Exception as e:
                self.logger.error("Error in go_outside", "DatabaseManager", exception=e)
                return False, "Database error"

    def come_back(self, employee_id: str, name: str) -> tuple:
        """Mark employee as coming back inside."""
        with self.lock:
            try:
                success, msg = self.attendance_manager.come_back(employee_id, name)
                if not success:
                    return False, msg

                log = self._get_latest_movement_log(employee_id)
                if log:
                    if not self.excel_manager.add_movement_log(log.to_dict()):
                        self.logger.warning("Failed to save movement log to Excel", "DatabaseManager")

                self._auto_backup()
                return True, msg
            except Exception as e:
                self.logger.error("Error in come_back", "DatabaseManager", exception=e)
                return False, "Database error"

    def get_todays_attendance(self) -> Dict[str, Any]:
        """Get today's attendance summary."""
        return self.attendance_manager.get_todays_attendance()

    def get_employee_status(self, employee_id: str) -> str:
        """Get current status of employee."""
        return self.attendance_manager.get_employee_status(employee_id)

    def get_movement_history(self, employee_id: Optional[str] = None, date: Optional[str] = None) -> List[MovementLog]:
        """Get movement history."""
        return self.attendance_manager.get_movement_history(employee_id, date)

    def get_recent_activity(self, limit: int = 20) -> List[MovementLog]:
        """Get recent activity."""
        return self.attendance_manager.get_recent_activity(limit)

    def get_employee_statistics(self) -> Dict[str, Any]:
        """Get employee statistics."""
        return self.employee_manager.get_statistics()

    def get_attendance_statistics(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get attendance statistics."""
        return self.attendance_manager.get_statistics(date)

    def _load_all_data(self) -> None:
        """Load all data from Excel into memory."""
        try:
            employees = self.excel_manager.get_employees()
            for emp_dict in employees:
                emp = Employee(**emp_dict)
                self.employee_manager.employees[emp.employee_id] = emp

            self.logger.info(f"Loaded {len(employees)} employees from Excel", "DatabaseManager")
        except Exception as e:
            self.logger.error("Failed to load data", "DatabaseManager", exception=e)

    def _get_latest_attendance_record(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get latest attendance record for employee."""
        records = self.attendance_manager.get_attendance_history(employee_id)
        if records:
            return records[-1].to_dict()
        return None

    def _get_latest_movement_log(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get latest movement log for employee."""
        logs = self.attendance_manager.get_movement_history(employee_id)
        if logs:
            return logs[0].to_dict()
        return None

    def _auto_backup(self) -> None:
        """Create automatic backup if needed."""
        try:
            current_time = DateTimeUtil.get_current_datetime()

            if self.last_backup is None or self._should_backup():
                backup_path = BackupUtil.create_backup(self.database_file)
                if backup_path:
                    self.last_backup = current_time
                    BackupUtil.cleanup_old_backups()
        except Exception as e:
            self.logger.warning("Auto backup failed", "DatabaseManager")

    def _should_backup(self) -> bool:
        """Check if backup should be performed."""
        if self.last_backup is None:
            return True

        last_backup_time = DateTimeUtil.parse_date(self.last_backup, "%d-%m-%Y %H:%M:%S")
        current_time = datetime.now()

        if last_backup_time:
            diff_minutes = (current_time - last_backup_time).total_seconds() / 60
            return diff_minutes >= BACKUP_FREQUENCY_MINUTES

        return True

    def backup_now(self) -> tuple:
        """Create backup immediately."""
        try:
            backup_path = BackupUtil.create_backup(self.database_file)
            if backup_path:
                self.last_backup = DateTimeUtil.get_current_datetime()
                return True, f"Backup created: {backup_path.name}"
            return False, "Failed to create backup"
        except Exception as e:
            self.logger.error("Backup error", "DatabaseManager", exception=e)
            return False, "Backup error"

    def restore_backup(self, backup_path: Path) -> tuple:
        """Restore from backup."""
        try:
            success = BackupUtil.restore_backup(backup_path, self.database_file)
            if success:
                self._load_all_data()
                return True, "Backup restored successfully"
            return False, "Failed to restore backup"
        except Exception as e:
            self.logger.error("Restore error", "DatabaseManager", exception=e)
            return False, "Restore error"

    def get_backups(self) -> List[Path]:
        """Get list of all backups."""
        return BackupUtil.get_backups()
