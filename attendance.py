"""
Attendance tracking for Staff Attendance Manager.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta

from config import ATTENDANCE_STATUS
from utils import Logger, DateTimeUtil


@dataclass
class AttendanceRecord:
    """Attendance record data model."""

    employee_id: str
    name: str
    date: str
    time_in: str
    time_out: Optional[str] = None
    status: str = "Inside"
    duration: Optional[str] = None
    present: bool = True
    created_at: str = field(default_factory=DateTimeUtil.get_current_datetime)

    def validate(self) -> Tuple[bool, str]:
        """Validate attendance record."""
        if not self.employee_id:
            return False, "Employee ID is required"

        if not self.date or not DateTimeUtil.parse_date(self.date):
            return False, "Invalid date format"

        if not self.time_in:
            return False, "Time In is required"

        if self.status not in ["Inside", "Outside"]:
            return False, f"Invalid status: {self.status}"

        return True, "Valid"

    def calculate_duration(self) -> Optional[str]:
        """Calculate duration between time_in and time_out."""
        if not self.time_out:
            return None

        try:
            time_in = datetime.strptime(self.time_in, "%H:%M:%S")
            time_out = datetime.strptime(self.time_out, "%H:%M:%S")

            if time_out < time_in:
                time_out = time_out.replace(day=time_out.day + 1)

            duration = time_out - time_in
            hours = duration.total_seconds() / 3600
            return f"{hours:.2f}"
        except Exception:
            return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "date": self.date,
            "time_in": self.time_in,
            "time_out": self.time_out,
            "status": self.status,
            "duration": self.duration,
            "present": self.present,
            "created_at": self.created_at,
        }


@dataclass
class MovementLog:
    """Movement log record data model."""

    employee_id: str
    name: str
    date: str
    time: str
    action: str
    status: str
    notes: Optional[str] = None
    created_at: str = field(default_factory=DateTimeUtil.get_current_datetime)

    def validate(self) -> Tuple[bool, str]:
        """Validate movement log."""
        if not self.employee_id:
            return False, "Employee ID is required"

        if not self.date:
            return False, "Date is required"

        if not self.time:
            return False, "Time is required"

        valid_actions = ["Present", "Go Outside", "Come Back"]
        if self.action not in valid_actions:
            return False, f"Invalid action. Must be one of: {', '.join(valid_actions)}"

        valid_statuses = ["Inside", "Outside"]
        if self.status not in valid_statuses:
            return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"

        return True, "Valid"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "date": self.date,
            "time": self.time,
            "action": self.action,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
        }


class AttendanceManager:
    """Manages attendance operations."""

    def __init__(self):
        """Initialize attendance manager."""
        self.logger = Logger()
        self.attendance_records: Dict[str, List[AttendanceRecord]] = {}
        self.movement_logs: Dict[str, List[MovementLog]] = {}

    def mark_present(self, employee_id: str, name: str) -> Tuple[bool, str]:
        """Mark employee as present."""
        date = DateTimeUtil.get_current_date()
        time_in = DateTimeUtil.get_current_time()

        if self._is_attendance_duplicate(employee_id, date):
            return False, "Employee already marked present today"

        record = AttendanceRecord(
            employee_id=employee_id,
            name=name,
            date=date,
            time_in=time_in,
            status="Inside",
            present=True
        )

        is_valid, msg = record.validate()
        if not is_valid:
            return False, msg

        if employee_id not in self.attendance_records:
            self.attendance_records[employee_id] = []

        self.attendance_records[employee_id].append(record)

        self._add_movement_log(
            employee_id=employee_id,
            name=name,
            date=date,
            time=time_in,
            action="Present",
            status="Inside"
        )

        self.logger.info(f"Employee marked present: {employee_id}", "AttendanceManager")
        return True, "Employee marked present"

    def go_outside(self, employee_id: str, name: str) -> Tuple[bool, str]:
        """Mark employee as going outside."""
        date = DateTimeUtil.get_current_date()
        time_outside = DateTimeUtil.get_current_time()

        record = self._get_todays_record(employee_id, date)
        if not record:
            return False, "Employee not marked present today"

        if record.status == "Outside":
            return False, "Employee already marked as outside"

        record.time_out = time_outside
        record.status = "Outside"

        self._add_movement_log(
            employee_id=employee_id,
            name=name,
            date=date,
            time=time_outside,
            action="Go Outside",
            status="Outside"
        )

        self.logger.info(f"Employee marked outside: {employee_id}", "AttendanceManager")
        return True, "Employee marked as outside"

    def come_back(self, employee_id: str, name: str) -> Tuple[bool, str]:
        """Mark employee as coming back inside."""
        date = DateTimeUtil.get_current_date()
        time_back = DateTimeUtil.get_current_time()

        record = self._get_todays_record(employee_id, date)
        if not record:
            return False, "Employee not marked present today"

        if record.status == "Inside":
            return False, "Employee already inside"

        record.status = "Inside"
        record.time_out = None

        self._add_movement_log(
            employee_id=employee_id,
            name=name,
            date=date,
            time=time_back,
            action="Come Back",
            status="Inside"
        )

        self.logger.info(f"Employee came back: {employee_id}", "AttendanceManager")
        return True, "Employee marked as back inside"

    def get_todays_attendance(self) -> Dict[str, Any]:
        """Get today's attendance summary."""
        date = DateTimeUtil.get_current_date()
        summary = {
            "total_present": 0,
            "total_inside": 0,
            "total_outside": 0,
            "total_absent": 0,
            "records": []
        }

        for emp_id, records in self.attendance_records.items():
            for record in records:
                if record.date == date:
                    summary["total_present"] += 1
                    if record.status == "Inside":
                        summary["total_inside"] += 1
                    else:
                        summary["total_outside"] += 1
                    summary["records"].append(record.to_dict())

        return summary

    def get_attendance_history(self, employee_id: str) -> List[AttendanceRecord]:
        """Get attendance history for employee."""
        return self.attendance_records.get(employee_id, [])

    def get_movement_history(self, employee_id: Optional[str] = None, date: Optional[str] = None) -> List[MovementLog]:
        """Get movement history with optional filters."""
        logs = []

        if employee_id:
            logs = self.movement_logs.get(employee_id, [])
        else:
            for emp_logs in self.movement_logs.values():
                logs.extend(emp_logs)

        if date:
            logs = [log for log in logs if log.date == date]

        return sorted(logs, key=lambda x: x.time, reverse=True)

    def get_recent_activity(self, limit: int = 20) -> List[MovementLog]:
        """Get recent activity logs."""
        all_logs = []
        for emp_logs in self.movement_logs.values():
            all_logs.extend(emp_logs)

        all_logs.sort(key=lambda x: x.created_at, reverse=True)
        return all_logs[:limit]

    def get_employee_status(self, employee_id: str) -> str:
        """Get current status of employee."""
        date = DateTimeUtil.get_current_date()
        record = self._get_todays_record(employee_id, date)

        if not record:
            return "Absent"

        if record.status == "Inside":
            return "Inside"
        else:
            return "Outside"

    def get_attendance_percentage(self, employee_id: str, days: int = 30) -> float:
        """Calculate attendance percentage for employee."""
        if employee_id not in self.attendance_records:
            return 0.0

        records = self.attendance_records[employee_id]
        cutoff_date = DateTimeUtil.parse_date(DateTimeUtil.get_current_date()) - timedelta(days=days)

        present_days = 0
        for record in records:
            record_date = DateTimeUtil.parse_date(record.date)
            if record_date and record_date > cutoff_date and record.present:
                present_days += 1

        if days == 0:
            return 0.0

        return (present_days / days) * 100

    def _is_attendance_duplicate(self, employee_id: str, date: str) -> bool:
        """Check if attendance already recorded for the day."""
        records = self.attendance_records.get(employee_id, [])
        return any(record.date == date for record in records)

    def _get_todays_record(self, employee_id: str, date: str) -> Optional[AttendanceRecord]:
        """Get today's attendance record for employee."""
        records = self.attendance_records.get(employee_id, [])
        for record in records:
            if record.date == date:
                return record
        return None

    def _add_movement_log(self, employee_id: str, name: str, date: str, time: str,
                          action: str, status: str, notes: Optional[str] = None) -> bool:
        """Add movement log record."""
        log = MovementLog(
            employee_id=employee_id,
            name=name,
            date=date,
            time=time,
            action=action,
            status=status,
            notes=notes
        )

        is_valid, msg = log.validate()
        if not is_valid:
            self.logger.error(f"Invalid movement log: {msg}", "AttendanceManager")
            return False

        if employee_id not in self.movement_logs:
            self.movement_logs[employee_id] = []

        self.movement_logs[employee_id].append(log)
        return True

    def get_statistics(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get attendance statistics."""
        if not date:
            date = DateTimeUtil.get_current_date()

        inside_count = 0
        outside_count = 0
        present_count = 0

        for emp_id, records in self.attendance_records.items():
            for record in records:
                if record.date == date and record.present:
                    present_count += 1
                    if record.status == "Inside":
                        inside_count += 1
                    else:
                        outside_count += 1

        return {
            "date": date,
            "present": present_count,
            "inside": inside_count,
            "outside": outside_count,
        }
