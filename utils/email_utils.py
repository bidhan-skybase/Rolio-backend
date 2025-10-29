import os
from brevo_python import Configuration, ApiClient, TransactionalEmailsApi
from brevo_python.models import SendSmtpEmail
from brevo_python.rest import ApiException
from pydantic import EmailStr

def send_mail(to: EmailStr, otp: int):
    configuration = Configuration()
    configuration.api_key['api-key'] = os.getenv("ROLIO_MAIL")
    print(os.getenv("ROLIO_MAIL"))

    api_instance = TransactionalEmailsApi(ApiClient(configuration))

    subject = "Your Rolio OTP Code"
    html_content = f"""
        <div style="font-family: Arial, sans-serif; color: #333;">
            <h2>🔐 Rolio Email Verification</h2>
            <p>Hello,</p>
            <p>Your one-time password (OTP) is:</p>
            <h1 style="letter-spacing: 2px; color: #007bff;">{otp}</h1>
            <p>This OTP will expire in <strong>5 minutes</strong>. Please do not share it with anyone.</p>
        </div>
    """

    send_smtp_email = SendSmtpEmail(
        to=[{"email": to}],
        sender={"name": "Rolio", "email": "marasinebidhan@gmail.com"}, 
        subject=subject,
        html_content=html_content
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        return {"status": "success", "message_id": response.message_id}
    except ApiException as e:
        return {"status": "error", "message": str(e)}