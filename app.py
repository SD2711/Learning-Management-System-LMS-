import logging
from datetime import date

from edu.models import Address, Platform
from edu.handlers import (
    InstructorHandler,
    MethodologyDepartmentHandler,
    ManagementHandler,
)
from edu.courses import ProgrammingCourse, DesignCourse, ScienceCourse


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
            students = [
                s.strip()
                for s in input("Студенты через запятую: ").split(",")
                if s.strip()
            ]
            topics = [
                t.strip() for t in input("Темы через запятую: ").split(",") if t.strip()
            ]
            start = date.fromisoformat(input("Дата начала (YYYY-MM-DD): "))
            end = date.fromisoformat(input("Дата окончания (YYYY-MM-DD): "))

            if ctype == "programming":
                extra = [
                    x.strip()
                    for x in input("Языки программирования: ").split(",")
                    if x.strip()
                ]
                course = ProgrammingCourse(
                    title, start, end, instructor, students, topics, extra
                )
            elif ctype == "design":
                extra = [
                    x.strip() for x in input("Инструменты: ").split(",") if x.strip()
                ]
                course = DesignCourse(
                    title, start, end, instructor, students, topics, extra
                )
            elif ctype == "science":
                extra = input("Область науки: ").strip()
                course = ScienceCourse(
                    title, start, end, instructor, students, topics, extra
                )
            else:
                print(" Неизвестный тип курса.")
                continue

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
            print(" Выход из программы.")
            break
        else:
            print(" Неверный выбор.")


if __name__ == "__main__":
    main_menu()
