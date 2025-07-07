from celery import shared_task
from datetime import datetime
from backend.models import db, User, Subject, Chapter, Quiz, Question, Score
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

import csv
import os
import smtplib
from email import encoders
from jinja2 import Template
def mail_config(to_address, subject,email_message,attachments=None):
    smtp_server_host= 'localhost'
    smtp_server_port= 1025
    sender_email= 'admin@gmail.com'
    
    msg= MIMEMultipart()
    msg['From']= sender_email
    msg['To']= to_address
    msg['Subject']= subject
    msg.attach(MIMEText(email_message, 'html'))
    if attachments:
        if os.path.exists(attachments):
            with open(attachments, 'rb') as file:
                part = MIMEBase('text', 'csv')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachments)}')
                msg.attach(part)
        else:
            print(f"Attachment {attachments} does not exist.")
            
    with smtplib.SMTP(smtp_server_host, smtp_server_port) as server:
        server.sendmail(sender_email, to_address, msg.as_string())
    print(f"Email sent to {to_address} with subject '{subject}'")
    
@shared_task
def daily_reminder():
    users = User.query.all()
    quizzes = Quiz.query.all()
    for user in users:
        if user.Is_admin:
            continue
        
        unattempted_quizzes = []
        for quiz in quizzes:
            attempt= Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()
            if not attempt:
                unattempted_quizzes.append(quiz)
        if unattempted_quizzes:
            html_body=build_html_email(user.username, unattempted_quizzes)
            mail_config(user.email, 'Reminder:Complete Your Quizzes', html_body)
         
def build_html_email(username, unattempted_quizzes):
    html_body=f'<p>Hello {username},</p>'
    html_body += '<p>You have the following quizzes that you have not attempted yet:</p>'
    html_body += '<ul>'
    for quiz in unattempted_quizzes:
        html_body += f'<li>{quiz.title} - {quiz.description} (Chapter: {quiz.chapter.name})</li>'
    html_body += '</ul>'
    html_body += '<p>Please log in to the system and complete these quizzes at your earliest convenience.</p>'
    html_body += '<p>Best regards,<br>Quiz Management System</p>'
    return html_body

@shared_task
def export_scores(user_id):
    try:
        reports_dir=os.path.join(os.getcwd(),'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        report_file = os.path.join(reports_dir, f'scores_report_{user_id}_quiz_reports_{datetime.now().strftime("%Y%m%d")}.csv')   

        with open(report_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username','Quiz ID','Quiz Title', 'Marks Obtained', 'Total Marks','Date Attempted'])
            quizzes=db.session.query(
                User.username,
                Quiz.id,
                Quiz.title,
                Score.marks_obtained.label('Marks Obtained'),
                Score.total_marks.label('Total Marks'),
                Score.date_taken.label('Date Attempted')
            ).join(Score,Score.quiz_id == Quiz.id).filter(Score.user.id == user_id).all()

            for quiz in quizzes:
                quiz_id, username, title, marks_obtained, total_marks, date_taken = quiz
                writer.writerow([
                    username, quiz_id, title, marks_obtained, total_marks,date_taken.strftime('%Y-%m-%d')if date_taken else 'N/A'
                    ])  
        
        user= User.query.get(id=user_id).first()
        mail_config(
            user.email, 
            'Your Quiz Scores Report', 
            'Please find attached your quiz scores report.', 
            attachments=report_file
        )
    except Exception as e:
        print(e)
    
def send_email(user, month, quiz_details, total_quizzes, avg_percentage):
    template_path="templates/report.html"
    with open(template_path, 'r') as template_file:
        template_file=template_file.read()
    template=Template(template_file)
    html_content=template.render(
        username=user.username,
        month=month,
        quiz_details=quiz_details,
        total_quizzes=total_quizzes,
        avg_percentage=avg_percentage
    )
    mail_config(
        user.email, 
        f'Monthly Report for {user.username} - {month}', 
        html_content
    )    
        
@shared_task
def send_monthly_report():
    users = User.query.filter_by(Is_admin=True).all()
    for user in users:
        month= datetime.now().strftime('%B')
        quiz_details=Score.query.filter_by(user_id=user.id).all()
        total_quizzes = len(quiz_details)
        if total_quizzes >0:
            avg_percentage=sum(score.percentage for score in quiz_details) / total_quizzes
        else:
            avg_percentage = 0.0
        send_email(user,month,quiz_details,total_quizzes,avg_percentage)    