from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    dob= db.Column(db.Date, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    Is_admin = db.Column(db.Boolean, default=False)
    qualification = db.Column(db.String(120), nullable=True)
    # profile_picture = db.Column(db.String(200), nullable=True)  # URL or path to profile picture
    
    scores = db.relationship('Score', back_populates='user', cascade='all,delete')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    
    chapters = db.relationship('Chapter', back_populates='subject', cascade='all,delete')
    scores = db.relationship('Score', back_populates='subject', cascade='all,delete')

class Chapter(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), nullable=False)
    description= db.Column(db.String(500), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    # subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))
    
    subject = db.relationship('Subject', back_populates='chapters')
    scores = db.relationship('Score', back_populates='chapter', cascade='all,delete')
    quizzes = db.relationship('Quiz', back_populates='chapter', cascade='all,delete')
    questions = db.relationship('Question', back_populates='chapter', cascade='all,delete')

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    Is_active = db.Column(db.Boolean, default=True)
    date= db.Column(db.DateTime, nullable=False)
    time_limit= db.Column(db.Time, nullable=False)  # Duration in minutes  
    single_attempt = db.Column(db.Boolean, nullable=True)
    
    chapter = db.relationship('Chapter', back_populates='quizzes')
    scores = db.relationship('Score', back_populates='quiz', cascade='all,delete')
    questions = db.relationship('Question', back_populates='quiz', cascade='all,delete')
    
    
class Question(db.Model):    
    id= db.Column(db.Integer, primary_key=True)
    question_text= db.Column(db.Text, nullable=False)
    question_type= db.Column(db.String(500), nullable=False)
    option_1= db.Column(db.String(200), nullable=False)
    option_2= db.Column(db.String(200), nullable=False)
    option_3= db.Column(db.String(200), nullable=False)
    option_4= db.Column(db.String(200), nullable=False)
    correct_answer= db.Column(db.String(200), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    # quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    # chapter = db.relationship('Chapter', backref=db.backref('questions', lazy=True))
    
    chapter = db.relationship('Chapter', back_populates='questions')
    quiz = db.relationship('Quiz', back_populates='questions')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    date_taken = db.Column(db.DateTime, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    
    user = db.relationship('User', back_populates='scores')
    subject = db.relationship('Subject', back_populates='scores')
    chapter = db.relationship('Chapter', back_populates='scores')
    quiz = db.relationship('Quiz', back_populates='scores')