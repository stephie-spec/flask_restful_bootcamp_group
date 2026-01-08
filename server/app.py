from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, Mentor, Student, Cohort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to Bootcamp API",
        }
        return make_response(response_dict, 200)

api.add_resource(Home, '/')

class Mentors(Resource):
    def get(self):
        mentors = [m.to_dict() for m in Mentor.query.all()]
        return make_response(mentors, 200)

    def post(self):
        data = request.get_json()
        new_mentor = Mentor(
            name=data['name'],
            expertise=data.get('expertise') 
        )
        db.session.add(new_mentor)
        db.session.commit()
        return make_response(new_mentor.to_dict(), 201)

api.add_resource(Mentors, '/mentors')

class MentorByID(Resource):
    def get(self, id):
        mentor = Mentor.query.filter_by(id=id).first()
        return make_response(mentor.to_dict(), 200)

    def post(self):
        data = request.get_json()
        new_mentor = Mentor(
            name=data['name'],
            expertise=data.get('expertise')
        )
        db.session.add(new_mentor)
        db.session.commit()
        return make_response(new_mentor.to_dict(), 201)

    def patch(self, id):
        mentor = Mentor.query.filter_by(id=id).first()
        
        data = request.get_json()
        for attr in data:
            if hasattr(mentor, attr):
                setattr(mentor, attr, data[attr])
        
        db.session.add(mentor)
        db.session.commit()
        return make_response(mentor.to_dict(), 200)

    def put(self, id):
        mentor = Mentor.query.filter_by(id=id).first()
        
        data = request.get_json()
        
        mentor.name = data['name']
        mentor.expertise = data.get('expertise')  
        
        db.session.add(mentor)
        db.session.commit()
        return make_response(mentor.to_dict(), 200)

    def delete(self, id):
        mentor = Mentor.query.filter_by(id=id).first()
        if not mentor:
            return make_response({"error": "Mentor not found"}, 404)
        
        db.session.delete(mentor)
        db.session.commit()
        return make_response({"message": "Mentor deleted successfully"}, 200)

api.add_resource(MentorByID, '/mentors/<int:id>')

class Students(Resource):
    def get(self):
        students = [s.to_dict() for s in Student.query.all()]
        return make_response(students, 200)

    def post(self):
        data = request.get_json()
        new_student = Student(
            name=data['name'],
            course=data.get('course')  
        )
        db.session.add(new_student)
        db.session.commit()
        return make_response(new_student.to_dict(), 201)

api.add_resource(Students, '/students')

class StudentByID(Resource):
    def get(self, id):
        student = Student.query.filter_by(id=id).first()
        return make_response(student.to_dict(), 200)

    def patch(self, id):
        student = Student.query.filter_by(id=id).first()
        
        data = request.get_json()
        for attr in data:
            if hasattr(student, attr):
                setattr(student, attr, data[attr])
        
        db.session.add(student)
        db.session.commit()
        return make_response(student.to_dict(), 200)

    def put(self, id):
        student = Student.query.filter_by(id=id).first()
        
        data = request.get_json()
        
        student.name = data['name']
        student.course = data.get('course') 
        
        db.session.add(student)
        db.session.commit()
        return make_response(student.to_dict(), 200)

    def delete(self, id):
        student = Student.query.filter_by(id=id).first()
        
        db.session.delete(student)
        db.session.commit()
        return make_response({"message": "Student deleted successfully"}, 200)

api.add_resource(StudentByID, '/students/<int:id>')

class Cohorts(Resource):
    def get(self):
        cohorts = [c.to_dict() for c in Cohort.query.all()]
        return make_response(cohorts, 200)

    def post(self):
        data = request.get_json()
        new_cohort = Cohort(
            name=data['name'],
            mentor_id=data['mentor_id'],
            student_id=data['student_id'],
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )
        db.session.add(new_cohort)
        db.session.commit()
        return make_response(new_cohort.to_dict(), 201)

api.add_resource(Cohorts, '/cohorts')

class CohortByID(Resource):
    def get(self, id):
        cohort = Cohort.query.filter_by(id=id).first()
        return make_response(cohort.to_dict(), 200)

    def patch(self, id):
        cohort = Cohort.query.filter_by(id=id).first()
        
        data = request.get_json()
        for attr in data:
            setattr(cohort, attr, data[attr])
        
        db.session.add(cohort)
        db.session.commit()
        return make_response(cohort.to_dict(), 200)

    def delete(self, id):
        cohort = Cohort.query.filter_by(id=id).first()
        
        db.session.delete(cohort)
        db.session.commit()
        return make_response({"message": "Cohort deleted successfully"}, 200)

api.add_resource(CohortByID, '/cohorts/<int:id>')

class MentorMostStudents(Resource):
    def get(self):
        mentors = Mentor.query.all()
        
        max_students = 0
        mentor_with_most = None
        
        for mentor in mentors:
            student_count = len({cohort.student_id for cohort in mentor.cohorts})
            
            if student_count > max_students:
                max_students = student_count
                mentor_with_most = mentor
            
        return make_response({
            'mentor': mentor_with_most.to_dict(),
            'student_count': max_students
        }, 200)

api.add_resource(MentorMostStudents, '/mentors/most-students')

if __name__ == '__main__':
    app.run(port=5555, debug=True)