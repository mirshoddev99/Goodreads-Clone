from goodreads.celery import app
import smtplib

@app.task()
def sending_email(reciever, username):
    sender = 'mirshodpnu22@gmail.com'
    password = 'obypzyiavxjkkddp'
    reciever = f"{reciever}"
    subject = 'Welcome to Goodreads clone'
    body = f""" Hi {username}, Welcome to our web-site enjoy reading books and reviews!!! """

    message = f"""
                    From: Goodreads Admin   {sender}
                    To: {username}   {reciever}
                    Subject: {subject}\n
                    {body}
                """

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender, password)
        print("Logged in...")
        server.sendmail(sender, reciever, message)
        print("Email has been sent!")

    except smtplib.SMTPAuthenticationError:
        print("Failed")



