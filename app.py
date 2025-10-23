import json
import logging
from abc import ABC, ABCMeta, abstractmethod
from datetime import date
from typing import List, Dict, Any, Optional


# ==========================
# 1. ИСКЛЮЧЕНИЯ
# ==========================
class InvalidDateError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


# ==========================
# 2. ДЕКОРАТОР
# ==========================
def check_permissions(required_role: str):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            user_role = getattr(self, "user_role", "student")
            if user_role != required_role:
                raise PermissionDeniedError(
                    f"Недостаточно прав: требуется роль '{required_role}'."
                )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


# ==========================
# 3. МИКСИНЫ
# ==========================
class LoggingMixin:
    def log_action(self, message: str):
        logging.info(f"[LOG] {message}")


class NotificationMixin:
    def notify_students(self, message: str):
        for student in self.students:
            logging.info(f"Уведомление для {student}: {message}")


# ==========================
# 4. ИНТЕРФЕЙСЫ
# ==========================
class Teachable(ABC):
    @abstractmethod
    def teach(self) -> str:
        pass


class Assessable(ABC):
    @abstractmethod
    def assess_progress(self) -> str:
        pass


# ==========================
# 5. МЕТАКЛАСС
# ==========================


class CourseMeta(ABCMeta):
    """Метакласс, регистрирующий все подклассы Course."""

    registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # Не регистрируем сам базовый класс Course
        if name != "Course":
            CourseMeta.registry[name.lower()] = cls
        return cls


# ==========================
# 6. АБСТРАКТНЫЙ КЛАСС COURSE
# ==========================
class Course(ABC, LoggingMixin, NotificationMixin, metaclass=CourseMeta):
    def __init__(
        self,
        title: str,
        start_date: date,
        end_date: date,
        instructor: str,
        students: List[str],
        topics: List[str],
    ):
        if end_date < start_date:
            raise InvalidDateError(
                "Дата окончания курса не может быть раньше даты начала."
            )
        self._title = title
        self._start_date = start_date
        self._end_date = end_date
        self._instructor = instructor
        self._students = students
        self._topics = topics

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def students(self):
        return self._students

    @property
    def duration(self):
        return (self._end_date - self._start_date).days

    @abstractmethod
    def calculate_completion_rate(self) -> float:
        pass

    def __str__(self):
        return f"Курс: {self._title}, Преподаватель: {self._instructor}"

    def __eq__(self, other):
        return len(self.students) == len(other.students)

    def __lt__(self, other):
        return len(self.students) < len(other.students)

    def __gt__(self, other):
        return len(self.students) > len(other.students)

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "title": self._title,
            "start_date": str(self._start_date),
            "end_date": str(self._end_date),
            "instructor": self._instructor,
            "students": self._students,
            "topics": self._topics,
        }


# ==========================
# 7. ПОДКЛАССЫ
# ==========================
class ProgrammingCourse(Course, Teachable, Assessable):
    def __init__(
        self, title, start_date, end_date, instructor, students, topics, languages
    ):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.languages = languages

    def calculate_completion_rate(self):
        return len(self.topics) * 10

    def teach(self):
        return "Провожу лекции по алгоритмам."

    def assess_progress(self):
        return "Оцениваю практические задания по коду."

    def __str__(self):
        return f"[Программирование] {self.title} ({', '.join(self.languages)})"


class DesignCourse(Course, Teachable, Assessable):
    def __init__(
        self, title, start_date, end_date, instructor, students, topics, tools
    ):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.tools = tools

    def calculate_completion_rate(self):
        return len(self.students) * 5

    def teach(self):
        return "Объясняю принципы композиции."

    def assess_progress(self):
        return "Оцениваю дизайн-проекты студентов."

    def __str__(self):
        return f"[Дизайн] {self.title} ({', '.join(self.tools)})"


class ScienceCourse(Course, Teachable, Assessable):
    def __init__(
        self, title, start_date, end_date, instructor, students, topics, field
    ):
        super().__init__(title, start_date, end_date, instructor, students, topics)
        self.field = field

    def calculate_completion_rate(self):
        return (len(self.topics) + len(self.students)) * 3

    def teach(self):
        return "Провожу лабораторные работы."

    def assess_progress(self):
        return "Оцениваю лабораторные отчёты."

    def __str__(self):
        return f"[Наука] {self.title} ({self.field})"


# ==========================
# 8. ПЛАТФОРМА И АДРЕС
# ==========================
class Address:
    def __init__(self, city, street, building):
        self.city, self.street, self.building = city, street, building

    def __str__(self):
        return f"{self.city}, {self.street}, {self.building}"


class Platform:
    def __init__(self, name, address):
        self.name, self.address = name, address
        self._courses = []

    def add_course(self, course):
        self._courses.append(course)

    def remove_course(self, title):
        self._courses = [c for c in self._courses if c.title != title]

    def get_courses(self):
        return self._courses

    def get_top_courses(self, n=3):
        return sorted(self._courses, key=lambda c: len(c.students), reverse=True)[:n]

    def save_to_file(self, filename="courses.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [c.to_dict() for c in self._courses], f, ensure_ascii=False, indent=2
            )
        print(f"✅ Курсы сохранены в {filename}")


# ==========================
# 9. ЦЕПОЧКА ОБЯЗАННОСТЕЙ
# ==========================
class Handler(ABC):
    def __init__(self, successor=None):
        self.successor = successor

    @abstractmethod
    def handle_request(self, request):
        pass


class InstructorHandler(Handler):
    def handle_request(self, request):
        if "материалы" in request:
            return "👩‍🏫 Преподаватель одобрил изменения материалов."
        elif self.successor:
            return self.successor.handle_request(request)


class MethodologyDepartmentHandler(Handler):
    def handle_request(self, request):
        if "структура" in request:
            return "📘 Методический отдел утвердил изменения структуры курса."
        elif self.successor:
            return self.successor.handle_request(request)


class ManagementHandler(Handler):
    def handle_request(self, request):
        return "🏛 Руководство платформы одобрило любые изменения."


# ==========================
# 10. МЕНЮ (CLI)
# ==========================
def main_menu():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[logging.FileHandler("platform.log"), logging.StreamHandler()],
    )

    platform = Platform("EduPro", Address("Москва", "Ленинградский пр.", "10А"))

    while True:
        print("\n=== МЕНЮ ПЛАТФОРМЫ ===")
        print("1. Добавить курс")
        print("2. Показать все курсы")
        print("3. Удалить курс")
        print("4. Топ-3 курса по студентам")
        print("5. Сохранить курсы")
        print("6. Одобрение изменений (цепочка)")
        print("7. Выйти")

        choice = input("Выберите пункт: ")

        if choice == "1":
            ctype = input("Тип курса (programming/design/science): ").lower()
            title = input("Название: ")
            instructor = input("Преподаватель: ")
            students = input("Студенты через запятую: ").split(",")
            topics = input("Темы через запятую: ").split(",")
            start = date.fromisoformat(input("Дата начала (YYYY-MM-DD): "))
            end = date.fromisoformat(input("Дата окончания (YYYY-MM-DD): "))

            extra = None
            if ctype == "programming":
                extra = input("Языки программирования: ").split(",")
            elif ctype == "design":
                extra = input("Инструменты: ").split(",")
            elif ctype == "science":
                extra = input("Область науки: ")

            if ctype == "programming":
                course = ProgrammingCourse(
                    title, start, end, instructor, students, topics, extra
                )
            elif ctype == "design":
                course = DesignCourse(
                    title, start, end, instructor, students, topics, extra
                )
            else:
                course = ScienceCourse(
                    title, start, end, instructor, students, topics, extra
                )

            platform.add_course(course)
            print("✅ Курс добавлен!")

        elif choice == "2":
            for c in platform.get_courses():
                print("-", c)

        elif choice == "3":
            title = input("Введите название курса для удаления: ")
            platform.remove_course(title)
            print("🗑 Курс удалён (если существовал).")

        elif choice == "4":
            for c in platform.get_top_courses():
                print(f"{c} — студентов: {len(c.students)}")

        elif choice == "5":
            platform.save_to_file()

        elif choice == "6":
            request = input("Введите запрос на изменение: ")
            chain = InstructorHandler(MethodologyDepartmentHandler(ManagementHandler()))
            print(chain.handle_request(request))

        elif choice == "7":
            print("👋 Выход из программы.")
            break
        else:
            print("❌ Неверный выбор.")


# ==========================
# 11. ЗАПУСК
# ==========================
if __name__ == "__main__":
    main_menu()
