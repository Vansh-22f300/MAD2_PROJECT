import os
from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
from passlib.hash import bcrypt
from backend.models import db, User
from backend.api import (
    User_Login, AddSubject, User_Signup, AddChapter, AddQuiz,
    AddQuestion, Export_Details, Start_Quiz, User_Results,
    Admin_Summary, Admin_Users, Admin_Profile, User_Profile
)
from app import bcrypt

from backend.config import cache
from dotenv import load_dotenv
load_dotenv()
from flask_mail import Mail, Message
mail=Mail()
def create_app():
    app = Flask(__name__, static_folder="frontend/dist", template_folder="frontend/dist")
    
    # Load config
    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object("backend.config.ProductionConfig")
    else:
        app.config.from_object("backend.config.LocalConfig")

    # Ensure DB URI is set from .env (Neon or SQLite fallback)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"  # fallback for local dev
    
    # Mail setup
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_EMAIL")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    mail.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    return app
def admin_setup():
    admin = User.query.filter_by(Is_admin=True).first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@gmail.com',
            password=bcrypt.generate_password_hash('vm123').decode('utf-8'),
            dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            full_name='Admin User',
            Is_admin=True,
            gender='Male',
            phone='1234567890',
            address='123 Admin St, Admin City, Admin Country',
            status='Active',
            qualification='Admin'
        )
        db.session.add(admin)
        db.session.commit()

app = create_app()
api = Api(app)
CORS(app)
jwt = JWTManager(app)

with app.app_context():
    # celery = celery_init_app(app)  # optional
    db.create_all()
    admin_setup()
@app.route("/send-test-email")
def send_test_email():
    try:
        msg = Message("Hello from Flask",
                      recipients=["your_friend_email@example.com"])
        msg.body = "This is a test email sent from Flask using SMTP."
        mail.send(msg)
        return "✅ Test email sent successfully!"
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

# API routes
api.add_resource(User_Login, '/login')
api.add_resource(AddSubject,'/add_subject/get', '/add_subject/post','/edit_subject/<int:sub_id>','/delete_subject/<int:sub_id>')
api.add_resource(User_Signup, '/signup')
api.add_resource(AddChapter, '/add_chapter/get', '/add_chapter/<int:subject_id>', '/edit_chapter/<int:chapter_id>','/delete_chapter/<int:chapter_id>','/get_chapters')
api.add_resource(AddQuiz,  '/add_quiz', '/edit_quiz/<int:quiz_id>', '/delete_quiz/<int:quiz_id>','/get_quiz')
api.add_resource(AddQuestion,'/add_question/<int:quiz_id>', '/edit_question/<int:question_id>', '/delete_question/<int:question_id>','/get_questions/<int:quiz_id>')
api.add_resource(Export_Details, '/export_details')
api.add_resource(Start_Quiz, '/start_quiz/<int:quiz_id>')
api.add_resource(User_Results, '/user_results')
api.add_resource(Admin_Summary, '/admin_summary')
api.add_resource(Admin_Users, '/admin_users')
api.add_resource(Admin_Profile, '/admin/profile')
api.add_resource(User_Profile, '/user/profile')

# Catch-all route to serve Vue
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")
    
 
    
if __name__ == "__main__":
    app.run(debug=True)