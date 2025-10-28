import logging


class LoggingMixin:
    def log_action(self, message: str):
        logging.info(f"[LOG] {message}")


class NotificationMixin:
    def notify_students(self, message: str):
        for student in self.students:
            logging.info(f"Уведомление для {student}: {message}")
