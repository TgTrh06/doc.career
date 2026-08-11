from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


OUTPUT = "output/pdf/Trinh_Thanh_Tung_CV_Backend_Draft.pdf"
PAGE_W, PAGE_H = A4

NAVY = colors.HexColor("#10243E")
BLUE = colors.HexColor("#1C4D80")
ORANGE = colors.HexColor("#E8893B")
INK = colors.HexColor("#182536")
MUTED = colors.HexColor("#617084")
LIGHT = colors.HexColor("#F3F6F9")
LINE = colors.HexColor("#DCE3EA")


def style(name, **kwargs):
    defaults = dict(
        name=name,
        fontName="Helvetica",
        fontSize=8.1,
        leading=10.6,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    defaults.update(kwargs)
    return ParagraphStyle(**defaults)


BODY = style("Body", fontSize=8.0, leading=10.4)
BODY_TIGHT = style("BodyTight", fontSize=7.55, leading=9.35)
SMALL = style("Small", fontSize=7.0, leading=8.8, textColor=MUTED)
CONTACT = style("Contact", fontSize=7.15, leading=9.2, textColor=colors.white)
SECTION = style("Section", fontName="Helvetica-Bold", fontSize=9.3, leading=11, textColor=BLUE)
LABEL = style("Label", fontName="Helvetica-Bold", fontSize=7.35, leading=9.2, textColor=BLUE)
PROJECT = style("Project", fontName="Helvetica-Bold", fontSize=9.4, leading=11.3, textColor=INK)
ROLE = style("Role", fontName="Helvetica-Bold", fontSize=8.7, leading=10.5, textColor=INK)


def draw_paragraph(canvas, text, x, top, width, paragraph_style=BODY):
    p = Paragraph(text, paragraph_style)
    _, height = p.wrap(width, PAGE_H)
    p.drawOn(canvas, x, top - height)
    return top - height


def draw_section(canvas, title, x, top, width):
    canvas.setFillColor(ORANGE)
    canvas.roundRect(x, top - 13, 4, 13, 2, fill=1, stroke=0)
    draw_paragraph(canvas, title.upper(), x + 9, top - 1, width - 9, SECTION)
    return top - 22


def draw_bullet(canvas, text, x, top, width, paragraph_style=BODY_TIGHT):
    p = Paragraph(text, paragraph_style, bulletText="-")
    p.leftIndent = 9
    p.firstLineIndent = -7
    _, height = p.wrap(width, PAGE_H)
    p.drawOn(canvas, x, top - height)
    return top - height - 4


def draw_rule(canvas, x, y, width):
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(x, y, x + width, y)


def main():
    canvas = Canvas(OUTPUT, pagesize=A4)
    canvas.setTitle("Trinh Thanh Tung - Backend CV Draft")
    canvas.setAuthor("Trinh Thanh Tung")

    # Header
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 111, PAGE_W, 111, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, PAGE_H - 111, PAGE_W, 4, fill=1, stroke=0)
    draw_paragraph(canvas, "TRINH THANH TUNG", 36, PAGE_H - 28, 320,
                   style("Name", fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=colors.white))
    draw_paragraph(canvas, "BACKEND DEVELOPER | FULL-STACK DEVELOPER", 37, PAGE_H - 59, 390,
                   style("Subtitle", fontName="Helvetica-Bold", fontSize=9.1, leading=11, textColor=colors.HexColor("#BFD7EC")))
    draw_paragraph(canvas, "Backend-focused engineer with enough frontend skill to ship complete product workflows.", 37, PAGE_H - 78, 420,
                   style("Tagline", fontSize=8.1, leading=10.2, textColor=colors.HexColor("#E4EDF5")))

    contact = "0337675626  |  tgtrh0604@gmail.com  |  Hanoi, Vietnam  |  github.com/TgTrh06"
    draw_paragraph(canvas, contact, 37, PAGE_H - 94, 515, CONTACT)

    left_x = 36
    left_w = 143
    right_x = 202
    right_w = PAGE_W - right_x - 36
    left_top = PAGE_H - 137
    right_top = PAGE_H - 137

    # Left column
    y = draw_section(canvas, "Profile", left_x, left_top, left_w)
    y = draw_paragraph(
        canvas,
        "Software Engineering student and backend-focused full-stack developer with end-to-end ownership of a large online learning platform. Strong in APIs, authentication, payments, data workflows and reliable product integrations, with enough frontend skill to ship complete user journeys.",
        left_x, y, left_w, BODY_TIGHT,
    ) - 13

    y = draw_section(canvas, "Backend Strengths", left_x, y, left_w)
    for item in [
        "Modular service architecture",
        "REST APIs and data contracts",
        "Authentication, sessions and RBAC",
        "Payments, commerce and integrations",
        "Testing, security and migrations",
    ]:
        y = draw_bullet(canvas, item, left_x, y, left_w)
    y -= 8

    y = draw_section(canvas, "Technical Skills", left_x, y, left_w)
    skills = [
        ("Backend", "Node.js, TypeScript, Express.js, PostgreSQL, Drizzle ORM, Redis"),
        ("Architecture", "REST APIs, RBAC, session auth, payment workflows, integrations"),
        ("Quality", "Unit and E2E testing, security checks, migrations, API validation"),
        ("Frontend", "React, Tailwind CSS, Zustand, Playwright E2E"),
    ]
    for label, value in skills:
        y = draw_paragraph(canvas, f"<b>{label}</b><br/>{value}", left_x, y, left_w, BODY_TIGHT) - 7
    y -= 2

    y = draw_section(canvas, "Education", left_x, y, left_w)
    y = draw_paragraph(canvas, "<b>Electric Power University</b><br/>Bachelor of Software Engineering<br/>10/2022 - Present<br/>GPA: 3.34 / 4.0", left_x, y, left_w, BODY_TIGHT) - 14

    y = draw_section(canvas, "Additional", left_x, y, left_w)
    y = draw_paragraph(canvas, "<b>English</b>: Intermediate", left_x, y, left_w, BODY_TIGHT) - 8
    draw_paragraph(canvas, "<b>Leadership</b>: Organized activities that helped 100+ freshmen integrate into a high-pressure school environment.", left_x, y, left_w, BODY_TIGHT)

    # Divider
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.8)
    canvas.line(188, PAGE_H - 137, 188, 45)

    # Right column
    y = draw_section(canvas, "Experience", right_x, right_top, right_w)
    y = draw_paragraph(canvas, "<b>IT INTERN | KTL</b><br/><font color='#617084'>11/2025 - Present</font>", right_x, y, right_w, ROLE) - 6
    y = draw_paragraph(canvas, "<b>TRI ANH EDU - Online Learning Platform</b>", right_x, y, right_w, PROJECT) - 5
    for item in [
        "Owned the end-to-end product implementation across <b>26 backend modules</b> and <b>78 frontend page files</b>, covering courses, learning, commerce, payments, exams and admin operations.",
        "Built backend services with Node.js, Express.js, TypeScript, PostgreSQL and Drizzle ORM for authentication, sessions, roles, courses, enrollments, cart/checkout, payments, vouchers, reviews and learning access.",
        "Implemented security and reliability workflows including OTP/session management, RBAC, request validation, Redis-backed controls, payment callbacks and database migrations.",
        "Created and maintained <b>81 backend test files</b> plus <b>35 frontend Playwright E2E cases</b> covering contracts, payment flows, accessibility errors, mobile overflow, checkout and exam security.",
    ]:
        y = draw_bullet(canvas, item, right_x, y, right_w)
    y -= 8

    y = draw_section(canvas, "Selected Project", right_x, y, right_w)
    y = draw_paragraph(canvas, "<b>ITSUSUSHI - Restaurant Reservation & Management Platform</b><br/><font color='#617084'>Solo full-stack project | 01/2026 - Present</font>", right_x, y, right_w, PROJECT) - 6
    for item in [
        "Designed and implemented the reservation backend: seat availability, reservation state transitions, payment confirmation and admin approval workflows.",
        "Supported <b>2 user roles</b> across customer and admin journeys, with <b>5 time slots</b>, maximum <b>8 seats</b> per reservation and a <b>15-minute</b> payment expiry.",
        "Implemented JWT access/refresh authentication, protected routes, Zod validation and MongoDB persistence for a complete reservation product.",
        "Built the supporting frontend flow across <b>17 page components</b> and <b>7 admin screens</b> so users can discover, reserve, pay and track reservations.",
    ]:
        y = draw_bullet(canvas, item, right_x, y, right_w)
    y -= 8
    draw_paragraph(canvas, "<b>Stack</b>: React 19, TypeScript, Zustand, Zod, Axios, Express.js, MongoDB", right_x, y, right_w, SMALL)
    y -= 17

    y = draw_section(canvas, "Links", right_x, y, right_w)
    draw_paragraph(
        canvas,
        "<b>TRI ANH EDU BE</b>: <a href='https://github.com/TgTrh06/project.trianh-edu-backend' color='#1C4D80'>GitHub repository</a><br/>"
        "<b>TRI ANH EDU FE</b>: <a href='https://github.com/TgTrh06/project.trianh-edu-frontend' color='#1C4D80'>GitHub repository</a><br/>"
        "<b>ITSUSUSHI</b>: <a href='https://github.com/TgTrh06/project.sushi-shop' color='#1C4D80'>GitHub repository</a><br/>"
        "<b>Portfolio</b>: add your Figma / Notion case-study link before sending",
        right_x, y, right_w, BODY_TIGHT,
    )

    # Footer
    draw_rule(canvas, 36, 35, PAGE_W - 72)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 6.5)
    canvas.drawString(36, 23, "Backend CV draft - replace the portfolio placeholder before applying")
    canvas.drawRightString(PAGE_W - 36, 23, "2026")
    canvas.showPage()
    canvas.save()


if __name__ == "__main__":
    main()
