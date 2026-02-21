from flask import Flask, render_template, request, send_file, Response, make_response
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle
import io
from datetime import datetime

app = Flask(__name__)

LOGO_PATH = "static/logo.jpg"  # Put logo inside static folder

def generate_pdf(data):
    # Create PDF in memory (BytesIO)
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        pagesize=(8.5*inch, 11*inch)
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # === TOP HEADER WITH LOGO AND CONTACT INFO ===
    logo_style = ParagraphStyle(
        'LogoStyle',
        parent=styles['Normal'],
        alignment=0,  # Left align
        fontSize=10,
        leading=12
    )
    
    contact_para = Paragraph(
        "<b>KAM CARZ</b><br/>Email: kunalmehta@kamcarz.com<br/>Website: www.kamcarz.com",
        logo_style
    )
    
    # Create header table with logo on left and contact on right
    header_table = Table(
        [[contact_para, ""]],
        colWidths=[4*inch, 2*inch],
        rowHeights=[0.8*inch]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)
    
    # === MAIN HEADING ===
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=1,  # Center align
        spaceAfter=10,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("CAR DELIVERY NOTE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # === DELIVERY INFORMATION TABLE WITH SEPARATE VEHICLE DETAILS ===
    table_data = [
        ["Buyer Name:", data.get("buyer_name", "")],
        ["Buyer Address:", data.get("buyer_address", "")],
        ["Buyer Contact:", data.get("buyer_email", "")],
        ["Car Make:", data.get("car_make", "")],
        ["Car Model:", data.get("car_model", "")],
        ["Year:", data.get("car_year", "")],
        ["Chasis No.:", data.get("Chasis No.", "")],
        ["Registration No:", data.get("reg_no", "")],
        ["Odometer Reading:", data.get("odometer", "")],
        ["Seller Name:", data.get("seller_name", "")],
    ["Seller Address:", data.get("seller_address", "")],
            ["Seller Contact:", data.get("seller_email", "")],
        ["Delivery Date:", datetime.now().strftime("%d %B %Y")],
    ]
    
    # Build table with proper styling
    table = Table(table_data, colWidths=[2.2*inch, 4.3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.4*inch))
    
    # === SIGNATURE SECTION ===
    sig_style = ParagraphStyle(
        'SigStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=0
    )
    
    sig_table = Table(
        [
            [
                Paragraph("Buyer Signature<br/><br/>_________________________", sig_style),
                Paragraph("Seller Signature<br/><br/>_________________________", sig_style)
            ]
        ],
        colWidths=[3.25*inch, 3.25*inch]
    )
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(sig_table)
    
    # === FOOTER ===
    elements.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=1,  # Center
        textColor=colors.grey
    )
    footer = Paragraph("www.kamcarz.com", footer_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form
        pdf_buffer = generate_pdf(data)
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=delivery_note_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        response.headers['Content-Length'] = len(pdf_buffer.getvalue())
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
