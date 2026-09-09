from pathlib import Path

from reportlab.pdfgen.canvas import Canvas

import build_cv_uiux as base


CV_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = CV_ROOT / "output" / "pdf" / "Trinh_Thanh_Tung_CV_Junior_Frontend_EDUCO.pdf"


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Keep the established one-page visual system while making room for the
    # additional frontend project evidence relevant to EDUCO.
    for title in base.SECTION_SPACING:
        base.SECTION_SPACING[title]["before_title"] = 22
        base.SECTION_SPACING[title]["title_bottom"] = 9
    base.SECTION_SPACING["Summary"]["before_title"] = 10

    base.BODY.fontSize = 9.0
    base.BODY.leading = 11.5
    base.BODY_SMALL.fontSize = 8.4
    base.BODY_SMALL.leading = 10.5
    base.BODY_SMALL_RIGHT.fontSize = 8.4
    base.BODY_SMALL_RIGHT.leading = 10.5

    canvas = Canvas(str(OUTPUT), pagesize=base.A4)
    canvas.setTitle("Trinh Thanh Tung - Frontend Developer CV")
    canvas.setAuthor("Trinh Thanh Tung")

    top = base.PAGE_H - base.PAGE_MARGIN
    canvas.setFillColor(base.INK)
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawString(base.MARGIN, top, "TRINH THANH TUNG")
    top -= base.HEADER_NAME_TO_ROLE_GAP
    canvas.setFillColor(base.ACCENT)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(base.MARGIN, top, "FRONTEND DEVELOPER")
    top -= base.HEADER_ROLE_TO_CONTACT_GAP
    top = base.draw_paragraph(
        canvas,
        f"0337675626  |  tgtrh0604@gmail.com  |  Hanoi, Vietnam  |  "
        f"<a href='https://github.com/TgTrh06' color='{base.ACCENT_HEX}'>github.com/TgTrh06</a>",
        base.MARGIN,
        top,
        base.CONTENT_W,
        base.META,
    )
    top -= base.HEADER_CONTACT_TO_SECTION_GAP

    top = base.draw_section(canvas, "Summary", top)
    top = base.draw_paragraph(
        canvas,
        "Final-year Software Engineering student with hands-on frontend experience on LMS / EdTech and full-stack products. Builds responsive interfaces with HTML, CSS, JavaScript / TypeScript and React; integrates REST APIs; and uses Git, Playwright and AI Coding Assistant (Codex) for implementation, testing and debugging. Eager to apply these foundations while learning Svelte / SvelteKit.",
        base.MARGIN,
        top,
        base.CONTENT_W,
        base.BODY,
    )

    top = base.draw_section(canvas, "Experience", top)
    top = base.draw_record_header(canvas, "IT INTERN | KTL", "Nov 2025 - Aug 2026", top)
    top = base.draw_paragraph(
        canvas,
        "<b>TRI ANH EDUCATION - LMS / EdTech Platform</b>",
        base.MARGIN,
        top,
        base.CONTENT_W,
        base.BODY_SMALL,
    ) - base.RECORD_GAP
    for bullet in [
        "Developed and maintained responsive LMS / EdTech interfaces across <b>78 frontend page files</b>, supporting course discovery, learning, checkout, payments, exams and admin operations.",
        "Connected user-facing flows with TypeScript REST APIs across authentication, roles, courses, enrollments, vouchers, payments and learning access while handling validation and common integration issues.",
        "Maintained <b>35 Playwright E2E cases</b> for checkout, payments, mobile behavior and exam-security scenarios, helping detect regressions and debug issues across frontend and API boundaries.",
    ]:
        top = base.draw_bullet(canvas, bullet, top)

    top = base.draw_section(canvas, "Selected Projects", top)
    top = base.draw_record_header(
        canvas,
        "ITSUSUSHI - Restaurant Reservation Platform",
        "Jan 2026 - Present",
        top,
        title_font_size=8.8,
    )
    top = base.draw_paragraph(
        canvas,
        f"Solo project  |  <a href='https://project-sushi-shop-frontend.vercel.app/' color='{base.ACCENT_HEX}'>Demo</a>  |  "
        f"Repository: <a href='https://github.com/TgTrh06/project.sushi-shop' color='{base.ACCENT_HEX}'>ItsuSushi</a>",
        base.MARGIN,
        top,
        base.CONTENT_W,
        base.META,
    ) - base.RECORD_GAP
    for bullet in [
        "Built <b>17 customer page components</b> and <b>7 admin screens</b> with React, TypeScript and Tailwind CSS for restaurant discovery, reservation, payment, history and operations.",
        "Integrated REST APIs for seat availability, reservation state transitions, payment confirmation and admin approval, delivering end-to-end customer and management flows.",
    ]:
        top = base.draw_bullet(canvas, bullet, top)

    top -= 2
    top = base.draw_record_header(
        canvas,
        "ITSUMORI - Personal Developer Portfolio",
        "Sep 2026",
        top,
        title_font_size=8.8,
    )
    for bullet in [
        "Built a responsive portfolio with React 19, TypeScript, semantic HTML, CSS and Vite, including mobile navigation, keyboard interactions and reduced-motion support.",
        "Verified no horizontal overflow at <b>7 viewport widths from 320px to 1440px</b>; passed ESLint, TypeScript type-checking and production build validation.",
    ]:
        top = base.draw_bullet(canvas, bullet, top)

    top = base.draw_section(canvas, "Technical Skills", top)
    for skill in [
        "<b>Frontend Core:</b> HTML5, CSS3, JavaScript, TypeScript, Responsive Web Design",
        "<b>Frameworks &amp; UI:</b> React, Vite, Tailwind CSS, Zustand",
        "<b>API &amp; Debugging:</b> REST API Integration, Client-side State, Validation, Error Handling",
        "<b>Testing &amp; Workflow:</b> Git, Playwright, E2E Testing, Automated Testing, ESLint, Type Checking",
        "<b>AI-assisted Development:</b> Codex for code implementation, test support and debugging",
    ]:
        top = base.draw_bullet(canvas, skill, top)

    top = base.draw_section(canvas, "Education", top)
    top = base.draw_record_header(
        canvas,
        "ELECTRIC POWER UNIVERSITY",
        "2022 - Present",
        top,
        title_font_size=8.8,
        date_font_size=8.0,
    )
    top = base.draw_two_column_paragraph(
        canvas,
        "Engineer in Software Engineering | GPA: 3.34 / 4.0",
        "Expected graduation: Feb 2027",
        top,
        left_width=base.CONTENT_W - base.EDUCATION_RIGHT_W - base.COLUMN_GAP,
        right_width=base.EDUCATION_RIGHT_W,
        gap=base.COLUMN_GAP,
    )

    top = base.draw_section(canvas, "Languages", top)
    top = base.draw_bullet(
        canvas,
        "<b>English:</b> B1 assessment at Electric Power University - 9.5/10; technical documentation reading",
        top,
    )

    if top < base.PAGE_MARGIN:
        raise RuntimeError(f"CV content exceeds the bottom margin: {top:.1f} pt")

    canvas.showPage()
    canvas.save()
    print(f"Created: {OUTPUT}")
    print(f"Remaining bottom space: {top - base.PAGE_MARGIN:.1f} pt")


if __name__ == "__main__":
    main()
