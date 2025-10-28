# Упрощаем импорт для потребителей пакета
from .exceptions import InvalidDateError, PermissionDeniedError, CourseNotFoundError
from .permissions import check_permissions
from .course import Course
from .handlers import InstructorHandler, MethodologyDepartmentHandler, ManagementHandler
from .models import Address, Platform
