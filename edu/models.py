import json


class Address:
    def __init__(self, city, street, building):
        self.city, self.street, self.building = city, street, building

    def __str__(self):
        return f"{self.city}, {self.street}, {self.building}"


class Platform:
    def __init__(self, name, address: Address):
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
