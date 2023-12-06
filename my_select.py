from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Score, Subject

engine = create_engine('sqlite:///./mydatabase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def select_1():
    return session.query(Student.name, func.avg(Score.value).label('average')) \
        .join(Score, Student.id == Score.student_id) \
        .group_by(Student.name) \
        .order_by(func.avg(Score.value).desc()) \
        .limit(5) \
        .all()

def select_2(subject_name):
    return session.query(Student.name, func.avg(Score.value).label('average')) \
        .join(Score, Student.id == Score.student_id) \
        .join(Subject, Score.subject_id == Subject.id) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.name) \
        .order_by(func.avg(Score.value).desc()) \
        .first()

def select_3(subject_name):
    return session.query(Student.name, func.avg(Score.value).label('average')) \
        .join(Score, Student.id == Score.student_id) \
        .join(Subject, Score.subject_id == Subject.id) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.name) \
        .all()

def select_4():
    return session.query(func.avg(Score.value).label('average')) \
        .scalar()

# Додайте інші функції select, які вам потрібні

if __name__ == "__main__":
    result_1 = select_1()
    print("Top 5 students with the highest average scores:")
    for student in result_1:
        print(f"{student.name}: {student.average}")

    result_2 = select_2("Subject 1")
    print("\nStudent with the highest average score in Subject 1:")
    print(f"{result_2.name}: {result_2.average}")

    result_3 = select_3("Subject 1")
    print("\nAverage scores for students in Subject 1:")
    for student in result_3:
        print(f"{student.name}: {student.average}")

    result_4 = select_4()
    print("\nOverall average score across all subjects:")
    print(f"{result_4}")
