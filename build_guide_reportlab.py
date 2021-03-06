import argparse
import datetime
import i18n
import os

from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, FragLine, ParaLines
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import arabic_reshaper

from bidi.algorithm import get_display

CONTRIBUTERS = [
    ("Anthony Wanyoike Peter", ["Portal screenshots"]),
    ("Imaduddin Ahmad Dalvi", ["Urdu translation"]),
    ("Ranjanas Vadivel", ["Sinhala and Tamil translation"]),
    ("Paul Mary Ranjanas", ["Sinhala and Tamil translation"]),
]


def text_transform_urdu(text):
    reshaper = arabic_reshaper.ArabicReshaper({"language": "Urdu"})
    reshaper = arabic_reshaper.ArabicReshaper(
        arabic_reshaper.config_for_true_type_font(
            "assets/fonts/urdu/Roboto_NotoNaskhArabic-Regular.ttf",
            arabic_reshaper.ENABLE_ALL_LIGATURES,
        )
    )
    reshaped_text = reshaper.reshape(text)
    return reshaped_text


def paragraph_transform_urdu(paragraph):
    # Inplace line reverser
    transformed_lines = []
    for line in paragraph.blPara.lines:
        if isinstance(line, tuple):
            transformed_lines.append(
                (line[0], get_display(" ".join(line[1])).split(" "))
            )
        elif isinstance(line, FragLine):
            for subline in line.words:
                subline.text = get_display(subline.text)
            transformed_lines.append(line)
        elif isinstance(line, ParaLines):
            for subline in line.words:
                subline.text = get_display(subline.text)
            transformed_lines.append(line)
        else:
            assert False, f"Unhandled line type {type(line)}"
    paragraph.blPara.lines = transformed_lines


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--language",
        default="en",
        choices={"en", "ur", "si", "ta"},
        help="Locale to generate the guide in",
    )
    args = parser.parse_args()

    # Default PDF page width will be same as A4, but height will be dependent
    # on the screenshot itself
    # Default margin is 0.5 inches
    MARGIN = inch * 0.5
    page_width, page_height = A4
    half_page_width = (page_width - 2 * MARGIN) / 2

    # Set text, alignment and font settings based on locale
    if args.language == "en":
        text_alignment = TA_LEFT
        text_transformer = lambda x: x
        paragraph_transformer = lambda x: x
        pdfmetrics.registerFont(
            TTFont("Font-light", "assets/fonts/roboto-android/Roboto-Light.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("Font-bold", "assets/fonts/roboto-android/Roboto-Bold.ttf")
        )
        column_1_offset = 0
        column_2_offset = half_page_width
    elif args.language == "ur":
        text_alignment = TA_RIGHT
        text_transformer = text_transform_urdu
        paragraph_transformer = paragraph_transform_urdu
        pdfmetrics.registerFont(
            TTFont("Font-light", "assets/fonts/urdu/Roboto_NotoNaskhArabic-Regular.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("Font-bold", "assets/fonts/urdu/Roboto_NotoNaskhArabic-Bold.ttf")
        )
        column_1_offset = half_page_width
        column_2_offset = 0
    elif args.language == "si":
        text_alignment = TA_LEFT
        text_transformer = lambda x: x
        paragraph_transformer = lambda x: x
        pdfmetrics.registerFont(
            TTFont("Font-light", "assets/fonts/sinhala/NotoSans_NotoSansSinhala-Light.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("Font-bold", "assets/fonts/sinhala/NotoSans_NotoSansSinhala-Bold.ttf")
        )
        column_1_offset = 0
        column_2_offset = half_page_width
    elif args.language == "ta":
        text_alignment = TA_LEFT
        text_transformer = lambda x: x
        paragraph_transformer = lambda x: x
        pdfmetrics.registerFont(
            TTFont("Font-light", "assets/fonts/tamil/NotoSans_NotoSansTamil-Light.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("Font-bold", "assets/fonts/tamil/NotoSans_NotoSansTamil-Bold.ttf")
        )
        column_1_offset = 0
        column_2_offset = half_page_width


    # Initialize Translation routines
    i18n.set("locale", args.language)
    i18n.load_path.append(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "translations")
    )
    i18n.set("filename_format", "{locale}.{format}")
    i18n.set("file_format", "json")
    _ = lambda text_id, prefix="": text_transformer(prefix + i18n.t(text_id))

    c = canvas.Canvas("test.pdf")

    heading_style = ParagraphStyle(
        name="headline",
        fontName="Font-bold",
        fontSize=30,
        textColor="#fca103",
        leading=34,
        alignment=text_alignment,
    )
    subheading_style = ParagraphStyle(
        name="subheading",
        fontName="Font-bold",
        fontSize=24,
        textColor="#333333",
        leading=28,
        alignment=text_alignment,
    )
    text_style = ParagraphStyle(
        name="text",
        fontName="Font-light",
        fontSize=16,
        textColor="#333333",
        leading=20,
        alignment=text_alignment,
    )
    bold_text_style = ParagraphStyle(
        name="text",
        fontName="Font-bold",
        fontSize=16,
        textColor="#333333",
        leading=20,
        alignment=text_alignment,
    )
    footnote_yellow_style = ParagraphStyle(
        name="footnote",
        fontName="Font-light",
        fontSize=12,
        textColor="#fca103",
        leading=16,
        alignment=text_alignment,
    )
    footnote_red_style = ParagraphStyle(
        name="footnote",
        fontName="Font-light",
        fontSize=12,
        textColor="#a30234",
        leading=16,
        alignment=text_alignment,
    )
    left_aligned_text_style = ParagraphStyle(
        name="text",
        fontName="Font-light",
        fontSize=16,
        textColor="#333333",
        leading=20,
        alignment=TA_LEFT,
    )

    content_width = half_page_width - inch * 0.2 - inch * 0.2

    # Cover page
    page_height = page_width
    c.setPageSize((page_width, page_height))

    # Draw background
    c.setStrokeColorRGB(163 / 255, 2 / 255, 52 / 255)
    c.setFillColorRGB(163 / 255, 2 / 255, 52 / 255)
    c.rect(
        MARGIN + column_1_offset,
        MARGIN,
        half_page_width,
        page_height - 2 * MARGIN,
        fill=1,
    )

    # Draw title
    p = Paragraph(_("main-title"), style=heading_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c, MARGIN + column_1_offset + inch * 0.2, page_height - MARGIN - eH - inch * 0.2
    )

    # Draw disclaimer
    p = Paragraph(_("disclaimer"), style=footnote_yellow_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(c, MARGIN + column_1_offset + inch * 0.2, MARGIN + inch * 0.2)

    # Draw cover text
    usedH = 0
    p = Paragraph(_("preparation-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(c, column_2_offset + MARGIN + inch * 0.2, page_height - MARGIN - eH)
    usedH = eH

    preparation_text = "".join(
        [
            _("time-text"),
            "<br/><br/>",
            "??? " + _("preparation-text-1") + "<br/>",
            "??? " + _("preparation-text-2") + "<br/>",
            "??? " + _("preparation-text-3") + "<br/>",
            "??? " + _("preparation-text-4") + "<br/>",
            "??? " + _("preparation-text-5") + "<br/>",
        ]
    )
    p = Paragraph(preparation_text, style=text_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c,
        column_2_offset + MARGIN + inch * 0.2,
        page_height - MARGIN - eH - usedH - inch * 0.2,
    )
    usedH += eH + inch * 0.5

    p = Paragraph(_("overview-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c,
        column_2_offset + MARGIN + inch * 0.2,
        page_height - MARGIN - eH - usedH - inch * 0.2,
    )
    usedH += eH + inch * 0.2

    preparation_text = "".join(
        ["??? " + _("overview-text-1") + "<br/>", "??? " + _("overview-text-2") + "<br/>",]
    )
    p = Paragraph(preparation_text, style=text_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c,
        column_2_offset + MARGIN + inch * 0.2,
        page_height - MARGIN - eH - usedH - inch * 0.2,
    )
    usedH += eH

    c.showPage()

    page_images = [
        f"assets/lowres-nas-page{page_number}.jpg" for page_number in range(1, 8)
    ] + [f"assets/lowres-portal-page{page_number}.jpg" for page_number in range(1, 7)]

    # Format: [(type, text)]
    page_texts = [
        [
            ("title", _("nas-title")),
            (
                "bullet",
                _("nas-page1-text1", prefix="??? ").replace(
                    "<NAS_URL>",
                    '<br/><a href="https://www.nas.gov.qa/self-service/" color="blue"> https://www.nas.gov.qa/ </a>',
                ),
            ),
            ("bullet", _("nas-page1-text2", prefix="??? ")),
            ("footnote", _("nas-page1-footnote")),
        ],
        [
            ("title", _("nas-title")),
            ("bullet", _("nas-page2-text1", prefix="??? ")),
            ("bullet", _("nas-page2-text2", prefix="??? ")),
        ],
        [
            ("title", _("nas-title")),
            ("bullet", _("nas-page3-text1", prefix="??? ")),
            ("bullet", _("nas-page3-text2", prefix="??? ")),
            ("bullet", _("nas-page3-text3", prefix="??? ")),
            ("bullet", _("nas-page3-text4", prefix="??? ")),
        ],
        [
            ("title", _("nas-title")),
            ("bullet", _("nas-page4-text1", prefix="??? ")),
            ("bullet", _("nas-page4-text2", prefix="??? ")),
        ],
        [
            ("title", _("nas-title")),
            ("bullet", _("nas-page5-text1", prefix="??? ")),
            ("bullet", _("nas-page5-text2", prefix="??? ")),
            ("bullet", _("nas-page5-text3", prefix="??? ")),
            ("bullet", _("nas-page5-text4", prefix="??? ")),
            ("bullet", _("nas-page5-text5", prefix="??? ")),
            ("bullet", _("nas-page5-text6", prefix="??? ")),
            ("bullet", _("nas-page5-text7", prefix="??? ")),
            ("bullet", _("nas-page5-text8", prefix="??? ")),
            ("bullet", _("nas-page5-text9", prefix="??? ")),
            ("bullet", _("nas-page5-text10", prefix="??? ")),
            ("bullet", _("nas-page5-text11", prefix="??? ")),
            ("bullet", _("nas-page5-text12", prefix="??? ")),
        ],
        [
            ("title", _("nas-title")),
            ("bullet", _("nas-page6-text1", prefix="??? ")),
            ("bullet", _("nas-page6-text2", prefix="??? ")),
            ("bullet", _("nas-page6-text3", prefix="??? ")),
        ],
        [
            ("title", _("nas-title")),
            ("bullet", _("nas-page7-text1", prefix="??? ")),
            ("footnote", _("nas-page7-footnote")),
        ],
        [
            ("title", _("vaccineportal-title")),
            (
                "bullet",
                _("vaccineportal-page1-text1", prefix="??? ").replace(
                    "<PORTAL_URL>",
                    '<a href="http://app-covid19.moph.gov.qa" color="blue">http://app-covid19.moph.gov.qa</a>',
                ),
            ),
            ("bullet", _("vaccineportal-page1-text2", prefix="??? ")),
            ("footnote", _("vaccineportal-page1-footnote")),
        ],
        [
            ("title", _("vaccineportal-title")),
            ("bullet", _("vaccineportal-page2-text1", prefix="??? ")),
            ("bullet", _("vaccineportal-page2-text2", prefix="??? ")),
            ("bullet", _("vaccineportal-page2-text3", prefix="??? ")),
        ],
        [
            ("title", _("vaccineportal-title")),
            ("bullet", _("vaccineportal-page3-text1", prefix="??? ")),
            ("bullet", _("vaccineportal-page3-text2", prefix="??? ")),
            ("bullet", _("vaccineportal-page3-text3", prefix="??? ")),
            ("bullet", _("vaccineportal-page3-text4", prefix="??? ")),
        ],
        [
            ("title", _("vaccineportal-title")),
            ("bullet", _("vaccineportal-page4-text1", prefix="??? ")),
            ("bullet", _("vaccineportal-page4-text2", prefix="??? ")),
            ("bullet", _("vaccineportal-page4-text3", prefix="??? ")),
            ("bullet", _("vaccineportal-page4-text4", prefix="??? ")),
            ("bullet", _("vaccineportal-page4-text5", prefix="??? ")),
        ],
        [
            ("title", _("vaccineportal-title")),
            ("bullet", _("vaccineportal-page5-text1", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text2", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text3", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text4", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text5", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text6", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text7", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text8", prefix="??? ")),
            ("bullet", _("vaccineportal-page5-text9", prefix="??? ")),
            ("footnote", _("vaccineportal-page5-footnote")),
        ],
        [
            ("title", _("vaccineportal-title")),
            ("bullet", _("vaccineportal-page6-text1", prefix="??? ")),
        ],
    ]

    for page_idx, page_image in enumerate(page_images):
        page_screenshot = Image.open(page_image)
        screenshot_width, screenshot_height = page_screenshot.size
        resize_ratio = (half_page_width) / screenshot_width

        page_height = screenshot_height * resize_ratio + MARGIN * 2
        c.setPageSize((page_width, page_height))

        # draw screenshot
        c.drawInlineImage(
            page_screenshot,
            MARGIN + column_1_offset,
            MARGIN,
            half_page_width,
            page_height - 2 * MARGIN,
            preserveAspectRatio=True,
        )

        # Draw texts
        print(f"Processing page {page_idx+1}")
        usedH = MARGIN
        for text_type, text in page_texts[page_idx]:
            if text_type == "title":
                p = Paragraph(text, style=subheading_style)
                eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
                paragraph_transformer(p)
                y = page_height - usedH - eH
                usedH += eH + 0.2 * inch
            elif text_type == "bullet":
                p = Paragraph(text, style=text_style)
                eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
                paragraph_transformer(p)
                y = page_height - usedH - eH
                usedH += eH + 0.1 * inch
            elif text_type == "footnote":
                p = Paragraph(text, style=footnote_red_style)
                eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
                paragraph_transformer(p)
                y = MARGIN + inch * 0.2
                usedH += eH

            p.drawOn(c, column_2_offset + MARGIN + inch * 0.2, y)

        c.showPage()

    # End Page
    page_height = page_width
    c.setPageSize((page_width, page_height))
    c.setStrokeColorRGB(163 / 255, 2 / 255, 52 / 255)
    c.setFillColorRGB(163 / 255, 2 / 255, 52 / 255)
    c.rect(
        MARGIN + column_1_offset,
        MARGIN,
        half_page_width,
        page_height - 2 * MARGIN,
        fill=1,
    )
    p = Paragraph(_("end-title"), style=heading_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c, MARGIN + column_1_offset + inch * 0.2, page_height - MARGIN - eH - inch * 0.2
    )

    p = Paragraph(
        f"v{datetime.datetime.now().strftime('%Y%m%d')}", style=footnote_yellow_style
    )
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(c, MARGIN + column_1_offset + inch * 0.2, MARGIN + inch * 0.2)

    usedH = 0
    p = Paragraph(_("contributors-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(c, column_2_offset + MARGIN + inch * 0.2, page_height - MARGIN - eH)
    usedH = eH

    preparation_text = "".join(
        [
            "??? " + _(f"{contributer} ({','.join(contributions)})") + "<br/>"
            for contributer, contributions in sorted(CONTRIBUTERS, key=lambda x: x[0])
        ]
    )
    p = Paragraph(preparation_text, style=left_aligned_text_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c,
        column_2_offset + MARGIN + inch * 0.2,
        page_height - MARGIN - eH - usedH - inch * 0.2,
    )
    usedH += eH + inch * 0.5

    p = Paragraph(_("created-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c,
        column_2_offset + MARGIN + inch * 0.2,
        page_height - MARGIN - eH - usedH - inch * 0.2,
    )
    usedH += eH + inch * 0.2

    p = Paragraph("Fahim Dalvi", style=text_style)
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c,
        column_2_offset + MARGIN + inch * 0.2,
        page_height - MARGIN - eH - usedH - inch * 0.2,
    )
    usedH += eH + inch * 0.2

    p = Paragraph(
        _("contribution-note").replace(
            "<CONTACT_EMAIL>",
            '<a href="mailto:fdalvi.vaccine.guide@protonmail.com" color="blue">fdalvi.vaccine.guide@protonmail.com</a>',
        ),
        style=footnote_red_style,
    )
    eW, eH = p.wrap(content_width, page_height - 2 * MARGIN)
    paragraph_transformer(p)
    p.drawOn(
        c,
        column_2_offset + MARGIN + inch * 0.2,
        page_height - MARGIN - eH - usedH - inch * 0.2,
    )
    usedH += eH

    c.showPage()

    c.save()


if __name__ == "__main__":
    main()
