from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Mentor(db.Model, SerializerMixin):
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    expertise = db.Column(db.String) 
    image = db.Column(db.String, default="")
    
    cohorts = db.relationship('Cohort', back_populates='mentor', cascade='all, delete-orphan')
    
    serialize_only = ('id', 'name', 'expertise', 'image', 'students')
    serialize_rules = ('-cohorts',)

    @property
    def students(self):
        """Automatically calculate student count"""
        return len({cohort.student_id for cohort in self.cohorts})

    def __repr__(self):
        return f'<Mentor {self.id}, {self.name}>'

class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    course = db.Column(db.String)  
    
    cohorts = db.relationship('Cohort', back_populates='student', cascade='all, delete-orphan')
    
    serialize_rules = ('-cohorts.student',)

    def __repr__(self):
        return f'<Student {self.id}, {self.name}>'

class Cohort(db.Model, SerializerMixin):
    __tablename__ = 'cohorts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    mentor = db.relationship('Mentor', back_populates='cohorts')
    student = db.relationship('Student', back_populates='cohorts')
    
    serialize_rules = ('-mentor.cohorts', '-student.cohorts')

    def __repr__(self):
        return f'<Cohort {self.id}, {self.name}>, {self.mentor_id}, {self.student_id}'