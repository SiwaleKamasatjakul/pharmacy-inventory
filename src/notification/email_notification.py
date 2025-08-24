from dotenv import load_dotenv
import os
from pretty_html_table import build_table

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from calculation.threadhold_inventory import ExpireDateCalculation,ReservePharmacyButNoStock

class EmailNotification:
    
    load_dotenv()
    
    @staticmethod
    def email_notification():
        email_sender = os.getenv("EMAIL_SENDER")
        email_password = os.getenv("EMAIL_PASSWORD")
        get_email_receiver = os.getenv("EMAIL_RECIEVER")
        email_receiver = [get_email_receiver]
        
        subject = "Pharmacy Stock Notification"

        # Get DataFrames from your custom classes
        reserve_pharmacy_but_not_stock = ReservePharmacyButNoStock.reserved_pharmacy_but_no_stock()
        expiredate_calculation = ExpireDateCalculation.expiredateCalculation()
        
        # Convert to HTML tables
        reserve_pharmacy_html = reserve_pharmacy_but_not_stock.to_html(index=False)
        expiredate_html = expiredate_calculation.to_html(index=False)
        
        # Create the message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = email_sender
        msg["To"] = ",".join(email_receiver)

        # Build email body with sections
        html_content = f"""
        <html>
        <body>
            <h2>📅 รายละเอียดข้อมูล</h2>
            
            <h3>🔴 รายการยาที่ใกล้หมดอายุในอีก 30 วัน</h3>
            {expiredate_html}
            
            <h3>⚠️ รายการยาที่ถูกจองไว้แต่ไม่มี stock ยาเหลือ</h3>
            {reserve_pharmacy_html}
        </body>
        </html>
        """

        # Attach HTML
        msg.attach(MIMEText(html_content, "html"))
        
        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string()) 
        server.quit()

        print("✅ Sent the email!")


if __name__ == "__main__":
    EmailNotification.email_notification()