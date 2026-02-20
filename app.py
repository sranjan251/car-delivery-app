from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle
import io
from datetime import datetime

app = Flask(__name__)

LOGO_PATH = "static/logo.jpg" # Put logo inside static folder

def generate_pdf(data):
    # Create PDF in memory (BytesIO)
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
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
            ["Buyer Address", data["buyer_address"]],
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
    pdf_buffer.seek(0)
    return pdf_buffer

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form
        pdf_buffer = generate_pdf(data)
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"delivery_note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
