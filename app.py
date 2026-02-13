from flask import Flask, render_template, request
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

app = Flask(__name__)

LOGO_PATH = "static/logo.jpg"  # Put logo inside static folder

def generate_pdf(data, filename):
    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    elements = []
    styles = getSampleStyleSheet()

    # === HEADER WITH LOGO (Right aligned) ===
    logo = Image(LOGO_PATH, width=2.5*inch, height=0.8*inch)
    header_table = Table(
        [
            [
                Paragraph("**CAR DELIVERY NOTE**", styles["Title"]),
                logo
            ]
        ],
        colWidths=[4*inch, 2*inch]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.4 * inch))

    # === DELIVERY INFO TABLE ===
    table_data = [
        ["Delivery Date", datetime.now().strftime("%d %B %Y")],
        ["Seller Name", data["seller_name"]],
        ["Seller Email", data["seller_email"]],
        ["Buyer Name", data["buyer_name"]],
        ["Buyer Email", data["buyer_email"]],
        ["Car Make", data["car_make"]],
        ["Car Model", data["car_model"]],
        ["Year", data["car_year"]],
        ["VIN", data["vin"]],
        ["Registration No", data["reg_no"]],
        ["Odometer Reading", data["odometer"]],
    ]
    table = Table(table_data, colWidths=[2.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    # === SIGNATURE SECTION ===
    signature_table = Table(
        [
            [
                "Seller Signature: ______________________",
                "Buyer Signature: ______________________"
            ]
        ],
        colWidths=[3*inch, 3*inch]
    )
    signature_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 30),
    ]))
    elements.append(signature_table)
    doc.build(elements)

def send_email(receiver, pdf_file):
    msg = EmailMessage()
    msg["Subject"] = "Car Delivery Note"
    msg["From"] = os.environ.get("EMAIL_ADDRESS")
    msg["To"] = receiver
    msg.set_content("Please find attached the car delivery note.")

    with open(pdf_file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="delivery_note.pdf"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.environ.get("EMAIL_ADDRESS"),
            os.environ.get("EMAIL_PASSWORD")
        )
        smtp.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form
        filename = "delivery_note.pdf"
        generate_pdf(data, filename)
        send_email(data["buyer_email"], filename)
        send_email(data["seller_email"], filename)
        return "Delivery Note Generated and Sent Successfully!"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
