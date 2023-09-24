import pyotp
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from django.contrib import messages

def send_otp(request,email):
  totp = pyotp.TOTP(request.session['otp_secret_key'], interval=60)
  otp=totp.now()

  email=request.POST.get("email")

  subject = "Your OTP Code"
  message = f"Your one-time password (OTP) is: {otp}"
  from_email = 'siyadsavad313@gmail.com'  # Use the same email as in your settings.py
  to_email = email

  msg = MIMEText(message)
  msg["Subject"] = subject
  msg["From"] = from_email
  msg["To"] = to_email


  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, 'uzaa qdox tykx vgyj')  # Use the same password as in your settings.py
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()
        

    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)

    messages.success(request, "OTP sent to your email. Please check your inbox.")

  except Exception as e:
        messages.error(request, f"Failed to send OTP: {str(e)}")



def resend_otp(request):
    email = request.session['email']
    totp = pyotp.TOTP(request.session['otp_secret_key'], interval=120)
    otp = totp.now()

    subject = "Your OTP Code"
    message = f"Your one-time password (OTP) is: {otp}"
    from_email = 'siyadsavad313@gmail.com'
    to_email = email

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, 'uzaa qdox tykx vgyj')
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()

        valid_date = datetime.now() + timedelta(minutes=1)
        request.session['otp_valid_date'] = str(valid_date)

        messages.success(request, "OTP sent to your email. Please check your inbox.")

    except Exception as e:
        messages.error(request, f"Failed to send OTP: {str(e)}")

