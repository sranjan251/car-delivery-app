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
        colWidths=[3.635 * inch, 3.635 * inch]
    )
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    elements.append(sig_table)
