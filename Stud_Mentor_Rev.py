# Импорт декоратора для автоматической генерации методов сравнения
from functools import total_ordering


class Student:
    def __init__(self, name, surname, gender):
        # Основные атрибуты студента
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []  # Завершенные курсы
        self.courses_in_progress = []  # Текущие курсы
        self.grades = {}  # Словарь оценок формата {курс: [оценки]}

    def rate_lecturer(self, lecturer, course, grade):
        """Метод для оценки лекторов студентами"""
        # Проверка корректности данных
        if (isinstance(lecturer, Lecturer)  # объект - лектор
                and course in lecturer.courses_attached  # курс прикреплен к лектору
                and course in self.courses_in_progress  # студент проходит курс
                and 1 <= grade <= 10):  # оценка в допустимом диапазоне

            # Добавление оценки в словарь лектора
            if course in lecturer.lectures_grades:
                lecturer.lectures_grades[course].append(grade)
            else:
                lecturer.lectures_grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_hw_grade(self):
        """Расчет средней оценки за домашние задания"""
        total = 0
        count = 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return round(total / count, 1) if count else 0  # Защита от деления на ноль

    def __str__(self):
        """Магический метод для строкового представления студента"""
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (
            f"Имя: {self.name}\nФамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self.average_hw_grade()}\n"
            f"Курсы в процессе изучения: {courses_in_progress}\n"
            f"Завершенные курсы: {finished_courses}"
        )

    # Методы сравнения студентов по средней оценке
    def __eq__(self, other):
        if not isinstance(other, Student):
            raise TypeError("Можно сравнивать только студентов")
        return self.average_hw_grade() == other.average_hw_grade()

    def __lt__(self, other):
        if not isinstance(other, Student):
            raise TypeError("Можно сравнивать только студентов")
        return self.average_hw_grade() < other.average_hw_grade()


class Mentor:
    """Базовый класс для преподавателей"""

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []  # Курсы, закрепленные за преподавателем

    def __str__(self):
        """Базовое строковое представление"""
        return f"Имя: {self.name}\nФамилия: {self.surname}"


@total_ordering  # Автоматически генерирует другие операторы сравнения
class Lecturer(Mentor):
    """Класс лекторов с функционалом оценки их работы"""

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lectures_grades = {}  # Оценки за лекции {курс: [оценки]}

    def average_lecture_grade(self):
        """Расчет средней оценки за лекции"""
        total = 0
        count = 0
        for grades in self.lectures_grades.values():
            total += sum(grades)
            count += len(grades)
        return round(total / count, 1) if count else 0

    def __str__(self):
        """Строковое представление с средней оценкой"""
        return super().__str__() + f"\nСредняя оценка за лекции: {self.average_lecture_grade()}"

    # Методы сравнения лекторов
    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            raise TypeError("Можно сравнивать только лекторов")
        return self.average_lecture_grade() == other.average_lecture_grade()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            raise TypeError("Можно сравнивать только лекторов")
        return self.average_lecture_grade() < other.average_lecture_grade()


class Reviewer(Mentor):
    """Класс проверяющих с функционалом оценки студентов"""

    def rate_hw(self, student, course, grade):
        """Метод оценки домашних работ"""
        # Проверка условий:
        if (isinstance(student, Student)  # объект - студент
                and course in self.courses_attached  # курс прикреплен к проверяющему
                and course in student.courses_in_progress):  # студент проходит курс

            # Добавление оценки в словарь студента
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


# Функции для подсчета средних оценок
def calculate_average_hw(students, course):
    """Средняя оценка за ДЗ по курсу среди всех студентов"""
    total = 0
    count = 0
    for student in students:
        if course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    return round(total / count, 1) if count else 0


def calculate_average_lecture(lecturers, course):
    """Средняя оценка за лекции по курсу среди всех лекторов"""
    total = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.lectures_grades:
            total += sum(lecturer.lectures_grades[course])
            count += len(lecturer.lectures_grades[course])
    return round(total / count, 1) if count else 0


# Пример использования классов
if __name__ == "__main__":
    # Создание экземпляров
    student1 = Student('Иосиф', 'Джугашвили', 'муж')
    student1.courses_in_progress = ['Python', 'Git']
    student1.finished_courses = ['Введение в программирование']

    student2 = Student('Володя', 'Ульянов', 'муж')
    student2.courses_in_progress = ['Python', 'Git']
    student2.finished_courses = ['Введение в программирование']

    lecturer1 = Lecturer('Александр', 'Герцен')
    lecturer1.courses_attached += ['Python']

    lecturer2 = Lecturer('Николай', 'Огарев')
    lecturer2.courses_attached += ['Git']

    reviewer1 = Reviewer('Павел', 'Пестель')
    reviewer1.courses_attached += ['Python']

    reviewer2 = Reviewer('Николай', 'Чернышевский')
    reviewer2.courses_attached += ['Git']

    # Выставление оценок
    reviewer1.rate_hw(student1, 'Python', 8)
    reviewer1.rate_hw(student2, 'Python', 9)
    reviewer2.rate_hw(student1, 'Git', 9)
    reviewer2.rate_hw(student2, 'Git', 10)

    student1.rate_lecturer(lecturer1, 'Python', 10)
    student2.rate_lecturer(lecturer1, 'Python', 9)
    student1.rate_lecturer(lecturer2, 'Git', 8)
    student2.rate_lecturer(lecturer2, 'Git', 9)

    # Демонстрация работы методов
    print("=== Проверяющие ===")
    print(reviewer1)
    print("\n", reviewer2)

    print("\n=== Лекторы ===")
    print(lecturer1)
    print("\n", lecturer2)

    print("\n=== Студенты ===")
    print(student1)
    print("\n", student2)


    # Сравнение объектов
    print("\n=== Сравнение объектов ===")
    if lecturer1 == lecturer2:
        print(f'У лекторов: {lecturer1.name} {lecturer1.surname} и {lecturer2.name} {lecturer2.surname} одинаковая средняя оценка')
    elif lecturer1 < lecturer2:
        print(f'Лучший лектор: {lecturer2.name} {lecturer2.surname}')
    else:
        print(f'Лучший лектор: {lecturer1.name} {lecturer1.surname}')

    if student1 == student2:
        print(f'У студентов: {student1.name} {student1.surname} и {student2.name} {student2.surname} одинаковая средняя оценка')
    elif student1 < student2:
        print(f'Лучший студент: {student2.name} {student2.surname}')
    else:
        print(f'Лучший студент: {student1.name} {student1.surname}')

    # Использование функций расчета средних
    students = [student1, student2]
    lecturers = [lecturer1, lecturer2]

    print("\nСредняя оценка за ДЗ по Python:",
          calculate_average_hw(students, 'Python'))
    print("\nСредняя оценка за ДЗ по Git:",
          calculate_average_hw(students, 'Git'))
    print("\nСредняя оценка за лекции по Python:",
          calculate_average_lecture(lecturers, 'Python'))
    print("\nСредняя оценка за лекции по Git:",
          calculate_average_lecture(lecturers, 'Git'))