from edu.course import Course
from edu.interfaces import Teachable, Assessable


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
