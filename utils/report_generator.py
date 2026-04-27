from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
import re
from html import escape


def clean_line(line: str) -> str:
    line = re.sub(r"#+\s*", "", line)  # remove ###
    return line.strip()


def create_pdf_bytes(text: str) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # 🔵 TITLE STYLE (BOLD + BULLET)
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceBefore=10,
        spaceAfter=5,
    )

    # 🔹 SUB BULLET STYLE
    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leftIndent=15,
        spaceAfter=4,
    )

    story = []

    for raw_line in text.split("\n"):
        line = clean_line(raw_line)

        if not line:
            story.append(Spacer(1, 6))
            continue

        # 🔥 TITLE (ADD ROUND BULLET)
        if not line.startswith("-"):
            story.append(Paragraph(f"• <b>{escape(line)}</b>", title_style))

        # 🔹 SUB POINTS
        else:
            bullet = line.replace("-", "").strip()
            story.append(Paragraph(f"• {escape(bullet)}", bullet_style))

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()