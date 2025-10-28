from abc import ABCMeta


class CourseMeta(ABCMeta):
    """Метакласс, регистрирующий все подклассы Course."""

    registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # Не регистрируем сам базовый класс Course
        if name != "Course":
            CourseMeta.registry[name.lower()] = cls
        return cls
