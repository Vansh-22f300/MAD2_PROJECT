from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
from passlib.hash import bcrypt
from backend.models import db,User
from backend.api import (User_Login,
                         AddSubject,
                         User_Signup,
                         AddChapter,
                         AddQuiz,
                         AddQuestion,
                         Export_Details
                         )
from backend.config import cache
from backend.worker import *

from backend.task import *
def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.LocalConfig')
    db.init_app(app)
    cache.init_app(app)
    return app


def admin_setup():
    admin = User.query.filter_by(Is_admin=True).first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@gmail.com',
            password=bcrypt.hash('admin'),
            dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            full_name='Admin User',
            Is_admin=True,
            qualification='Admin'
        )
        db.session.add(admin)
        db.session.commit()
        
app = create_app()        
api = Api(app)
CORS(app)
jwt = JWTManager(app)
with app.app_context():
    celery= celery_init_app(app)
    # Initialize the database
    celery.conf.beat_schedule = CeleryConfig.beat_schedule
    db.create_all()
    admin_setup()

    
@app.get('/')
def index():
    return "Welcome to the Quiz Management System API!"

@app.get('/test')
@cache.cached(timeout=60)  # Cache for 60 seconds

def test():
    return {'Time':str(datetime.now())}

api.add_resource(User_Login, '/login')
api.add_resource(AddSubject,'/add_subject/get', '/add_subject/post')
api.add_resource(User_Signup, '/signup')
api.add_resource(AddChapter, '/add_chapter/get', '/add_chapter/<int:subject_id>', '/edit_chapter/<int:chapter_id>','/delete_chapter/<int:chapter_id>')
api.add_resource(AddQuiz,  '/add_quiz/<int:chapter_id>', '/edit_quiz/<int:quiz_id>', '/delete_quiz/<int:quiz_id>')
api.add_resource(AddQuestion, '/add_question/get', '/add_question/<int:quiz_id>/post', '/edit_question/<int:question_id>', '/delete_question/<int:question_id>')
api.add_resource(Export_Details, '/export_details')

if __name__ == '__main__':
    app.run(debug=True)