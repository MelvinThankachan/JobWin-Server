from django.core.mail import EmailMultiAlternatives
from server.settings import FROM_EMAIL, OTP_EXPIRATION_TIME
from datetime import datetime


def get_otp_email_body(otp):
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Static Template</title>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link
      href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap"
      rel="stylesheet"
    />
  </head>
  <body
    style="
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: #ffffff;
      font-size: 14px;
    "
  >
    <div
      style="
        max-width: 680px;
        margin: 0 auto;
        padding: 45px 30px 60px;
        background: #e5eefa;
        background-image: url(https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661497957196_595865/email-template-background-banner);
        background-repeat: no-repeat;
        background-size: 800px 452px;
        background-position: top center;
        font-size: 14px;
        color: #434343;
      "
    >
      <header>
        <table style="width: 100%;">
          <tbody>
            <tr style="height: 0;">
              <td>
              </td>
              <td style="text-align: right;">
                <span
                  style="font-size: 16px; line-height: 30px; color: #ffffff;"
                  >{datetime.now().strftime("%Y-%m-%d")}</span
                >
              </td>
            </tr>
          </tbody>
        </table>
      </header>

      <main>
        <div
          style="
            margin: 0;
            margin-top: 70px;
            padding: 92px 30px 115px;
            background: #ffffff;
            border-radius: 10px;
            text-align: center;
          "
        >
          <div style="width: 100%; max-width: 489px; margin: 0 auto;">
            <h1
              style="
                margin: 0;
                font-size: 24px;
                font-weight: 500;
                color: #1f1f1f;
              "
            >
              Your OTP
            </h1>
            <p
              style="
                margin: 0;
                margin-top: 17px;
                font-weight: 400;
                letter-spacing: 0.56px;
              "
            >
              Thank you for choosing <span style="font-size:18px; font-weight: 600; color: #1f1f1f;">JobWin</span>. Use the following OTP
              to complete the procedure to verify your email address.
            </p>
            <p
              style="
                margin: 0;
                margin-top: 60px;
                font-size: 30px;
                font-weight: 600;
                letter-spacing: 5px;
                color: #2976d7;
                background: #f6f9fd;
                padding: 10px;
                border-radius: 10px;
              "
            >{otp}</p>
            <p
              style="
                margin: 0;
                margin-top: 60px;
                font-weight: 400;
                letter-spacing: 0.56px;
              "
            >
              OTP is
              valid for
              <span style="font-size:18px; font-weight: 600; color: #1f1f1f;">{OTP_EXPIRATION_TIME} minutes</span>.
              Do not share this code with others, including JobWin
              employees.
            </p>
          </div>
        </div>

        <p
          style="
            max-width: 400px;
            margin: 0 auto;
            margin-top: 90px;
            text-align: center;
            font-weight: 500;
            color: #434343;
          "
        >
          Need help? Ask at
          <a
            href="#"
            style="color: #499fb6; text-decoration: none;"
            >JobWin@gmail.com</a
          >
          <br/>
          or visit our
          <a
            href="#"
            target="_blank"
            style="color: #499fb6; text-decoration: none;"
            >Help Center</a
          >
        </p>
      </main>

      <footer
        style="
          width: 100%;
          max-width: 490px;
          margin: 20px auto 0;
          text-align: center;
          border-top: 1px solid #e6ebf1;
        "
      >
        <p
          style="
            margin: 0;
            margin-top: 40px;
            font-size: 16px;
            font-weight: 600;
            color: #2976d7;
          "
        >
          JobWin
        </p>
        <p style="margin: 0; margin-top: 8px; color: #434343;">
          Job portal
        </p>
        <div style="margin: 0; margin-top: 16px;">
          <a href="" target="_blank" style="display: inline-block;">
            <img
              width="36px"
              alt="Facebook"
              src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661502815169_682499/email-template-icon-facebook"
            />
          </a>
          <a
            href=""
            target="_blank"
            style="display: inline-block; margin-left: 8px;"
          >
            <img
              width="36px"
              alt="Instagram"
              src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661504218208_684135/email-template-icon-instagram"
          /></a>
          <a
            href=""
            target="_blank"
            style="display: inline-block; margin-left: 8px;"
          >
            <img
              width="36px"
              alt="Twitter"
              src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503043040_372004/email-template-icon-twitter"
            />
          </a>
          <a
            href=""
            target="_blank"
            style="display: inline-block; margin-left: 8px;"
          >
            <img
              width="36px"
              alt="Youtube"
              src="https://archisketch-resources.s3.ap-northeast-2.amazonaws.com/vrstyler/1661503195931_210869/email-template-icon-youtube"
          /></a>
        </div>
        <p style="margin: 0; margin-top: 16px; color: #434343;">
          Copyright © 2025 Company. All rights reserved.
        </p>
      </footer>
    </div>
  </body>
</html>
"""


def send_otp(email, otp):
    try:
        subject = "JobWin - OTP Verification"
        text_content = (
            f"Your OTP is: {otp}. This OTP is valid for {OTP_EXPIRATION_TIME} minutes."
        )
        html_content = get_otp_email_body(otp)
        email_message = EmailMultiAlternatives(
            subject, text_content, FROM_EMAIL, [email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send(fail_silently=False)
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_user_object(user):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
    }
