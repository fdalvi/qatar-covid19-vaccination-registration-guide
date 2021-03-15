import datetime
import i18n
import os

from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch    
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def main():
    # Default PDF page width will be same as A4, but height will be dependent
    # on the screenshot itself
    # Default margin is 0.5 inches
    MARGIN = inch*.5
    page_width, page_height = A4
    half_page_width = (page_width-2*MARGIN)/2

    i18n.load_path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'translations'))
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set('file_format', 'json')
    
    c = canvas.Canvas("test.pdf")

    pdfmetrics.registerFont(TTFont('Roboto-light', 'assets/fonts/roboto-android/Roboto-Light.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-bold', 'assets/fonts/roboto-android/Roboto-Bold.ttf'))
    # pdfmetrics.registerFont(TTFont('Times', 'times.ttf',))
    # pdfmetrics.registerFont(TTFont('Timesi', 'timesi.ttf',))
    # pdfmetrics.registerFont(TTFont('Timesbd', 'timesbd.ttf',))
    # pdfmetrics.registerFontFamily('Times',normal='Times',bold='Timesbd',
    # italic='Timesi',)

    heading_style = ParagraphStyle(name="headline", fontName="Roboto-bold", fontSize=30, textColor="#fca103", leading=34)
    subheading_style = ParagraphStyle(name="subheading", fontName="Roboto-bold", fontSize=24, textColor="#333333", leading=28)
    text_style = ParagraphStyle(name="text", fontName="Roboto-light", fontSize=16, textColor="#333333", leading=20)
    bold_text_style = ParagraphStyle(name="text", fontName="Roboto-bold", fontSize=16, textColor="#333333", leading=20)
    footnote_yellow_style = ParagraphStyle(name="footnote", fontName="Roboto-light", fontSize=12, textColor="#fca103", leading=16)
    footnote_red_style = ParagraphStyle(name="footnote", fontName="Roboto-light", fontSize=12, textColor="#a30234", leading=16)

    content_width = half_page_width - inch*0.2 - inch*0.2

    # Cover page
    page_height = page_width
    c.setPageSize((page_width, page_height))
    c.setStrokeColorRGB(163/255, 2/255, 52/255)
    c.setFillColorRGB(163/255, 2/255, 52/255)
    c.rect(MARGIN, MARGIN, half_page_width, page_height-2*MARGIN, fill=1)
    p = Paragraph(i18n.t("main-title"), style=heading_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, MARGIN + inch*0.2, page_height - MARGIN - eH - inch*0.2)

    p = Paragraph(i18n.t("disclaimer"), style=footnote_yellow_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, MARGIN + inch*0.2,  MARGIN + inch*0.2)

    usedH = 0
    p = Paragraph(i18n.t("preparation-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH)
    usedH = eH

    preparation_text = "".join([
        i18n.t("time-text"),
        "<br/><br/>",
        "• " + i18n.t("preparation-text-1") + "<br/>",
        "• " + i18n.t("preparation-text-2") + "<br/>",
        "• " + i18n.t("preparation-text-3") + "<br/>",
        "• " + i18n.t("preparation-text-4") + "<br/>",
        "• " + i18n.t("preparation-text-5") + "<br/>",
    ])
    p = Paragraph(preparation_text, style=text_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH - usedH - inch*0.2)
    usedH += eH + inch * 0.5

    p = Paragraph(i18n.t("overview-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH - usedH - inch*0.2)
    usedH += eH + inch * 0.2

    preparation_text = "".join([
        "• " + i18n.t("overview-text-1") + "<br/>",
        "• " + i18n.t("overview-text-2") + "<br/>",
    ])
    p = Paragraph(preparation_text, style=text_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH - usedH - inch*0.2)
    usedH += eH

    c.showPage()

    # Format: [type, text, vertical offset]
    page_images = [f"assets/lowres-nas-page{page_number}.jpg" for page_number in range(1,8)] \
        + [f"assets/lowres-portal-page{page_number}.jpg" for page_number in range(1,7)]
    page_texts = [
        [
            ("title", i18n.t("nas-title"), 0),
            ("bullet", i18n.t("nas-page1-text1").replace("<NAS_URL>", "<a href=\"https://www.nas.gov.qa/self-service/\" color=\"blue\">https://www.nas.gov.qa/self-service/</a>"), 0),
            ("bullet", i18n.t("nas-page1-text2"), 0),
            ("footnote", i18n.t("nas-page1-footnote"), 0)
        ],
        [
            ("title", i18n.t("nas-title"), 0),
            ("bullet", i18n.t("nas-page2-text1"), 0),
            ("bullet", i18n.t("nas-page2-text2"), 0)
        ],
        [
            ("title", i18n.t("nas-title"), 0),
            ("bullet", i18n.t("nas-page3-text1"), 0),
            ("bullet", i18n.t("nas-page3-text2"), 0),
            ("bullet", i18n.t("nas-page3-text3"), 0),
            ("bullet", i18n.t("nas-page3-text4"), 0)
        ],
        [
            ("title", i18n.t("nas-title"), 0),
            ("bullet", i18n.t("nas-page4-text1"), 0),
            ("bullet", i18n.t("nas-page4-text2"), 0),
        ],
        [
            ("title", i18n.t("nas-title"), 0),
            ("bullet", i18n.t("nas-page5-text1"), 0),
            ("bullet", i18n.t("nas-page5-text2"), 0),
            ("bullet", i18n.t("nas-page5-text3"), 0),
            ("bullet", i18n.t("nas-page5-text4"), 0),
            ("bullet", i18n.t("nas-page5-text5"), 0),
            ("bullet", i18n.t("nas-page5-text6"), 0),
            ("bullet", i18n.t("nas-page5-text7"), 0),
            ("bullet", i18n.t("nas-page5-text8"), 0),
            ("bullet", i18n.t("nas-page5-text9"), 0),
            ("bullet", i18n.t("nas-page5-text10"), 0),
            ("bullet", i18n.t("nas-page5-text11"), 0),
            ("bullet", i18n.t("nas-page5-text12"), 0),
        ],
        [
            ("title", i18n.t("nas-title"), 0),
            ("bullet", i18n.t("nas-page6-text1"), 0),
            ("bullet", i18n.t("nas-page6-text2"), 0),
            ("bullet", i18n.t("nas-page6-text3"), 0),
        ],
        [
            ("title", i18n.t("nas-title"), 0),
            ("bullet", i18n.t("nas-page7-text1"), 0),
            ("footnote", i18n.t("nas-page7-footnote"), 0)
        ],
        [
            ("title", i18n.t("vaccineportal-title"), 0),
            ("bullet", i18n.t("vaccineportal-page1-text1").replace("<PORTAL_URL>", "<a href=\"http://app-covid19.moph.gov.qa\" color=\"blue\">http://app-covid19.moph.gov.qa</a>"), 0),
            ("bullet", i18n.t("vaccineportal-page1-text2"), 0),
            ("footnote", i18n.t("vaccineportal-page1-footnote"), 0)
        ],
        [
            ("title", i18n.t("vaccineportal-title"), 0),
            ("bullet", i18n.t("vaccineportal-page2-text1"), 0),
            ("bullet", i18n.t("vaccineportal-page2-text2"), 0),
            ("bullet", i18n.t("vaccineportal-page2-text3"), 0)
        ],
        [
            ("title", i18n.t("vaccineportal-title"), 0),
            ("bullet", i18n.t("vaccineportal-page3-text1"), 0),
            ("bullet", i18n.t("vaccineportal-page3-text2"), 0),
            ("bullet", i18n.t("vaccineportal-page3-text3"), 0),
            ("bullet", i18n.t("vaccineportal-page3-text4"), 0)
        ],
        [
            ("title", i18n.t("vaccineportal-title"), 0),
            ("bullet", i18n.t("vaccineportal-page4-text1"), 0),
            ("bullet", i18n.t("vaccineportal-page4-text2"), 0),
            ("bullet", i18n.t("vaccineportal-page4-text3"), 0),
            ("bullet", i18n.t("vaccineportal-page4-text4"), 0),
            ("bullet", i18n.t("vaccineportal-page4-text5"), 0)
        ],
        [
            ("title", i18n.t("vaccineportal-title"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text1"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text2"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text3"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text4"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text5"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text6"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text7"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text8"), 0),
            ("bullet", i18n.t("vaccineportal-page5-text9"), 0),
            ("footnote", i18n.t("vaccineportal-page5-footnote"), 0)
        ],
        [
            ("title", i18n.t("vaccineportal-title"), 0),
            ("bullet", i18n.t("vaccineportal-page6-text1"), 0)
        ],
    ]
    
    for page_idx, page_image in enumerate(page_images):
        page_screenshot = Image.open(page_image)
        screenshot_width, screenshot_height = page_screenshot.size
        resize_ratio =  (half_page_width) / screenshot_width

        page_height = screenshot_height * resize_ratio + MARGIN*2
        c.setPageSize((page_width, page_height))

        # draw screenshot
        c.drawInlineImage(page_screenshot, MARGIN, MARGIN, half_page_width, page_height-2*MARGIN, preserveAspectRatio=True)

        # Draw texts
        print(f"Page {page_idx}")
        usedH = MARGIN
        for text_type, text, offset in page_texts[page_idx]:
            if text_type == "title":
                p = Paragraph(text, style=subheading_style)
                eW, eH = p.wrap(content_width, page_height-2*MARGIN)
                y = page_height - usedH - offset - eH
                usedH += eH + 0.2 * inch
            elif text_type == "bullet":
                p = Paragraph("• " + text, style=text_style)
                eW, eH = p.wrap(content_width, page_height-2*MARGIN)
                y = page_height - usedH - offset - eH
                usedH += eH + 0.1 * inch
            elif text_type == "footnote":
                p = Paragraph(text, style=footnote_red_style)
                eW, eH = p.wrap(content_width, page_height-2*MARGIN)
                y = MARGIN + inch*0.2 - offset
                usedH += eH
            print(f"{eW} {eH} {usedH}")
            

            p.drawOn(c, half_page_width + MARGIN + inch*0.2, y)
            
        
        c.showPage()

    # End Page
    page_height = page_width
    c.setPageSize((page_width, page_height))
    c.setStrokeColorRGB(163/255, 2/255, 52/255)
    c.setFillColorRGB(163/255, 2/255, 52/255)
    c.rect(MARGIN, MARGIN, half_page_width, page_height-2*MARGIN, fill=1)
    p = Paragraph(i18n.t("end-title"), style=heading_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, MARGIN + inch*0.2, page_height - MARGIN - eH - inch*0.2)

    p = Paragraph(f"v{datetime.datetime.now().strftime('%Y%m%d')}", style=footnote_yellow_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, MARGIN + inch*0.2,  MARGIN + inch*0.2)

    usedH = 0
    p = Paragraph(i18n.t("contributors-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH)
    usedH = eH

    preparation_text = "".join([
        "• " + i18n.t("Anthony Wanyoike Peter (Portal screenshots)") + "<br/>",
    ])
    p = Paragraph(preparation_text, style=text_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH - usedH - inch*0.2)
    usedH += eH + inch * 0.5

    p = Paragraph(i18n.t("created-title"), style=subheading_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH - usedH - inch*0.2)
    usedH += eH + inch * 0.2

    p = Paragraph("Fahim Dalvi", style=text_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH - usedH - inch*0.2)
    usedH += eH + inch * 0.2

    p = Paragraph(i18n.t("contribution-note").replace("<CONTACT_EMAIL>", "<a href=\"mailto:fdalvi.vaccine.guide@protonmail.com\" color=\"blue\">fdalvi.vaccine.guide@protonmail.com</a>"), style=footnote_red_style)
    eW, eH = p.wrap(content_width, page_height-2*MARGIN)
    p.drawOn(c, half_page_width + MARGIN + inch*0.2, page_height - MARGIN - eH - usedH - inch*0.2)
    usedH += eH

    c.showPage()

    c.save()


if __name__ == "__main__":
    main()