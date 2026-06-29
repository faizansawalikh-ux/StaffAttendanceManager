"""
Employee model and management for Staff Attendance Manager.
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from utils import Logger, Validator, DateTimeUtil


@dataclass
class Employee:
    """Employee data model."""

    employee_id: str
    name: str
    department: str
    designation: str
    phone: str
    email: str
    joining_date: str
    status: str = "Active"
    photo_path: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = field(default_factory=DateTimeUtil.get_current_datetime)
    updated_at: str = field(default_factory=DateTimeUtil.get_current_datetime)

    def validate(self) -> tuple:
        """Validate employee data."""
        if not self.employee_id or not self.employee_id.strip():
            return False, "Employee ID is required"

        if not self.name or not self.name.strip():
            return False, "Employee name is required"

        if not self.department or not self.department.strip():
            return False, "Department is required"

        if not self.designation or not self.designation.strip():
            return False, "Designation is required"

        if not Validator.validate_phone(self.phone):
            return False, "Invalid phone number format"

        if not Validator.validate_email(self.email):
            return False, "Invalid email format"

        if not Validator.validate_date(self.joining_date):
            return False, "Invalid joining date format (use DD-MM-YYYY)"

        if self.photo_path and not Path(self.photo_path).exists():
            Logger.warning(f"Photo not found: {self.photo_path}", "Employee")

        return True, "Valid"

    def to_dict(self) -> Dict[str, Any]:
        """Convert employee to dictionary."""
        data = asdict(self)
        data["updated_at"] = DateTimeUtil.get_current_datetime()
        return data


class EmployeeManager:
    """Manages employee operations."""

    def __init__(self):
        """Initialize employee manager."""
        self.employees: Dict[str, Employee] = {}
        self.logger = Logger()

    def add_employee(self, employee: Employee) -> tuple:
        """Add new employee."""
        is_valid, message = employee.validate()
        if not is_valid:
            return False, message

        if employee.employee_id in self.employees:
            return False, f"Employee ID {employee.employee_id} already exists"

        self.employees[employee.employee_id] = employee
        self.logger.info(f"Employee added: {employee.employee_id}", "EmployeeManager")
        return True, "Employee added successfully"

    def update_employee(self, employee_id: str, employee: Employee) -> tuple:
        """Update existing employee."""
        if employee_id not in self.employees:
            return False, f"Employee {employee_id} not found"

        is_valid, message = employee.validate()
        if not is_valid:
            return False, message

        self.employees[employee_id] = employee
        self.logger.info(f"Employee updated: {employee_id}", "EmployeeManager")
        return True, "Employee updated successfully"

    def delete_employee(self, employee_id: str) -> tuple:
        """Delete employee."""
        if employee_id not in self.employees:
            return False, f"Employee {employee_id} not found"

        del self.employees[employee_id]
        self.logger.info(f"Employee deleted: {employee_id}", "EmployeeManager")
        return True, "Employee deleted successfully"

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID."""
        return self.employees.get(employee_id)

    def get_all_employees(self) -> List[Employee]:
        """Get all employees."""
        return list(self.employees.values())

    def get_employees_by_department(self, department: str) -> List[Employee]:
        """Get employees by department."""
        return [
            emp for emp in self.employees.values()
            if emp.department == department
        ]

    def search_employees(self, query: str) -> List[Employee]:
        """Search employees by ID, name, department, phone, or email."""
        query_lower = query.lower()
        results = []

        for emp in self.employees.values():
            if (query_lower in emp.employee_id.lower() or
                query_lower in emp.name.lower() or
                query_lower in emp.department.lower() or
                query_lower in emp.phone or
                query_lower in emp.email.lower()):
                results.append(emp)

        return results

    def get_active_employees(self) -> List[Employee]:
        """Get only active employees."""
        return [emp for emp in self.employees.values() if emp.status == "Active"]

    def get_inactive_employees(self) -> List[Employee]:
        """Get only inactive employees."""
        return [emp for emp in self.employees.values() if emp.status != "Active"]

    def get_employee_count(self) -> int:
        """Get total employee count."""
        return len(self.employees)

    def get_employees_by_status(self, status: str) -> List[Employee]:
        """Get employees by status."""
        return [emp for emp in self.employees.values() if emp.status == status]

    def is_duplicate_id(self, employee_id: str, exclude_id: Optional[str] = None) -> bool:
        """Check if employee ID is duplicate."""
        if exclude_id:
            return employee_id in self.employees and employee_id != exclude_id
        return employee_id in self.employees

    def bulk_import(self, employees: List[Employee]) -> tuple:
        """
        Bulk import employees.

        Returns:
            Tuple of (successful_count, failed_count, error_messages)
        """
        success_count = 0
        failed_count = 0
        errors = []

        for idx, emp in enumerate(employees, 1):
            success, msg = self.add_employee(emp)
            if success:
                success_count += 1
            else:
                failed_count += 1
                errors.append(f"Row {idx} ({emp.employee_id}): {msg}")

        self.logger.info(
            f"Bulk import completed: {success_count} successful, {failed_count} failed",
            "EmployeeManager"
        )
        return success_count, failed_count, errors

    def get_statistics(self) -> Dict[str, Any]:
        """Get employee statistics."""
        employees = self.get_all_employees()
        departments = {}

        for emp in employees:
            dept = emp.department
            if dept not in departments:
                departments[dept] = 0
            departments[dept] += 1

        return {
            "total": len(employees),
            "active": len(self.get_active_employees()),
            "inactive": len(self.get_inactive_employees()),
            "by_department": departments,
        }
