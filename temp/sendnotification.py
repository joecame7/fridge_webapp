import sqlite3
import smtplib

def get_user_email(user_id=1):
    conn = sqlite3.connect('static/temp/smart_fridge.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM Users WHERE user_id = ?;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0]
    else:
        raise ValueError(f"No user found with user_id {user_id}")

def send_email(receiver_email, subject, message):

    sender_email = "cardiffgroup24@gmail.com"  
    app_password = "lijj pesm ggjt vnsh"       
    
    email_text = f"Subject: {subject}\n\n{message}"
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the SMTP connection
        
        server.login(sender_email, app_password)
        
        server.sendmail(sender_email, receiver_email, email_text)
        print("Email has been sent to " + receiver_email)
    except Exception as e:
        print("An error occurred while sending the email:", e)
        raise
    finally:
        server.quit()

def send_email_to_user(subject, message, user_id=1):

    try:
        send_email(receiver_email, subject, message)
    except Exception as error:
        print("An error occurred in send_email_to_user:", error)


if __name__ == "__main__":

    subject = input("Subject: ")
    message = input("Message: ")
    send_email_to_user(subject, message)
