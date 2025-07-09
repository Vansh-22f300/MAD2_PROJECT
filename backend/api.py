from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token,get_jwt,verify_jwt_in_request

from backend.models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime
from passlib.hash import bcrypt
from backend.task import *
class User_Login(Resource):
    def post(self):
        data = request.get_json()
        user= User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': 'User Does not Exist'}, 401
        if user and bcrypt.verify(data['password'], user.password):
            access_token = create_access_token(identity=user.username, additional_claims={'user_id': user.id})
            
            if user.Is_admin:
                return {'message': 'Admin Login successful', 
                        'access_token': access_token, 
                        # 'Is_admin': True,
                        'user_id':user.id, 
                        'username': user.username}, 200
            else:
                return {'message': 'User Login successful', 
                        'access_token': access_token, 
                        # 'Is_admin': False,
                        'user_id':user.id, 
                        'username': user.username}, 200    
                
        else:
            return {'message': 'Invalid username or password'}, 401
        

class User_Signup(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=bcrypt.hash(data['password']),
            dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            full_name=data['full_name'],
            gender = data['gender'],
            phone = data['phone'],
            address = data['address'],
            qualification=data.get('qualification', '')
            
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {'message': 'User registered successfully'}, 200
        
class AddSubject(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
            
        
        subjects = Subject.query.all()
        sub_json = []
        for subject in subjects:
            chapters=Chapter.query.filter_by(subject_id=subject.id).all()
            chapter_json = []
            for chapter in chapters:
                chapter_json.append({
                    'id': chapter.id,
                    'name': chapter.name,
                    'description': chapter.description
                })
            sub_json.append({
                'id': subject.id,
                'name': subject.name,
                'code': subject.code,
                'credits': subject.credits,
                'description': subject.description,
                'chapters': chapter_json
            })
        return sub_json, 200
    
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        subject = Subject(
            name=data['name'],
            code=data['code'],
            credits=data['credits'],
            description=data.get('description', '')
        )
        db.session.add(subject)
        db.session.commit()
        
        return {'message': 'Subject added successfully'}, 200
    
    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        subject = Subject.query.filter_by(id=data['id']).first()
        if not subject:
            return {'message': 'Subject not found'}, 404
        
        subject.name = data['name']
        subject.code = data['code']
        subject.credits = data['credits']
        subject.description = data.get('description', '')
        db.session.commit()
        return {'message': 'Subject updated successfully'}, 200       
    
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        subject = Subject.query.filter_by(id=data['id']).first()
        if not subject:
            return {'message': 'Subject not found'}, 404
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Subject deleted successfully'}, 200      
    
    
class AddChapter(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
            
        chapters = Chapter.query.all()
        chapter_json = []
        for chapter in chapters:
            chapter_json.append({
                'id': chapter.id,
                'name': chapter.name,
                'description': chapter.description,
                'subject_id': chapter.subject_id
            })
        return chapter_json, 200
    
    @jwt_required()
    def post(self, subject_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        subject_id=Subject.query.filter_by(id=subject_id).first()
        chapter = Chapter(
            name=data['name'],
            description=data.get('description', ''),
            subject_id=subject_id.id
        )
        db.session.add(chapter)
        db.session.commit()
        return {'message': 'Chapter added successfully'}, 200    
    
    
    
    @jwt_required()
    def put(self, chapter_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        
        chapter.name = data['name']
        chapter.description = data.get('description', '')
        db.session.commit()
        return {'message': 'Chapter updated successfully'}, 200
    
    
    @jwt_required()
    def delete(self, chapter_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        db.session.delete(chapter)
        db.session.commit()
        return {'message': 'Chapter deleted successfully'}, 200
    
    
class AddQuiz(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
            
        quizzes = Quiz.query.all()
        quiz_json = []
        for quiz in quizzes:
            attempts=None
            if quiz.single_attempt:
                attempts= Score.query.filter_by(quiz_id=quiz.id).count()
                if attempts is not None and attempts > 0:
                    quiz.is_active = False
            quiz_json.append({
                'id': quiz.id,
                'title': quiz.title,
                'description': quiz.description,
                'chapter_id': quiz.chapter_id,
                'Is_active': quiz.is_active,
                'date': quiz.date.strftime('%Y-%m-%d'),
                'time_limit': str(quiz.time_limit),
                'single_attempt': quiz.single_attempt,
                'chapter_name': quiz.chapter.name,
                'subject_name': quiz.chapter.subject.name 
                
            })
        return quiz_json, 200

    @jwt_required()
    def post(self, chapter_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        chapter=Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        
        quiz = Quiz(
            title=data['title'],
            description=data.get('description', ''),
            chapter_id=chapter.id,
            Is_active=data.get('Is_active', True),
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            time_limit=datetime.strptime(data['time_limit'], '%H:%M:%S').time(),
            single_attempt=data.get('single_attempt')
        )
        db.session.add(quiz)
        db.session.commit()
        return {'message': 'Quiz added successfully'}, 200
    
    
    
    @jwt_required()
    def put(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        
        quiz.title = data['title']
        quiz.description = data.get('description', '')
        quiz.chapter_id = data['chapter_id']
        quiz.Is_active = data.get('Is_active', True)
        quiz.date = datetime.strptime(data['date'], '%Y-%m-%d')
        quiz.time_limit = datetime.strptime(data['time_limit'], '%H:%M:%S').time()
        quiz.single_attempt = data.get('single_attempt')
        
        db.session.commit()
        return {'message': 'Quiz updated successfully'}, 200   
    
    @jwt_required()
    def delete(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        
        db.session.delete(quiz)
        db.session.commit()
        return {'message': 'Quiz deleted successfully'}, 200
    
class AddQuestion(Resource):
    @jwt_required()
    def get(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
            
        questions = Question.query.all()
        question_json = []
        for question in questions:
            question_json.append({
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'option_1': question.option_1,
                'option_2': question.option_2,
                'option_3': question.option_3,
                'option_4': question.option_4,
                'correct_answer': question.correct_answer
                # 'quiz_id': question.quiz_id,
                # 'chapter_id': question.chapter_id
            })
        return question_json, 200
    
    @jwt_required()
    def post(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        chapter_id= Quiz.query.filter_by(id=quiz_id).first().chapter_id
        
        question = Question(
            question_text=data['question_text'],
            question_type=data['question_type'],
            option_1=data['option_1'],
            option_2=data['option_2'],
            option_3=data['option_3'],
            option_4=data['option_4'],
            correct_answer=data['correct_answer'],
            quiz_id=quiz_id,
            chapter_id=chapter_id
        )
        
        db.session.add(question)
        db.session.commit()
        return {'message': 'Question added successfully'}, 200
    
    @jwt_required()
    def put(self, question_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message': 'Question not found'}, 404
        
        question.question_text = data['question_text']
        question.question_type = data['question_type']
        question.option_1 = data['option_1']
        question.option_2 = data['option_2']
        question.option_3 = data['option_3']
        question.option_4 = data['option_4']
        question.correct_answer = data['correct_answer']
        
        db.session.commit()
        return {'message': 'Question updated successfully'}, 200
    
    @jwt_required()
    def delete(self, question_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message': 'Question not found'}, 404
        
        db.session.delete(question)
        db.session.commit()
        return {'message': 'Question deleted successfully'}, 200
    
class Export_Details(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user== 'admin':
            return {'message': 'Only Users can access this resource'}, 401
        claims = get_jwt()
        user_id = claims['user_id']
        user=User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        export_scores.apply_async(args=[user_id])
        return {'message': 'Export started successfully'}, 200