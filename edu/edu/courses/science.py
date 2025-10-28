from edu.course import Course
from edu.interfaces import Teachable, Assessable


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
