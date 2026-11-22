import numpy as np


rng = np.random.default_rng(seed=42)


SUBJECTS = ["Математический анализ", "Механика", "Программирование", "ТВиМС", "Английский"]
N_STUDENTS = 22


grades = rng.integers(2, 11, size=(N_STUDENTS, len(SUBJECTS)))
students = [f"Студент-{i+1:02d}" for i in range(N_STUDENTS)]

print("=== ТАБЛИЦА ОЦЕНОК ЗА СЕССИЮ ===\n")
print(f"{'Имя студента':15}" + "".join(f"{s:>18}" for s in SUBJECTS))
print("-" * 105)

for name, row in zip(students, grades):
    print(f"{name:15}" + "".join(f"{g:>18}" for g in row))

student_avg = grades.mean(axis=1)

print("\n=== СРЕДНИЙ БАЛЛ СТУДЕНТОВ ===")
for name, avg in zip(students, student_avg):
    print(f"{name}: {avg:.2f}")

best_idx = int(np.argmax(student_avg))
worst_idx = int(np.argmin(student_avg))

print(f"\nЛучший студент: {students[best_idx]} (средний балл {student_avg[best_idx]:.2f})")
print(f"Худший студент: {students[worst_idx]} (средний балл {student_avg[worst_idx]:.2f})")


subject_avg = grades.mean(axis=0)

print("\n=== СРЕДНИЙ БАЛЛ ПО ПРЕДМЕТАМ ===")
for subj, avg in zip(SUBJECTS, subject_avg):
    print(f"{subj}: {avg:.2f}")

easiest_idx = int(np.argmax(subject_avg))
hardest_idx = int(np.argmin(subject_avg))

print(f"\nСамый простой предмет: {SUBJECTS[easiest_idx]} (средний балл {subject_avg[easiest_idx]:.2f})")
print(f"Самый сложный предмет: {SUBJECTS[hardest_idx]} (средний балл {subject_avg[hardest_idx]:.2f})")


FUND = 100_000


eligible = student_avg >= 4.0
weights = np.where(eligible, student_avg, 0)

if weights.sum() == 0:
    weights = student_avg.copy()

scholarship = FUND * weights / weights.sum()
scholarship = np.round(scholarship, 2)

print(f"\n РАСПРЕДЕЛЕНИЕ СТИПЕНДИИ ({FUND} руб.) ")
for name, s, avg, is_el in zip(students, scholarship, student_avg, eligible):
    status = "" if is_el else " (не проходит по баллу)"
    print(f"{name}: {s:>10.2f} руб. (ср. балл {avg:.2f}){status}")

print(f"\nИтого распределено: {scholarship.sum():.2f} руб.")