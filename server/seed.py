#!/usr/bin/env python3

from datetime import datetime
from app import app
from models import db, Mentor, Cohort, Student

with app.app_context():
    # Clear existing data
    Cohort.query.delete()
    Mentor.query.delete()
    Student.query.delete()
    
    # Create mentors
    mentor1 = Mentor(name='Kimi Raikonnen', expertise='Software Engineering')
    mentor2 = Mentor(name='Michael Schumacher', expertise='Data Science')
    mentor3 = Mentor(name='Lewis Hamilton', expertise='Cybersecurity')
    db.session.add_all([mentor1, mentor2, mentor3])
    db.session.commit()
    
    mentors = Mentor.query.all()
    
    # Create students
    student1 = Student(name='Nico Rosberg')
    student2 = Student(name='Lando Norris')
    student3 = Student(name='Pierre Gasly')
    student4 = Student(name='Max Verstappen')
    student5 = Student(name='George Russell')
    db.session.add_all([student1, student2, student3, student4, student5])
    db.session.commit()
    
    students = Student.query.all()
    
    # Create cohorts
    db.session.add_all([
        Cohort(
            name="Software Engineering", 
            mentor=mentors[0], 
            student=students[0], 
            start_date=datetime(2024, 1, 15), 
            end_date=datetime(2024, 4, 15)
        ),
        Cohort(
            name="Data Science", 
            mentor=mentors[1], 
            student=students[1],
            start_date=datetime(2024, 2, 1), 
            end_date=datetime(2024, 5, 1)
        ),
        Cohort(
            name="Cybersecurity", 
            mentor=mentors[2], 
            student=students[2],
            start_date=datetime(2024, 3, 1), 
            end_date=datetime(2024, 6, 1)
        ),
        Cohort(
            name="Software Engineering", 
            mentor=mentors[0], 
            student=students[3],
            start_date=datetime(2024, 4, 1), 
            end_date=datetime(2024, 7, 1)
        ),
        Cohort(
            name="Software Engineering", 
            mentor=mentors[0], 
            student=students[4],
            start_date=datetime(2024, 4, 1), 
            end_date=datetime(2024, 7, 1)
        )
    ])
    db.session.commit()
    
    cohorts = Cohort.query.all()
    
    print("Seeded:", len(mentors), "mentors,", len(students), "students,", len(cohorts), "cohorts")