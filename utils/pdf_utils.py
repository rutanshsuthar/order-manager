# utils/pdf_utils
from datetime import date
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Frame, PageTemplate, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def draw_letterhead(canvas, doc, customer_name, contact_number, order_no, date):
    canvas.setFont("Helvetica-Bold", 40)
    canvas.drawCentredString(105 * mm, A4[1] - 15 * mm, "SARTHAK ENTERPRISES LTD", wordSpace=0.5 * mm)

    canvas.setFont("Helvetica", 15)
    canvas.drawCentredString(105 * mm, A4[1] - 22 * mm,
                             "Direct Importers and Wholesalers of Bicycles and Spare Parts / Agriculture Implements")

    canvas.drawString(0 * mm, A4[1] - 32 * mm, "  Plot No. 20515, Mumbwa Road,")
    canvas.drawString(0 * mm, A4[1] - 38 * mm, "  Chinika Area,")
    canvas.drawString(0 * mm, A4[1] - 44 * mm, "  Lusaka, Zambia")

    canvas.drawRightString(210 * mm, A4[1] - 38 * mm, "Mobile: +260 953 663 143  ")
    canvas.drawRightString(210 * mm, A4[1] - 44 * mm, "Email: sarthaksky111@gmail.com  ")

    canvas.setLineWidth(1)
    canvas.setStrokeColor(colors.black)
    canvas.line(2 * mm, A4[1] - 47 * mm, A4[0] - 2 * mm, A4[1] - 47 * mm)

    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawCentredString(105 * mm, A4[1] - 55 * mm, "ORDER NOTE")

    canvas.setFont("Helvetica-Bold", 15)
    canvas.drawString(0 * mm, A4[1] - 63 * mm, f"  Customer Name: {customer_name}")
    canvas.drawString(0 * mm, A4[1] - 72 * mm, f"  Contact Number: {contact_number}")

    canvas.drawString(155 * mm, A4[1] - 63 * mm, f"No. {order_no}")
    canvas.drawString(155 * mm, A4[1] - 72 * mm, f"Date: {date}")


def create_pdf(data, customer_name, mobile_number, order_no):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    col_widths = [10 * mm, 10 * mm, 10 * mm, 160 * mm]

    data_with_sn = [[str(i + 1), "", qty, desc] for i, (qty, desc) in enumerate(data)]

    table_data = [['SN', 'Chk', 'Qty', 'Description']] + data_with_sn
    table = Table(table_data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 0), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    elements.append(table)

    elements.append(Spacer(1, 12 * mm))

    styles = getSampleStyleSheet()

    prepared_by = Paragraph("Prepared By: __________________________________", styles['Normal'])
    sign_prepared_by = Paragraph("Sign: ____________________", styles['Normal'])
    received_by = Paragraph("Received By: __________________________________", styles['Normal'])
    sign_received_by = Paragraph("Sign: ____________________", styles['Normal'])
    remarks = Paragraph(
        "Remarks: ______________________________________________________________________________________",
        styles['Normal'])

    table_prepared_by = Table([[prepared_by, sign_prepared_by]], colWidths=[110 * mm, 80 * mm])
    table_received_by = Table([[received_by, sign_received_by]], colWidths=[110 * mm, 80 * mm])
    table_remarks = Table([[remarks]], colWidths=[190 * mm])

    elements.append(table_prepared_by)
    elements.append(Spacer(1, 6 * mm))
    elements.append(table_received_by)
    elements.append(Spacer(1, 6 * mm))
    elements.append(table_remarks)

    frame = Frame(10 * mm, 10 * mm, A4[0] - 20 * mm, A4[1] - 85 * mm, id='normal')

    def draw_letterhead_with_args(canvas, doc):
        current_date = date.today()
        draw_letterhead(canvas, doc, customer_name, mobile_number, order_no, current_date)

    template = PageTemplate(id='test', frames=frame, onPage=draw_letterhead_with_args)
    pdf.addPageTemplates([template])

    pdf.build(elements)
    buffer.seek(0)
    return buffer
