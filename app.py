from flask import Flask, render_template, request, send_file, Response, make_response
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle
import io
from datetime import datetime
import os

app = Flask(__name__)

LOGO_PATH = "static/logo.jpg"  # Put logo inside static folder

def generate_pdf(data):
    # Create PDF in memory (BytesIO) with A4 dimensions
    pdf_buffer = io.BytesIO()
    # A4 size: 8.27 x 11.69 inches
    doc = SimpleDocTemplate(
        pdf_buffer,
        rightMargin=0.4*inch,
        leftMargin=0.4*inch,
        topMargin=0.3*inch,
        bottomMargin=0.3*inch,
        pagesize=(8.27*inch, 11.69*inch)  # A4 dimensions
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Calculate dimensions based on A4 page
    page_height = 11.69 * inch
    header_height = page_height * 0.10  # 10% for header
    footer_height = page_height * 0.05  # 5% for footer
    
    # === HEADER (20% of page) ===
    # Header with logo on left and contact info on right
    header_logo = ""
    header_contact = ""
    
    try:
        if os.path.exists(LOGO_PATH):
            header_logo = 47
 header_logo = Image(LOGO_PATH, width=1.38*inch, height=1*inch)
else:
            logo_style = ParagraphStyle(
                'LogoPlaceholder',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.grey
            )
            header_logo = Paragraph("[Logo]", logo_style)
    except:
        logo_style = ParagraphStyle(
            'LogoPlaceholder',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.grey
        )
        header_logo = Paragraph("[Logo]", logo_style)
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        alignment=2,  # Right align
        fontSize=9,
        leading=12,
        textColor=colors.black
    )
    
    header_contact = Paragraph(
        "<b>KAM CARZ</b><br/>Email: kunalmehta@kamcarz.com<br/>Website: www.kamcarz.com",
        contact_style
    )
    
    # Create header table with logo and contact
    75
77
44
(
        [[header_logo, header_contact]],
        colWidths=[2*inch, 5.47*inch],
        rowHeights=[header_height]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.lightgrey),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # === TITLE (LEFT ALIGNED) ===
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=0,  # Left align
        spaceAfter=15,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("CAR DELIVERY NOTE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # === DELIVERY INFORMATION TABLE ===
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
    table = Table(table_data, colWidths=[2.2*inch, 5.47*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # === SIGNATURE SECTION (space above text) ===
    sig_style = ParagraphStyle(
        'SigStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=0
    )
    
    sig_table = Table(
        [
            [
                Paragraph("_________________________<br/><br/>Buyer Signature", sig_style),
                Paragraph("_________________________<br/><br/>Seller Signature", sig_style)
            ]
        ],
        colWidths=[3.635*inch, 3.635*inch]
    )
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(sig_table)
    
    # === FOOTER (5% of page) ===
    # Push remaining space
    elements.append(Spacer(1, 0.4*inch))
    
    footer_style_left = ParagraphStyle(
        'FooterStyleLeft',
        parent=styles['Normal'],
        fontSize=8,
        alignment=0,  # Left align
        textColor=colors.grey
    )
    
    footer_style_right = ParagraphStyle(
        'FooterStyleRight',
        parent=styles['Normal'],
        fontSize=8,
        alignment=2,  # Right align
        textColor=colors.grey
    )
    
    footer_table = Table(
        [
            [
                Paragraph("www.kamcarz.com", footer_style_left),
                Paragraph("Powered by Neovertx", footer_style_right)
            ]
        ],
        colWidths=[4.135*inch, 4.135*inch]
    )
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LINEABOVE', (0, 0), (-1, -1), 1, colors.lightgrey),
    ]))
    
    elements.append(footer_table)
    
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
