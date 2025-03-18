
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []  # Список закрепленных курсов

class Student:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.finished_courses = []  # Завершенные курсы
        self.courses_in_progress = []  # Курсы в процессе изучения
        self.grades = {}  # Оценки за домашние задания

    def rate_lecturer(self, lecturer, course, grade):
        # Проверяем, что лектор является объектом класса Lecturer,
        # курс привязан к лектору, и студент изучает этот курс
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        # Вычисление средней оценки за домашние задания
        total_grades = 0
        count = 0
        for grades in self.grades.values():
            total_grades += sum(grades)
            count += len(grades)
        return total_grades / count if count > 0 else 0

    def __str__(self):
        # Строковое представление студента
        avg_grade = self.average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else 'Нет'
        finished_courses = ', '.join(self.finished_courses) if self.finished_courses else 'Нет'
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade:.2f}\n'
                f'Курсы в процессе изучения: {courses_in_progress}\n'
                f'Завершенные курсы: {finished_courses}')


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        # Проверяем, что студент является объектом класса Student,
        # курс привязан к проверяющему, и студент изучает этот курс
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
    def __str__(self):
        # Строковое представление рецензента
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # Оценки за лекции

    def average_grade(self):
        # Вычисление средней оценки за лекции
        total_grades = 0
        count = 0
        for grades in self.grades.values():
            total_grades += sum(grades)
            count += len(grades)
        return total_grades / count if count > 0 else 0

    def __str__(self):
        # Строковое представление лектора
        avg_grade = self.average_grade()
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg_grade:.2f}')
class Assessment:
    """Метод оценки на равно или меньше с проверкой вхождения в класс Assessment"""
    def __init__(self, value):
        if not isinstance(value, float):
            raise AttributeError('значение не входит в класс Assessment')
        self.value = value
    @classmethod
    def __verifi_data(cls, other):
        if not isinstance(other, Assessment):
            raise AttributeError('значение не входит в класс Assessment')
        return other.value


    def __eq__(self, other):
        return self.value == other.__verifi_data(other)

    def __lt__(self, other):
        return self.value < other.__verifi_data(other)
# Пример использования
student_1= Student('Иосиф', 'Джугашвили')
student_1.courses_in_progress += ['Python', 'Git']
student_1.finished_courses += ['Введение в программирование']
student_2 = Student('Володя', 'Ульянов')
student_2.courses_in_progress += ['Python', 'Git']
student_2.finished_courses += ['Введение в программирование']

lecturer_1= Lecturer('Александр', 'Герцен')
lecturer_1.courses_attached += ['Python']
lecturer_2= Lecturer('Николай', 'Огарев')
lecturer_2.courses_attached += ['Git']

reviewer_1 = Reviewer('Павел', 'Пестель')
reviewer_1.courses_attached += ['Python']
reviewer_2 = Reviewer('Николай', 'Чернышевский')
reviewer_2.courses_attached += ['Git']

# Проверяющий выставляет оценку студенту
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_2.rate_hw(student_1, 'Git', 8)

reviewer_1.rate_hw(student_2, 'Python', 9)
reviewer_2.rate_hw(student_2, 'Git', 8)

# Студент выставляет оценку лектору
student_1.rate_lecturer(lecturer_1, 'Python', 10)
student_2.rate_lecturer(lecturer_1, 'Python', 9)
student_1.rate_lecturer(lecturer_2, 'Git', 8)
student_2.rate_lecturer(lecturer_2, 'Git', 8)




# Вывод информации
print("Рецензенты:")
print(reviewer_1)
print()
print(reviewer_2)
print('_______________________________________________________________')
print('Лекторы:')
print(lecturer_1)
print()
print(lecturer_2)
print('_______________________________________________________________')
print('Студенты:')
print(student_1)
print()
print(student_2)
print('_______________________________________________________________')
# лучший студент

first_student = Assessment(student_1.average_grade())
second_student = Assessment(student_2.average_grade())

if first_student == second_student:
    print (f'У студентов: {student_1.name} {student_1.surname} и {student_2.name} {student_2.surname} одинаковая средняя оценка')
elif first_student < second_student:
    print(f'Лучший студент: {student_2.name} {student_2.surname}')
else:
    print(f'Лучший студент: {student_1.name} {student_1.surname}')
print()
# лучший лектор
first_lecturer = Assessment(lecturer_1.average_grade())
second_lecturer = Assessment(lecturer_2.average_grade())
if first_lecturer == second_lecturer:
    print (f'У лекторов: {lecturer_1.name} {lecturer_1.surname} и {lecturer_2.name} {lecturer_2.surname} одинаковая средняя оценка')
elif first_lecturer < second_lecturer:
    print(f'Лучший лектор: {lecturer_2.name} {lecturer_2.surname}')
else:
    print(f'Лучший лектор: {lecturer_1.name} {lecturer_1.surname}')
