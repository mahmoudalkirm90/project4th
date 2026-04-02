import smtplib
import ssl
from email.message import EmailMessage
import socket

def send_email(receiver_email, otp_code):

    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "afiete2026@gmail.com"
    sender_password = "nmmsuchwtfunhwhy" # eco password not real for security
    subject = "Welcome to Afiete"
    is_html=False
    body = f"""Hello,

I hope you are doing well.

I would like to request a One-Time Password {otp_code} to complete my account verification process.
Please send the OTP to this email address or provide guidance on how I can receive it.

Thank you for your assistance.

Best regards,
Afiete Team"""
    try:
        # إنشاء الرسالة
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        print(len(sender_password))

        if is_html:
            msg.add_alternative(body, subtype='html')
        else:
            msg.set_content(body)

        # إنشاء اتصال آمن
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(smtp_server, port, timeout=10) as server:
                server.starttls(context=context)

                try:
                    server.login(sender_email, sender_password)
                except smtplib.SMTPAuthenticationError as e:
                    # print("❌ خطأ في تسجيل الدخول: تحقق من الإيميل أو كلمة المرور")
                    # print(e)
                    return False

                try:
                    server.send_message(msg)
                    # print("✅ تم إرسال الإيميل بنجاح")
                    return True

                except smtplib.SMTPRecipientsRefused:
                    # print("❌ الإيميل المستلم مرفوض")
                    return False
                except smtplib.SMTPException as e:
                    # print(f"❌ خطأ أثناء الإرسال: {e}")
                    return False
                return False

        except smtplib.SMTPConnectError:
            # print("❌ فشل الاتصال بالسيرفر")
            return False
        except smtplib.SMTPServerDisconnected:
            # print("❌ السيرفر قطع الاتصال")
            return False    
        except socket.gaierror:
            #   print("❌ خطأ في DNS أو اسم السيرفر غير صحيح")
            return False
        except TimeoutError:
            # print("❌ انته ت مهلة الاتصال (Timeout)")
                return False
        return False

    except Exception as e:
        # print(f"❌ خطأ غير متوقع: {e}")
        return False
    