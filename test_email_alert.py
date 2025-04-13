import smtplib
from email.message import EmailMessage

sender ="sakshina23@gmail.com"
password ="dbjqigotpsrwfpaz"
    # ✅ Your 16-char App Password
recipient ="31240817@vupune.ac.in"  # ✅ Recipient

msg = EmailMessage()
msg['Subject'] = "Test Email from OceanGuard"
msg['From'] = sender
msg['To'] = recipient
msg.set_content("This is a test email from your OceanGuard system.")

try:
    print("📤 Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        print("🔐 Login successful.")
        smtp.send_message(msg)
        print("✅ Test email sent successfully.")
except Exception as e:
    print("❌ Email failed. Error:")
    print(e)
