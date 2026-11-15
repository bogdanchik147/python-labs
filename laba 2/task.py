from dataclasses import dataclass, field
from typing import Dict, List, Optional
from statistics import mean



class FacultyError(Exception):
    pass

class AddToCourseError(FacultyError):
    pass

class SemesterError(FacultyError):
    pass

class StudentNotFoundError(FacultyError):
    pass

class GradeError(FacultyError):
    pass

class DisciplineNotFoundError(FacultyError):
    pass






@dataclass
class Discipline:
    discipline_id: str
    name: str
    department_name: str
    specialties: Dict[str, List[int]]
    students: Dict[str, Optional[int]] = field(default_factory=dict)

    def is_available_for(self, specialty, semester):
        return semester in self.specialties.get(specialty, [])

    def add_student(self, student):
        if not self.is_available_for(student.specialty, student.semester):
            raise AddToCourseError(
                f"Предмет {self.name} недоступен для специальности "
                f"{student.specialty} в {student.semester}-м семестре"
            )
        if student.student_id in self.students:
            raise AddToCourseError("Студент уже записан на этот предмет")
        self.students[student.student_id] = None

    def set_grade(self, student_id, grade):
        if student_id not in self.students:
            raise AddToCourseError("Студент не записан на этот предмет")
        if not isinstance(grade, int) or not 1 <= grade <= 10:
            raise GradeError("Оценка должна быть целым числом от 1 до 10")
        self.students[student_id] = grade






@dataclass
class Department:
    name: str
    disciplines: Dict[str, Discipline] = field(default_factory=dict)

    def add_discipline(self, discipline):
        self.disciplines[discipline.discipline_id] = discipline




@dataclass
class Student:
    student_id: str
    full_name: str
    specialty: str
    semester: int = 1
    disciplines: List[str] = field(default_factory=list)






@dataclass
class Faculty:
    name: str
    departments: Dict[str, Department] = field(default_factory=dict)
    students: Dict[str, Student] = field(default_factory=dict)
    expelled_students: Dict[str, dict] = field(default_factory=dict)
    disciplines: Dict[str, Discipline] = field(default_factory=dict)
    specialties: List[str] = field(default_factory=list)

    def add_department(self, department):
        self.departments[department.name] = department

    def add_discipline(self, discipline):
        if discipline.department_name not in self.departments:
            raise FacultyError("Сначала добавьте кафедру этой дисциплины")
        if discipline.discipline_id in self.disciplines:
            raise FacultyError("Дисциплина с таким ID уже существует")
        self.disciplines[discipline.discipline_id] = discipline
        self.departments[discipline.department_name].add_discipline(discipline)

    def save_registry(self):
        lines = ["Файл СТУДЕНТОВ", "=" * 60]

        for student in self.students.values():
            lines.extend([
                "",
                "Статус: ОБУЧАЕТСЯ",
                f"ID: {student.student_id}",
                f"ФИО: {student.full_name}",
                f"Специальность: {student.specialty}",
                f"Семестр: {student.semester}",
                "Предметы:"
            ])
            if not student.disciplines:
                lines.append("  Нет записанных предметов")
            for discipline_id in student.disciplines:
                discipline = self.disciplines[discipline_id]
                grade = discipline.students.get(student.student_id)
                grade_text = str(grade) if grade is not None else "не выставлена"
                lines.append(f"  {discipline.name} — оценка: {grade_text}")

        for record in self.expelled_students.values():
            lines.extend([
                "",
                "Статус: ОТЧИСЛЕН",
                f"ID: {record['student_id']}",
                f"ФИО: {record['full_name']}",
                f"Специальность: {record['specialty']}",
                f"Семестр: {record['semester']}",
                f"Причина отчисления: {record['reason']}",
                "Предметы и оценки:"
            ])
            for subject, grade in record["grades"]:
                lines.append(f"  {subject} — оценка: {grade}")

        with open("students_registry.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")

    def addtocourse_student(self, student_id, full_name, specialty, semester=1):
        if student_id in self.students or student_id in self.expelled_students:
            raise FacultyError("Студент с таким ID уже существует")
        if specialty not in self.specialties:
            raise FacultyError("Неизвестная специальность: " + ", ".join(self.specialties))
        if semester < 1:
            raise SemesterError("Номер семестра должен быть положительным")
        student = Student(student_id, full_name, specialty, semester)
        self.students[student_id] = student
        self.save_registry()
        return student

    def get_student(self, student_id):
        student = self.students.get(student_id)
        if student is None:
            raise StudentNotFoundError(f"Студент с ID {student_id} не найден")
        return student

    def expel_student(self, student_id, reason="Отчислен по решению администрации"):
        student = self.get_student(student_id)
        grades = []
        for discipline_id in student.disciplines:
            discipline = self.disciplines[discipline_id]
            grade = discipline.students.get(student_id)
            grades.append((discipline.name, grade if grade is not None else "не выставлена"))
            discipline.students.pop(student_id, None)

        self.expelled_students[student_id] = {
            "student_id": student.student_id,
            "full_name": student.full_name,
            "specialty": student.specialty,
            "semester": student.semester,
            "reason": reason,
            "grades": grades
        }
        del self.students[student_id]
        self.save_registry()

    def add_student_to_discipline(self, student_id, discipline_id):
        student = self.get_student(student_id)
        discipline = self.disciplines.get(discipline_id)
        if discipline is None:
            raise DisciplineNotFoundError(f"Предмет с ID {discipline_id} не найден")
        #один язык английский или немецкий
        language_ids = {"S3", "S4"}
        if discipline_id in language_ids and any(
            course_id in language_ids for course_id in student.disciplines
        ):
            raise AddToCourseError("Можно выбрать только один иностранный язык: английский или немецкий")
        discipline.add_student(student)
        student.disciplines.append(discipline_id)
        self.save_registry()

    def remove_student_from_discipline(self, student_id, discipline_id):
        student = self.get_student(student_id)
        discipline = self.disciplines.get(discipline_id)
        if discipline is None:
            raise DisciplineNotFoundError(f"Предмет с ID {discipline_id} не найден")
        if discipline_id not in student.disciplines:
            raise AddToCourseError("Студент не записан на этот предмет")
        discipline.students.pop(student_id, None)
        student.disciplines.remove(discipline_id)
        self.save_registry()

    def set_student_grade(self, student_id, discipline_id, grade):
        self.get_student(student_id)
        discipline = self.disciplines.get(discipline_id)
        if discipline is None:
            raise DisciplineNotFoundError(f"Предмет с ID {discipline_id} не найден")
        discipline.set_grade(student_id, grade)
        if grade < 4:
            self.expel_student(
                student_id,
                f"Автоматическое отчисление: оценка {grade} по предмету {discipline.name}"
            )
            return True
        self.save_registry()
        return False

    def move_to_next_semester(self, student_id):
        student = self.get_student(student_id)
        if not student.disciplines:
            raise SemesterError("У студента нет предметов в текущем семестре")

        for discipline_id in student.disciplines:
            discipline = self.disciplines[discipline_id]
            grade = discipline.students.get(student_id)
            if grade is None:
                raise SemesterError(f"По предмету {discipline.name} еще нет оценки")
            if grade < 4:

                self.expel_student(student_id, f"Неудовлетворительная оценка {grade}")
                return

        for discipline_id in student.disciplines:
            self.disciplines[discipline_id].students.pop(student_id, None)
        student.disciplines.clear()
        student.semester += 1
        self.save_registry()

    def student_report(self, student_id):
        student = self.get_student(student_id)
        lines = [
            f"Ведомость студента: {student.full_name}",
            f"ID: {student.student_id}",
            f"Факультет: {self.name}",
            f"Специальность: {student.specialty}",
            f"Семестр: {student.semester}",
            "",
            "Предметы:"
        ]
        grades = []
        for discipline_id in student.disciplines:
            discipline = self.disciplines[discipline_id]
            grade = discipline.students.get(student_id)
            grade_text = str(grade) if grade is not None else "не выставлена"
            lines.append(f"{discipline.name} | кафедра: {discipline.department_name} | оценка: {grade_text}")
            if grade is not None:
                grades.append(grade)

        lines.append(f"\nСредний балл: {mean(grades):.2f}" if grades else "\nСредний балл: нет оценок")
        report = "\n".join(lines)
        filename = f"vedomost_student_{student_id}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)
        return report, filename

    def discipline_report(self, discipline_id):
        discipline = self.disciplines.get(discipline_id)
        if discipline is None:
            raise DisciplineNotFoundError(f"Предмет с ID {discipline_id} не найден.")

        completed = []
        for student_id, grade in discipline.students.items():
            student = self.students.get(student_id)
            if student and grade is not None:
                completed.append((student, grade))

        grades = [grade for _, grade in completed]
        average = f"{mean(grades):.2f}" if grades else "нет оценок"
        lines = [
            f"Ведомость по предмету: {discipline.name}",
            f"Кафедра: {discipline.department_name}",
            f"Средний балл: {average}",
            "",
            "Студенты с выставленными оценками:"
        ]
        for student, grade in completed:
            lines.append(f"{student.student_id} | {student.full_name} | {student.specialty} | оценка: {grade}")

        report = "\n".join(lines)
        filename = f"vedomost_discipline_{discipline_id}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)
        return report, filename

def My_faculty():
    faculty = Faculty(
        "Факультет информационных технологий",
         specialties=["КБ", "ПИ", "РФ", "ИНТЭЛ"]
    )

    departments = [
        "Кафедра программирования",
        "Кафедра математики",
        "Кафедра радиотехники",
        "Кафедра иностранных языков"
        ]
    for name in departments:
        faculty.add_department(Department(name))


    all_it = ["КБ", "ПИ", "ИНТЭЛ"]
    all_specialties = ["КБ", "ПИ", "РФ", "ИНТЭЛ"]
    courses = [
        ("S1", "Программирование на Java", "Кафедра программирования", ["ПИ", "ИНТЭЛ"]),
        ("S2", "Программирование на Python", "Кафедра программирования", ["КБ", "ПИ", "ИНТЭЛ"]),
        ("S3", "Английский язык", "Кафедра иностранных языков", all_specialties),
        ("S4", "Немецкий язык", "Кафедра иностранных языков", all_specialties),
        ("S5", "Дискретная математика", "Кафедра математики", ["КБ", "ПИ", "ИНТЭЛ"]),
        ("S6", "Базы данных", "Кафедра программирования", ["КБ", "ПИ", "ИНТЭЛ"]),
        ("S7", "Численные методы", "Кафедра математики", ["ПИ", "РФ", "ИНТЭЛ"]),
        ("S8", "Основы радиоэлектроники", "Кафедра радиотехники", ["РФ", "ИНТЭЛ", "КБ"]),
        ("S9", "Математический анализ", "Кафедра математики", all_specialties),
        ("S10", "ТВиМС", "Кафедра математики", ["ПИ", "РФ", "ИНТЭЛ"])
    ]

    for course_id, name, department, specialties in courses:
        faculty.add_discipline(Discipline(
            course_id, name, department,
            {specialty: [1, 2, 3, 4, 5, 6, 7, 8] for specialty in specialties}
        ))
    faculty.save_registry()
    return faculty


def show_disciplines(faculty, specialty=None, semester=None):
    print("\nДоступные предметы:")
    for discipline in faculty.disciplines.values():
        if specialty and not discipline.is_available_for(specialty, semester):
            continue
        print(f"  {discipline.discipline_id} — {discipline.name} "
              f"| кафедра: {discipline.department_name}")


def show_students(faculty):
    print("\nСписок студентов:")
    if not faculty.students:
        print("Студентов пока нет.")
    for student in faculty.students.values():
        print(f"{student.student_id} | {student.full_name} | "
              f"{student.specialty} | семестр {student.semester}")
    if faculty.expelled_students:
        print("\nОтчисленные студенты:")
        for record in faculty.expelled_students.values():
            print(f"{record['student_id']} | {record['full_name']} | ОТЧИСЛЕН")


def print_menu():
    print("""
==================================
1. Зачислить студента
2. Отчислить студента
3. Записать студента на предмет
4. Удалить студента с предмета
5. Выставить оценку
6. Перевести на следующий семестр
7. Ведомость студента
8. Ведомость предмета
9. Показать студентов
10. Показать предметы
0. Выход
===================================
""")


def main():
    faculty = My_faculty()
    print("Специальности:", ", ".join(faculty.specialties))

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                student_id = input("ID студента: ").strip()
                full_name = input("ФИО студента: ").strip()
                print("Специальности:", ", ".join(faculty.specialties))
                specialty = input("Специальность: ").strip().upper()
                semester_text = input("Семестр (по умолчанию 1): ").strip()
                semester = int(semester_text) if semester_text else 1
                student = faculty.addtocourse_student(student_id, full_name, specialty, semester)
                print(f"Студент {student.full_name} зачислен. Данные записаны в students_registry.txt")

            elif choice in {"2", "3", "4", "5", "6", "7"}:
                student_id = input("ID студента: ").strip()
                student = faculty.get_student(student_id)

                if choice == "2":
                    faculty.expel_student(student_id)
                    print("Студент отчислен. Запись сохранена")

                elif choice == "3":
                    show_disciplines(faculty, student.specialty, student.semester)
                    discipline_id = input("ID предмета: ").strip().upper()
                    faculty.add_student_to_discipline(student_id, discipline_id)
                    print("Студент записан на предмет")

                elif choice == "4":
                    discipline_id = input("ID предмета: ").strip().upper()
                    faculty.remove_student_from_discipline(student_id, discipline_id)
                    print("Студент удален с предмета")

                elif choice == "5":
                    discipline_id = input("ID предмета: ").strip().upper()
                    grade = int(input("Оценка (1–10): ").strip())
                    expelled = faculty.set_student_grade(student_id, discipline_id, grade)
                    if expelled:
                        print("Оценка ниже 4. Студент автоматически ОТЧИСЛЕН")
                    else:
                        print("Оценка сохранена.")

                elif choice == "6":
                    faculty.move_to_next_semester(student_id)
                    print(f"Студент переведен в {student.semester}-й семестр")

                elif choice == "7":
                    report, filename = faculty.student_report(student_id)
                    print(report)
                    print(f"\nВедомость сохранена в файл: {filename}")

            elif choice == "8":
                show_disciplines(faculty)
                discipline_id = input("ID предмета: ").strip().upper()
                report, filename = faculty.discipline_report(discipline_id)
                print(report)
                print(f"\nВедомость сохранена в файл: {filename}")

            elif choice == "9":
                show_students(faculty)

            elif choice == "10":
                show_disciplines(faculty)

            elif choice == "0":
                print("Работа программы завершена")
                break

            else:
                print("Выберите пункт меню от 0 до 10")

        except ValueError:
            print("Ошибка: введите корректное числовое значение")
        except FacultyError as error:
            print("Ошибка:", error)
        except OSError as error:
            print("Ошибка при работе с файлом:", error)

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()