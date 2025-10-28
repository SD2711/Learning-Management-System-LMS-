from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from .exceptions import InvalidDateError
from .mixins import LoggingMixin, NotificationMixin
from .meta import CourseMeta


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
    def topics(self):
        return self._topics

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
