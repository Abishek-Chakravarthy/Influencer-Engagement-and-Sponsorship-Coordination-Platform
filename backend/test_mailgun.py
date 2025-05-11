# test_mailgun.py
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object('config.Config')
mail = Mail(app)

def send_mail():
    print("mail sending started")
    msg = Message(
        'Hello',
        sender=app.config['MAIL_USERNAME'],
        recipients=['rccy2601@gmail.com']  # Replace with your email address
    )
    msg.body = 'This is a test email sent from Flask using Mailgun.'
    print("message formed")
    try:
        mail.send(msg)
        print("Mail sent successfully!")
    except Exception as e:
        print("Failed to send mail: ", str(e))

if __name__ == '__main__':
    with app.app_context():
        send_mail()
    print("Done")
