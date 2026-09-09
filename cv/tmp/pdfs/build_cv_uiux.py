from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


# Run this script from any working directory.
CV_ROOT = Path(__file__).resolve().parents[2]
GENERATED_AT = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_NAME = f"Trinh_Thanh_Tung_CV_Harvard_Backend_{GENERATED_AT}.pdf"
OUTPUT = CV_ROOT / "output" / "pdf" / OUTPUT_NAME
PAGE_W, PAGE_H = A4
PAGE_MARGIN = 43
MARGIN = PAGE_MARGIN
CONTENT_W = PAGE_W - (PAGE_MARGIN * 2)

INK = colors.HexColor("#1E2823")
MUTED = colors.HexColor("#5B675F")
ACCENT = colors.HexColor("#546B45")
ACCENT_HEX = "#546B45"
RULE = colors.HexColor("#C7CEC7")

# Layout controls: use one predictable spacing system throughout the CV.
SPACE_XS = 3
SPACE_SM = 5
SPACE_MD = 8
SPACE_LG = 12

SECTION_RULE_OFFSET = 4
SECTION_END_GAP = 22
SECTION_TITLE_BOTTOM_GAP = 9
DEFAULT_SECTION_SPACING = {
    "before_title": SECTION_END_GAP,
    "title_bottom": SECTION_TITLE_BOTTOM_GAP,
}
SECTION_SPACING = {
    "Summary": {"before_title": 10, "title_bottom": SECTION_TITLE_BOTTOM_GAP},
    "Experience": {"before_title": SECTION_END_GAP, "title_bottom": SECTION_TITLE_BOTTOM_GAP},
    "Selected Projects": {"before_title": SECTION_END_GAP, "title_bottom": SECTION_TITLE_BOTTOM_GAP},
    "Technical Skills": {"before_title": SECTION_END_GAP, "title_bottom": SECTION_TITLE_BOTTOM_GAP},
    "Education": {"before_title": SECTION_END_GAP, "title_bottom": SECTION_TITLE_BOTTOM_GAP},
    "Languages": {"before_title": SECTION_END_GAP, "title_bottom": SECTION_TITLE_BOTTOM_GAP},
}
CONTENT_GAP = SPACE_MD
RECORD_GAP = SPACE_SM
BULLET_GAP = SPACE_XS
COLUMN_GAP = SPACE_LG
RECORD_BASELINE_OFFSET = 9
RECORD_HEADER_HEIGHT = 14
HEADER_NAME_TO_ROLE_GAP = 19
HEADER_ROLE_TO_CONTACT_GAP = 8
HEADER_CONTACT_TO_SECTION_GAP = 13
EDUCATION_RIGHT_W = 170


def make_style(name, **kwargs):
    defaults = dict(
        name=name,
        fontName="Helvetica",
        fontSize=8.7,
        leading=11.1,
        textColor=INK,
        spaceAfter=0,
    )
    defaults.update(kwargs)
    return ParagraphStyle(**defaults)


BODY = make_style("Body")
BODY_SMALL = make_style("BodySmall", fontSize=8.1, leading=10.1)
BODY_SMALL_RIGHT = make_style("BodySmallRight", fontSize=8.1, leading=10.1, alignment=2)
META = make_style("Meta", fontSize=8.0, leading=9.8, textColor=MUTED)
SECTION = make_style("Section", fontName="Helvetica-Bold", fontSize=9.4, leading=11, textColor=ACCENT)


def draw_paragraph(canvas, text, x, top, width, paragraph_style=BODY):
    paragraph = Paragraph(text, paragraph_style)
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(canvas, x, top - height)
    return top - height


def draw_two_column_paragraph(canvas, left_text, right_text, top, left_width, right_width, gap=COLUMN_GAP):
    """Draw one content row with independent left- and right-aligned paragraphs."""
    left = Paragraph(left_text, BODY_SMALL)
    right = Paragraph(right_text, BODY_SMALL_RIGHT)
    _, left_height = left.wrap(left_width, PAGE_H)
    _, right_height = right.wrap(right_width, PAGE_H)
    row_height = max(left_height, right_height)
    left.drawOn(canvas, MARGIN, top - left_height)
    right.drawOn(canvas, MARGIN + left_width + gap, top - right_height)
    return top - row_height


def draw_section(canvas, title, top):
    """Draw a section title with a small title gap and a separate section-end gap."""
    spacing = SECTION_SPACING.get(title, DEFAULT_SECTION_SPACING)
    top -= spacing["before_title"]
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 9.4)
    canvas.drawString(MARGIN, top, title.upper())
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.65)
    rule_y = top - SECTION_RULE_OFFSET
    canvas.line(MARGIN, rule_y, PAGE_W - MARGIN, rule_y)
    return rule_y - spacing["title_bottom"]


def draw_record_header(
    canvas,
    title,
    date_text,
    top,
    title_font_size=9.0,
    date_font_size=8.2,
):
    """Draw a record title and timeline on the same baseline."""
    baseline = top - RECORD_BASELINE_OFFSET
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", title_font_size)
    canvas.drawString(MARGIN, baseline, title)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", date_font_size)
    canvas.drawRightString(PAGE_W - MARGIN, baseline, date_text)
    return top - RECORD_HEADER_HEIGHT


def draw_bullet(canvas, text, top):
    paragraph = Paragraph(text, BODY_SMALL, bulletText="\u2022")
    paragraph.leftIndent = 11
    paragraph.firstLineIndent = -8
    _, height = paragraph.wrap(CONTENT_W, PAGE_H)
    paragraph.drawOn(canvas, MARGIN, top - height)
    return top - height - BULLET_GAP


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas = Canvas(str(OUTPUT), pagesize=A4)
    canvas.setTitle("Trinh Thanh Tung - Backend Developer CV")
    canvas.setAuthor("Trinh Thanh Tung")

    top = PAGE_H - PAGE_MARGIN
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawString(MARGIN, top, "TRINH THANH TUNG")
    top -= HEADER_NAME_TO_ROLE_GAP
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(MARGIN, top, "BACKEND DEVELOPER")
    top -= HEADER_ROLE_TO_CONTACT_GAP
    top = draw_paragraph(
        canvas,
        f"0337675626  |  tgtrh0604@gmail.com  |  Hanoi, Vietnam  |  <a href='https://github.com/TgTrh06' color='{ACCENT_HEX}'>github.com/TgTrh06</a>",
        MARGIN,
        top,
        CONTENT_W,
        META,
    )
    top -= HEADER_CONTACT_TO_SECTION_GAP

    top = draw_section(canvas, "Summary", top)
    top = draw_paragraph(
        canvas,
        "Final-year Software Engineering student with hands-on experience developing and maintaining an LMS / EdTech platform. Built TypeScript, Node.js and Express.js backend services with RESTful API design and integration, OOP principles, PostgreSQL / SQL, authentication and authorization, error handling, API security, payment workflows, Git and automated testing.",
        MARGIN,
        top,
        CONTENT_W,
        BODY,
    )

    top = draw_section(canvas, "Experience", top)
    top = draw_record_header(canvas, "IT INTERN | KTL", "Nov 2025 - Aug 2026", top)
    top = draw_paragraph(canvas, "<b>TRI ANH EDUCATION - LMS / EdTech Platform</b>", MARGIN, top, CONTENT_W, BODY_SMALL) - RECORD_GAP
    for bullet in [
        "Developed and maintained an LMS / EdTech platform across <b>26 backend modules</b> and <b>78 frontend page files</b>, supporting courses, learning, commerce, payments, exams and admin operations.",
        "Designed, built and maintained TypeScript, Node.js and Express.js (ExpressJS) RESTful APIs with PostgreSQL and Drizzle ORM for authentication, roles, courses, enrollments, checkout, payments, vouchers and learning access.",
        "Applied OOP principles, structured backend modules, coding conventions, error handling, OTP, session management, RBAC, request validation, Redis-backed controls, payment callbacks and database migrations for secure product flows.",
        "Maintained <b>81 backend test files</b> and <b>35 Playwright E2E cases</b>, reducing regression risk across RESTful API contracts, checkout, payments, mobile and exam-security scenarios.",

    ]:
        top = draw_bullet(canvas, bullet, top)

    top = draw_section(canvas, "Selected Projects", top)
    top = draw_record_header(
        canvas,
        "ITSUSUSHI - Restaurant Reservation Platform",
        "Jan 2026 - Present",
        top,
        title_font_size=8.8,
    )
    top = draw_paragraph(
        canvas,
        f"Solo project  |  <a href='https://project-sushi-shop-frontend.vercel.app/' color='{ACCENT_HEX}'>Demo</a>  |  Repository: <a href='https://github.com/TgTrh06/project.sushi-shop' color='{ACCENT_HEX}'>ItsuSushi</a>",
        MARGIN,
        top,
        CONTENT_W,
        META,
    ) - RECORD_GAP
    for bullet in [
        "Built the reservation backend around seat availability, reservation state transitions, payment confirmation and admin approval, enabling a complete restaurant reservation workflow.",
        "Designed customer and admin journeys for <b>2 user roles</b>, using <b>5 time slots</b>, a maximum of <b>8 seats</b> per reservation and a <b>15-minute</b> payment expiry to enforce booking constraints.",
        "Implemented JWT access and refresh authentication, protected routes, Zod validation and MongoDB persistence to secure reservation and administrative operations.",
        "Delivered <b>17 page components</b> and <b>7 admin screens</b> covering restaurant discovery, reservation, payment and history, providing end-to-end customer and management flows.",
    ]:
        top = draw_bullet(canvas, bullet, top)
    top -= CONTENT_GAP

    top = draw_section(canvas, "Technical Skills", top)
    for skill in [
        "<b>Backend:</b> JavaScript, TypeScript, Node.js, Express.js (ExpressJS), RESTful API Design &amp; Integration, OOP",
        "<b>API &amp; Security:</b> Authentication &amp; Authorization (RBAC), Error Handling, Request Validation, API Security",
        "<b>Database &amp; Data:</b> PostgreSQL, SQL, MongoDB, Redis, Drizzle ORM, Database Migrations",
        "<b>Engineering Practices:</b> Git, Automated Testing, E2E Testing (Playwright)",
        "<b>Frontend &amp; Domain:</b> React, Tailwind CSS, Zustand, LMS / EdTech, Payment Integration",
    ]:

        top = draw_bullet(canvas, skill, top)

    top = draw_section(canvas, "Education", top)
    top = draw_record_header(canvas, "ELECTRIC POWER UNIVERSITY", "2022 - Present", top, title_font_size=8.8, date_font_size=8.0)
    top = draw_two_column_paragraph(
        canvas,
        "Engineer in Software Engineering | GPA: 3.34 / 4.0",
        "Expected graduation: Feb 2027",
        top,
        left_width=CONTENT_W - EDUCATION_RIGHT_W - COLUMN_GAP,
        right_width=EDUCATION_RIGHT_W,
        gap=COLUMN_GAP,
    )

    top = draw_section(canvas, "Languages", top)
    for language in [
        "<b>English:</b> B1 assessment at Electric Power University - 9.5/10; technical documentation reading",
        "<b>Japanese:</b> Currently studying JLPT N5 (beginner level)",
    ]:
        top = draw_bullet(canvas, language, top)

    canvas.showPage()
    canvas.save()
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
