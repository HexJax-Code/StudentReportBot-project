from reportlab.pdfgen import canvas

def generate_report(student, output_path):
    c = canvas.Canvas(output_path)
    c.setFont("Helvetica", 16)

    c.drawString(50, 800, "Student Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Name: {student['name']}")
    c.drawString(50, 740, f"Math: {student['math']}")
    c.drawString(50, 720, f"English: {student['english']}")
    c.drawString(50, 700, f"Science: {student['science']}")

    c.save()
    return output_path
