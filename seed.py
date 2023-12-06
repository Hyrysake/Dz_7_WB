from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Base, Student, Group, Teacher, Subject, Score
from datetime import datetime, timedelta
import random

fake = Faker()
engine = create_engine('sqlite:///./mydatabase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def seed_database():
    # Create tables
    Base.metadata.create_all(engine)

    # Seed Groups
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)

    # Seed Teachers
    teachers = [Teacher(name=f"Teacher {i}") for i in range(1, 6)]
    session.add_all(teachers)

    # Seed Subjects
    subjects = [Subject(name=f"Subject {i}", teacher=random.choice(teachers)) for i in range(1, 9)]
    session.add_all(subjects)

    # Commit changes to insert data
    session.commit()

    # Seed Students
    students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(30)]
    session.add_all(students)

    # Seed Scores
    for student in students:
        for subject in subjects:
            for _ in range(4):
                score_date = datetime.utcnow() - timedelta(days=random.randint(1, 365))
                score = Score(value=random.uniform(60, 100), date=score_date, student=student, subject=subject)
                session.add(score)

    # Commit changes to insert data
    session.commit()


if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully.")
