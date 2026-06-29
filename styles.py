"""
Styling module for Staff Attendance Manager.
Defines modern dark theme with Microsoft Office styling.
"""

from config import COLORS, FONT_FAMILY, FONT_SIZES


class Stylesheet:
    """Centralized stylesheet management."""

    @staticmethod
    def get_main_stylesheet() -> str:
        """Get main application stylesheet."""
        return f"""
        QMainWindow {{
            background-color: {COLORS['background']};
            color: {COLORS['text_primary']};
            font-family: {FONT_FAMILY};
        }}

        QWidget {{
            background-color: {COLORS['background']};
            color: {COLORS['text_primary']};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZES['body']}pt;
        }}

        /* Sidebar */
        QListWidget {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: none;
            outline: none;
        }}

        QListWidget::item {{
            padding: 12px;
            border-radius: 4px;
            margin: 4px;
        }}

        QListWidget::item:selected {{
            background-color: {COLORS['primary']};
            color: white;
        }}

        QListWidget::item:hover {{
            background-color: {COLORS['surface_light']};
        }}

        /* Buttons */
        QPushButton {{
            background-color: {COLORS['primary']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: {FONT_SIZES['body']}pt;
            outline: none;
        }}

        QPushButton:hover {{
            background-color: {COLORS['primary_dark']};
        }}

        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
        }}

        QPushButton:disabled {{
            background-color: {COLORS['text_disabled']};
            color: {COLORS['text_secondary']};
        }}

        /* Secondary Button */
        QPushButton#secondaryButton {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
        }}

        QPushButton#secondaryButton:hover {{
            background-color: {COLORS['border']};
        }}

        /* Danger Button */
        QPushButton#dangerButton {{
            background-color: {COLORS['danger']};
        }}

        QPushButton#dangerButton:hover {{
            background-color: #C50F1F;
        }}

        /* Success Button */
        QPushButton#successButton {{
            background-color: {COLORS['success']};
        }}

        QPushButton#successButton:hover {{
            background-color: #0A7D0A;
        }}

        /* Line Edit / Input */
        QLineEdit {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 8px 12px;
            font-size: {FONT_SIZES['body']}pt;
            selection-background-color: {COLORS['primary']};
        }}

        QLineEdit:focus {{
            border: 2px solid {COLORS['primary']};
        }}

        /* Text Edit */
        QTextEdit {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 8px 12px;
            font-size: {FONT_SIZES['body']}pt;
        }}

        QTextEdit:focus {{
            border: 2px solid {COLORS['primary']};
        }}

        /* ComboBox */
        QComboBox {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 8px 12px;
            font-size: {FONT_SIZES['body']}pt;
        }}

        QComboBox:focus {{
            border: 2px solid {COLORS['primary']};
        }}

        QComboBox::drop-down {{
            border: none;
        }}

        QComboBox::down-arrow {{
            image: none;
            background-color: {COLORS['primary']};
        }}

        /* Dropdown Menu */
        QComboBox QAbstractItemView {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            selection-background-color: {COLORS['primary']};
            outline: none;
        }}

        /* Label */
        QLabel {{
            color: {COLORS['text_primary']};
            font-size: {FONT_SIZES['body']}pt;
        }}

        QLabel#heading1 {{
            font-size: {FONT_SIZES['h1']}pt;
            font-weight: bold;
        }}

        QLabel#heading2 {{
            font-size: {FONT_SIZES['h2']}pt;
            font-weight: bold;
        }}

        QLabel#heading3 {{
            font-size: {FONT_SIZES['h3']}pt;
            font-weight: bold;
        }}

        QLabel#secondary {{
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['small']}pt;
        }}

        /* Table Widget */
        QTableWidget {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            gridline-color: {COLORS['border']};
        }}

        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {COLORS['border']};
        }}

        QTableWidget::item:selected {{
            background-color: {COLORS['primary']};
        }}

        /* Table Header */
        QHeaderView::section {{
            background-color: {COLORS['primary']};
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }}

        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {COLORS['surface']};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {COLORS['border']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['text_secondary']};
        }}

        QScrollBar:horizontal {{
            background-color: {COLORS['surface']};
            height: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {COLORS['border']};
            border-radius: 6px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {COLORS['text_secondary']};
        }}

        /* Spin Box */
        QSpinBox, QDoubleSpinBox {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 8px 12px;
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 2px solid {COLORS['primary']};
        }}

        /* Date/Time Edit */
        QDateEdit, QTimeEdit, QDateTimeEdit {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 8px 12px;
        }}

        QDateEdit:focus, QTimeEdit:focus, QDateTimeEdit:focus {{
            border: 2px solid {COLORS['primary']};
        }}

        /* CheckBox */
        QCheckBox {{
            color: {COLORS['text_primary']};
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 3px;
            background-color: {COLORS['surface_light']};
            border: 1px solid {COLORS['border']};
        }}

        QCheckBox::indicator:checked {{
            background-color: {COLORS['primary']};
            border: 1px solid {COLORS['primary']};
        }}

        /* RadioButton */
        QRadioButton {{
            color: {COLORS['text_primary']};
            spacing: 8px;
        }}

        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 9px;
            background-color: {COLORS['surface_light']};
            border: 1px solid {COLORS['border']};
        }}

        QRadioButton::indicator:checked {{
            background-color: {COLORS['primary']};
            border: 2px solid {COLORS['primary']};
        }}

        /* TabWidget */
        QTabWidget {{
            background-color: {COLORS['background']};
        }}

        QTabBar::tab {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_secondary']};
            padding: 8px 16px;
            border-bottom: 2px solid transparent;
        }}

        QTabBar::tab:selected {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border-bottom: 2px solid {COLORS['primary']};
        }}

        QTabBar::tab:hover {{
            background-color: {COLORS['surface_light']};
        }}

        /* GroupBox */
        QGroupBox {{
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 3px;
        }}

        /* Dialog */
        QDialog {{
            background-color: {COLORS['background']};
        }}

        /* Menu Bar */
        QMenuBar {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border-bottom: 1px solid {COLORS['border']};
        }}

        QMenuBar::item:selected {{
            background-color: {COLORS['primary']};
        }}

        /* Menu */
        QMenu {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
        }}

        QMenu::item:selected {{
            background-color: {COLORS['primary']};
        }}

        /* Status Bar */
        QStatusBar {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            border-top: 1px solid {COLORS['border']};
        }}

        /* Message Box */
        QMessageBox {{
            background-color: {COLORS['background']};
        }}

        QMessageBox QLabel {{
            color: {COLORS['text_primary']};
        }}

        /* Card Style */
        QFrame#card {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 16px;
        }}

        /* Progress Bar */
        QProgressBar {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            text-align: center;
            padding: 2px;
        }}

        QProgressBar::chunk {{
            background-color: {COLORS['primary']};
            border-radius: 2px;
        }}
        """

    @staticmethod
    def get_card_stylesheet() -> str:
        """Get card styling."""
        return f"""
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 16px;
        """

    @staticmethod
    def get_button_stylesheet(button_type: str = "primary") -> str:
        """Get button styling based on type."""
        if button_type == "danger":
            return f"""
            background-color: {COLORS['danger']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            """
        elif button_type == "success":
            return f"""
            background-color: {COLORS['success']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            """
        elif button_type == "warning":
            return f"""
            background-color: {COLORS['warning']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            """
        else:  # primary
            return f"""
            background-color: {COLORS['primary']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            """

    @staticmethod
    def get_input_stylesheet() -> str:
        """Get input field styling."""
        return f"""
        background-color: {COLORS['surface_light']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 8px 12px;
        """
