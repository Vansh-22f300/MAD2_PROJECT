from celery import shared_task
from datetime import datetime
from backend.models import db, User, Quiz, Score
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
import os, csv, smtplib


# ------------ SMTP Config ------------
SMTP_HOST = os.getenv("MAIL_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("MAIL_PORT", 587))
SMTP_USER = os.getenv("MAIL_EMAIL", "your-email@gmail.com")
SMTP_PASS = os.getenv("MAIL_PASSWORD", "your-app-password")
SENDER_EMAIL = SMTP_USER


# ------------ Mail Utility ------------
def mail_config(to_address, subject, email_message, attachments=None):
    # Get config from the running Flask app
    sender_email = current_app.config['MAIL_DEFAULT_SENDER']
    smtp_host = current_app.config['MAIL_SERVER']
    smtp_port = current_app.config['MAIL_PORT']
    smtp_user = current_app.config['MAIL_USERNAME']
    smtp_pass = current_app.config['MAIL_PASSWORD']

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(email_message, 'html'))

    # ... (rest of the function is the same) ...

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, to_address, msg.as_string())

    print(f"✅ Email sent to {to_address} with subject '{subject}'")



# ------------ Celery Tasks ------------

@shared_task
def daily_reminder():
    users = User.query.filter_by(Is_admin=False).all()
    quizzes = Quiz.query.all()

    for user in users:
        unattempted = []
        for quiz in quizzes:
            attempt = Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()
            if not attempt:
                unattempted.append(quiz)

        if unattempted:
            html_body = build_html_email(user.username, unattempted)
            mail_config(user.email, 'Reminder: Complete Your Quizzes', html_body)


def build_html_email(username, unattempted_quizzes):
    html = f'<p>Hello {username},</p>'
    html += '<p>You have the following unattempted quizzes:</p><ul>'
    for quiz in unattempted_quizzes:
        html += f'<li>{quiz.title} - {quiz.description}</li>'
    html += '</ul><p>Please log in and complete them.</p>'
    return html


@shared_task
def export_scores(user_id):
    try:
        print(f"📊 Export task started for user {user_id}")
        reports_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        report_file = os.path.join(
            reports_dir,
            f'scores_report_{user_id}_{datetime.now().strftime("%Y%m%d")}.csv'
        )

        with open(report_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Quiz Title', 'Score', 'Total', 'Date'])

            quizzes = db.session.query(
                User.username,
                Quiz.title,
                Score.score,
                Score.total_possible_marks,
                Score.date_taken
            ).join(Quiz, Score.quiz_id == Quiz.id).join(User, User.id == Score.user_id) \
             .filter(Score.user_id == user_id).all()

            for row in quizzes:
                username, title, score, total, date = row
                writer.writerow([username, title, score, total, date.strftime('%Y-%m-%d')])

        user = User.query.get(user_id)
        mail_config(user.email, 'Your Quiz Report', 'Attached is your quiz report.', report_file)

    except Exception as e:
        print(f"❌ Error in export_scores: {e}")


def send_email(user, month, quiz_details, total_quizzes, avg_percentage):
    template_path = "templates/report.html"
    with open(template_path, 'r') as f:
        html = Template(f.read()).render(
            username=user.username,
            month=month,
            quiz_details=quiz_details,
            total_quizzes=total_quizzes,
            avg_percentage=avg_percentage
        )
    mail_config(user.email, f'Monthly Report - {month}', html)


@shared_task
def send_monthly_report():
    from sqlalchemy import extract
    print("📅 Monthly report triggered")

    users = User.query.filter_by(Is_admin=False).all()
    now = datetime.now()

    for user in users:
        month = now.strftime('%B')
        quiz_details = Score.query.filter(
            Score.user_id == user.id,
            extract('month', Score.date_taken) == now.month,
            extract('year', Score.date_taken) == now.year
        ).all()

        total = len(quiz_details)
        avg = sum(q.percentage for q in quiz_details) / total if total > 0 else 0.0
        send_email(user, month, quiz_details, total, avg)
