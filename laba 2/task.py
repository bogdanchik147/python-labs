from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Discipline:
    discipline_id: str
    name: str
    department_name: str
    specialties: Dict[str, List[int]]
    students: Dict[str, Optional[int]] = field(default_factory=dict)

@dataclass
class Department:
    name: str
    disciplines: Dict[str, Discipline] = field(default_factory=dict)

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



