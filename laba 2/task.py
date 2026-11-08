from dataclasses import dataclass, field
from typing import Dict, List, Optional

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
                f"Предмет «{self.name}» недоступен для специальности "
                f"{student.specialty} в {student.semester}-м семестре"
            )
        if student.student_id in self.students:
            raise AddToCourseError("Студент уже записан на этот предмет")
        self.students[student.student_id] = None

    def set_grade(self, student_id, grade):
        if student_id not in self.students:
            raise AddToCourseError("Студент не записан на этот предмет.")
        if not isinstance(grade, int) or not 1 <= grade <= 10:
            raise GradeError("Оценка должна быть целым числом от 1 до 10.")
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
            raise FacultyError("Сначала добавьте кафедру этой дисциплины.")
        if discipline.discipline_id in self.disciplines:
            raise FacultyError("Дисциплина с таким ID уже существует.")
        self.disciplines[discipline.discipline_id] = discipline
        self.departments[discipline.department_name].add_discipline(discipline)

    def addtocourse_student(self, student_id, full_name, specialty, semester=1):
        if student_id in self.students or student_id in self.expelled_students:
            raise FacultyError("Студент с таким ID уже существует.")
        if specialty not in self.specialties:
            raise FacultyError("Неизвестная специальность: " + ", ".join(self.specialties))
        if semester < 1:
            raise SemesterError("Номер семестра должен быть положительным.")
        student = Student(student_id, full_name, specialty, semester)
        self.students[student_id] = student
        return student

    def get_student(self, student_id):
        student = self.students.get(student_id)
        if student is None:
            raise StudentNotFoundError(f"Студент с ID {student_id} не найден.")
        return student

    def add_student_to_discipline(self, student_id, discipline_id):
        student = self.get_student(student_id)
        discipline = self.disciplines.get(discipline_id)
        if discipline is None:
            raise DisciplineNotFoundError(f"Предмет с ID {discipline_id} не найден.")
        # Иностранный язык выбирается один: английский ИЛИ немецкий.
        language_ids = {"D03", "D04"}
        if discipline_id in language_ids and any(
                course_id in language_ids for course_id in student.disciplines
        ):
            raise AddToCourseError("Можно выбрать только один иностранный язык: английский или немецкий.")
        discipline.add_student(student)
        student.disciplines.append(discipline_id)
        self.save_registry()

    def remove_student_from_discipline(self, student_id, discipline_id):
        student = self.get_student(student_id)
        discipline = self.disciplines.get(discipline_id)
        if discipline is None:
            raise DisciplineNotFoundError(f"Предмет с ID {discipline_id} не найден.")
        if discipline_id not in student.disciplines:
            raise AddToCourseError("Студент не записан на этот предмет.")
        discipline.students.pop(student_id, None)
        student.disciplines.remove(discipline_id)
        self.save_registry()

    def set_student_grade(self, student_id, discipline_id, grade):
        self.get_student(student_id)
        discipline = self.disciplines.get(discipline_id)
        if discipline is None:
            raise DisciplineNotFoundError(f"Предмет с ID {discipline_id} не найден.")
        discipline.set_grade(student_id, grade)



