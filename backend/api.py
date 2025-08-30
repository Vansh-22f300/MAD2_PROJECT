from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token,get_jwt,verify_jwt_in_request

from backend.models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime
from passlib.hash import bcrypt
from backend.task import *
from backend.config import cache 

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
    def put(self,sub_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        subject = Subject.query.get(sub_id)
        if not subject:
            return {'message': 'Subject not found'}, 404
        
        subject.name = data['name']
        subject.code = data['code']
        subject.credits = data['credits']
        subject.description = data.get('description', '')
        db.session.commit()
        return {'message': 'Subject updated successfully'}, 200       
    
    @jwt_required()
    def delete(self, sub_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403

        subject = Subject.query.get(sub_id)
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
        
        claims=get_jwt()
        user_id=claims['user_id']    
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
                'Is_active': quiz.Is_active,
                'date': quiz.date.strftime('%Y-%m-%d'),
                'time_limit': quiz.time_limit.strftime('%H:%M:%S'),
                'single_attempt': quiz.single_attempt,
                'chapter_name': quiz.chapter.name,
                'subject_name': quiz.chapter.subject.name 
                
            })
        return quiz_json, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        chapter=Chapter.query.filter_by(id=data['chapter_id']).first()
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
        print(f"Received data for PUT /edit_quiz/{quiz_id}: {data}") # Keep this for debugging!
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        if 'title' in data:
            quiz.title = data['title']
        if 'description' in data:
            quiz.description = data['description']
        if 'chapter_id' in data:
            quiz.chapter_id = data['chapter_id']
        
        if 'Is_active' in data:
            if isinstance(data['Is_active'], str): 
                quiz.Is_active = data['Is_active'].lower() == 'true'
            else: 
                quiz.Is_active = bool(data['Is_active'])
        
        if 'date' in data:
            try:
                quiz.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return {'message': 'Invalid date format. Expected YYYY-MM-DD'}, 400

        if 'time_limit' in data:
            try:
                quiz.time_limit = datetime.strptime(data['time_limit'], '%H:%M:%S').time()
            except ValueError:
                return {'message': 'Invalid time limit format. Expected HH:MM:SS'}, 400
        
        if 'single_attempt' in data:
            if isinstance(data['single_attempt'], str):
                quiz.single_attempt = data['single_attempt'].lower() == 'true'
            else: 
                quiz.single_attempt = bool(data['single_attempt'])
        
        
        try:
            db.session.commit()
            return {'message': 'Quiz updated successfully'}, 200
        except Exception as e:
            db.session.rollback() 
            print(f"Error updating quiz: {e}")
            return {'message': 'Failed to update quiz', 'error': str(e)}, 500   
    
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
        if current_user != 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403

        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        question_json = []
        for question in questions:
            question_json.append({
                'id': question.id,
                'question_tag': question.question_tag,
                'question_state': question.question_state,
                'option_1': question.option_1,
                'option_2': question.option_2,
                'option_3': question.option_3,
                'option_4': question.option_4,
                'correct_answer': question.correct_answer
            })

        return {
            'quiz': {
                'id': quiz.id,
                'title': quiz.title,
                'chapter_id': quiz.chapter_id
            },
            'questions': question_json
        }, 200
    
    @jwt_required()
    def post(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403
        
        data = request.get_json()
        chapter_id= Quiz.query.filter_by(id=quiz_id).first().chapter_id
        
        question = Question(
            question_tag=data['question_tag'],
            question_state=data['question_state'],
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

        question.question_tag = data['question_tag']
        question.question_state = data['question_state']
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
    
class Start_Quiz(Resource):
    @jwt_required()
    def get(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            return {'message': 'Only Users can access this resource'}, 401
        
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        if not questions:
            return {'message': 'Empty quiz, no questions available'}, 404
            
        time_limit = quiz.time_limit.hour * 3600 + quiz.time_limit.minute * 60 + quiz.time_limit.second
        
        quiz_data = {
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'chapter': quiz.chapter.name,
            'time_limit': time_limit,
            'questions': [
                {
                    'id': question.id,
                    'question_state': question.question_state,
                    'option_1': question.option_1,
                    'option_2': question.option_2,
                    'option_3': question.option_3,
                    'option_4': question.option_4,
                    # For security, correct_answer is not included here
                } for question in questions
            ]
        }
        return quiz_data, 200

    @jwt_required()
    def post(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            return {'message': 'Only Users can access this resource'}, 401
        
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404
            
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        data = request.get_json()
        
        score = 0
        total_possible_marks = len(questions)
        
        if not data.get('answers'):
            return {'message': 'No answers submitted'}, 400

        user_answers = data.get('answers', {})
        for question in questions:
            user_answer = user_answers.get(str(question.id))
            if user_answer:
                correct_answer_text = getattr(question, question.correct_answer)
                if user_answer.strip().lower() == correct_answer_text.strip().lower():
                    score += 1
        
        percentage = (score / total_possible_marks) * 100 if total_possible_marks > 0 else 0
        grade = 'Excellent' if percentage >= 75 else 'Improve'
        timestamp = datetime.now()
        
        new_score = Score(
            user_id=user_id,
            subject_id=subject.id,
            chapter_id=chapter.id,
            quiz_id=quiz_id,
            score=score,
            date_taken=timestamp,
            percentage=round(percentage, 2),
            grade=grade,
            total_possible_marks=total_possible_marks
        )
        
        db.session.add(new_score)
        db.session.commit()
        
       
        questions_with_answers = [
            {
                'id': q.id,
                'question_state': q.question_state,
                'options': [q.option_1, q.option_2, q.option_3, q.option_4],
                'correct_answer': q.correct_answer
            } for q in questions
        ]

        return {
            'message': 'Quiz Attempted successfully',
            'score': score,
            'total_possible_marks': total_possible_marks,
            'percentage': percentage,
            'questions': questions_with_answers
        }, 200

class User_Results(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            return {'message': 'Only Users can access this resource'}, 401
        
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        scores = Score.query.filter_by(user_id=user_id).all()
        result = []
        for score in scores:
            result.append({
                'subject_name': score.subject.name,
                'chapter_name': score.chapter.name,
                'quiz_title': score.quiz.title,
                'date_taken': score.date_taken.strftime('%Y-%m-%d %H:%M:%S'),
                'score': score.score,
                'total_possible_marks': score.total_possible_marks,
                'percentage': score.percentage,
                'grade': score.grade
            })
        return result, 200
    
class Admin_Summary(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return {'message': 'Access forbidden: Admins only'}, 401

        
        # 🚀 Pie Chart Data: Subject-wise attempts
        subject_attempts = db.session.query(
            Subject.name,
            db.func.count(Score.id)
        ).join(Quiz, Score.quiz_id == Quiz.id
        ).join(Chapter, Quiz.chapter_id == Chapter.id
        ).join(Subject, Chapter.subject_id == Subject.id
        ).group_by(Subject.name
        ).all()
        
        pie_labels = [row[0] for row in subject_attempts]
        pie_data = [row[1] for row in subject_attempts]

        top_score = db.session.query(
            Subject.name,
            db.func.max(Score.score)
        ).join(Quiz, Score.quiz_id == Quiz.id
        ).join(Chapter, Quiz.chapter_id == Chapter.id
        ).join(Subject, Chapter.subject_id == Subject.id
        ).group_by(Subject.name
        ).all()
        
        bar_labels = [row[0] for row in top_score]
        bar_data = [row[1] for row in top_score]

       
        result = {
            'pie_labels': pie_labels,
            'pie_data': pie_data,
            'bar_labels': bar_labels,
            'bar_data': bar_data
        }


        return result, 200      
class Admin_Users(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user!= 'admin':
            return {'message': 'Access forbidden: Admins only'}, 401
        users=User.query.filter_by(Is_admin=False).all()
        user_json=[]
        for user in users:
            user_json.append({
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'full_name':user.full_name,
                'dob':user.dob.strftime('%Y-%m-%d'),
                'gender':user.gender,
                'phone':user.phone,
                'address':user.address,
                # 'status':user.status,
                'qualification':user.qualification
            })        
        return user_json,200    
    
class User_Profile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'username': current_user}, 200  
    
         
class Admin_Profile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        if current_user != 'admin':
            return {'message': 'Access forbidden: Admins only'}, 403

        return {'username': current_user}, 200        
        