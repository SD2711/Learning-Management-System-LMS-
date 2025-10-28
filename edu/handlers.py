from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self, successor=None):
        self.successor = successor

    @abstractmethod
    def handle_request(self, request: str):
        pass


class InstructorHandler(Handler):
    def handle_request(self, request: str):
        if "материалы" in request:
            return " Преподаватель одобрил изменения материалов."
        elif self.successor:
            return self.successor.handle_request(request)


class MethodologyDepartmentHandler(Handler):
    def handle_request(self, request: str):
        if "структура" in request:
            return " Методический отдел утвердил изменения структуры курса."
        elif self.successor:
            return self.successor.handle_request(request)


class ManagementHandler(Handler):
    def handle_request(self, request: str):
        return " Руководство платформы одобрило любые изменения."
