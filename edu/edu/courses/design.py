from edu.course import Course
from edu.interfaces import Teachable, Assessable


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
