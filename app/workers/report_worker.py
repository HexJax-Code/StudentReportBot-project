import os
from app.services.pdf_generator import generate_report
from app.services.whatsapp_adapter import send_whatsapp_message

def process_student(student):
    name = student["name"]
    pdf_path = f"/tmp/{name.replace(' ', '_')}_report.pdf"

    # 1. Generate PDF
    generate_report(student, pdf_path)

    # 2. Send WhatsApp message
    send_whatsapp_message(
        student["phone"],
        f"Hello {name}, your report is ready!",
        media_url=None
    )

    # Optional: upload PDF to cloud & send link
    return True
