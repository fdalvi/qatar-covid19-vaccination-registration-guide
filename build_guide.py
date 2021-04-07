import argparse
import pdfkit
import datetime
from yattag import Doc

from PIL import Image
from PyPDF2 import PdfFileMerger

import io
import i18n
import os

HINDI_TRANFORMS = {
    'के ': 'के ',
    'र्क ': 'र्क '
}

CONTRIBUTERS = [
    ("Anthony Wanyoike Peter", ["Portal screenshots"]),
    ("Imaduddin Ahmad Dalvi", ["Urdu translation"]),
    ("Ranjanas Vadivel", ["Sinhala and Tamil translation"]),
    ("Paul Mary Ranjanas", ["Sinhala and Tamil translation"]),
    ("Nadir Durrani", ["Urdu translation"]),
    ("Lamana Mulaffer", ["Sinhala and Tamil translation"]),
    ("Nijla Mulaffer", ["Sinhala and Tamil translation"])
]

def render_cover_page(translation, doc_style):
    print(f"Processing page 1")
    page_width = 8.27
    page_height = page_width
    MARGIN = 0.5
    BUFFER = 0.1
    half_page_width = (page_width - 2 * MARGIN) / 2
    column_1_offset = 0
    column_2_offset = half_page_width

    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('style'):
                doc.asis(doc_style)
        with tag('body'):
            with tag('div', style="display: -webkit-box; display: flex; flex-direction: row"):
                with tag('div', style=f"width: 49%; height: {(page_height-2*MARGIN)}in; background-color: #a30234;"):
                    with tag('p', style=f"padding: 0.2in;", klass="heading"):
                        text(translation('main-title'))
                    with tag('p', style=f"padding: 0.2in; position:absolute; bottom: 0px; width: 40%;", klass="footnote-yellow"):
                        text(translation('disclaimer'))
                        
                with tag('div', style=f"width: 49%; height: {(page_height-2*MARGIN)}in;"):
                    with tag('p', style="margin: 0 0.2in;", klass="subheading"):
                        text(translation('preparation-title'))
                    doc.stag('br')
                    with tag('p', style="margin: 0 0.2in;", klass="text"):
                        text(translation('time-text'))
                    doc.stag('br')
                    with tag('ul', style="margin: 0 0.2in;", klass="text"):
                        for prep_text_idx in range(1, 6):
                            with tag('li'):
                                text(translation(f'preparation-text-{prep_text_idx}'))
                    doc.stag('br')
                    with tag('p', style="margin: 0 0.2in;", klass="subheading"):
                        text(translation('overview-title'))
                    doc.stag('br')
                    with tag('ul', style="margin: 0 0.2in;", klass="text"):
                        for prep_text_idx in range(1, 3):
                            with tag('li'):
                                text(translation(f'overview-text-{prep_text_idx}'))
    
    options = {
        'page-width': f'{page_width}in',
        'page-height': f'{page_height+BUFFER}in',
        'margin-top': f'{MARGIN}in',
        'margin-right': f'{MARGIN}in',
        'margin-bottom': f'{MARGIN}in',
        'margin-left': f'{MARGIN}in',
        'encoding': "UTF-8",
        'disable-smart-shrinking': None,
        'user-style-sheet': 'main.css',
        'enable-local-file-access': None,
        'quiet': None
    }

    # with open('out.html', 'w') as fp:
    #     fp.write(doc.getvalue())

    return pdfkit.from_string(doc.getvalue(), False, options=options)

def render_guide_pages(translation, doc_style):
    # Define page data
    page_images = [
        f"assets/lowres-nas-page{page_number}.jpg" for page_number in range(1, 8)
    ] + [f"assets/lowres-portal-page{page_number}.jpg" for page_number in range(1, 7)]

    # Format: [(type, text)]
    page_texts = [
        [
            ("title", translation("nas-title")),
            (
                "bullet",
                translation("nas-page1-text1").replace(
                    "<NAS_URL>",
                    '<a href="https://www.nas.gov.qa/self-service/" color="blue"> https://www.nas.gov.qa </a>',
                ),
            ),
            ("bullet", translation("nas-page1-text2")),
            ("footnote", translation("nas-page1-footnote")),
        ],
        [
            ("title", translation("nas-title")),
            ("bullet", translation("nas-page2-text1")),
            ("bullet", translation("nas-page2-text2")),
        ],
        [
            ("title", translation("nas-title")),
            ("bullet", translation("nas-page3-text1")),
            ("bullet", translation("nas-page3-text2")),
            ("bullet", translation("nas-page3-text3")),
            ("bullet", translation("nas-page3-text4")),
        ],
        [
            ("title", translation("nas-title")),
            ("bullet", translation("nas-page4-text1")),
            ("bullet", translation("nas-page4-text2")),
        ],
        [
            ("title", translation("nas-title")),
            ("bullet", translation("nas-page5-text1")),
            ("bullet", translation("nas-page5-text2")),
            ("bullet", translation("nas-page5-text3")),
            ("bullet", translation("nas-page5-text4")),
            ("bullet", translation("nas-page5-text5")),
            ("bullet", translation("nas-page5-text6")),
            ("bullet", translation("nas-page5-text7")),
            ("bullet", translation("nas-page5-text8")),
            ("bullet", translation("nas-page5-text9")),
            ("bullet", translation("nas-page5-text10")),
            ("bullet", translation("nas-page5-text11")),
            ("bullet", translation("nas-page5-text12")),
        ],
        [
            ("title", translation("nas-title")),
            ("bullet", translation("nas-page6-text1")),
            ("bullet", translation("nas-page6-text2")),
            ("bullet", translation("nas-page6-text3")),
        ],
        [
            ("title", translation("nas-title")),
            ("bullet", translation("nas-page7-text1")),
            ("footnote", translation("nas-page7-footnote")),
        ],
        [
            ("title", translation("vaccineportal-title")),
            (
                "bullet",
                translation("vaccineportal-page1-text1").replace(
                    "<PORTAL_URL>",
                    '<a href="http://app-covid19.moph.gov.qa" color="blue">http://app-covid19.moph.gov.qa</a>',
                ),
            ),
            ("bullet", translation("vaccineportal-page1-text2")),
            ("footnote", translation("vaccineportal-page1-footnote")),
        ],
        [
            ("title", translation("vaccineportal-title")),
            ("bullet", translation("vaccineportal-page2-text1")),
            ("bullet", translation("vaccineportal-page2-text2")),
            ("bullet", translation("vaccineportal-page2-text3")),
        ],
        [
            ("title", translation("vaccineportal-title")),
            ("bullet", translation("vaccineportal-page3-text1")),
            ("bullet", translation("vaccineportal-page3-text2")),
            ("bullet", translation("vaccineportal-page3-text3")),
            ("bullet", translation("vaccineportal-page3-text4")),
        ],
        [
            ("title", translation("vaccineportal-title")),
            ("bullet", translation("vaccineportal-page4-text1")),
            ("bullet", translation("vaccineportal-page4-text2")),
            ("bullet", translation("vaccineportal-page4-text3")),
            ("bullet", translation("vaccineportal-page4-text4")),
            ("bullet", translation("vaccineportal-page4-text5")),
        ],
        [
            ("title", translation("vaccineportal-title")),
            ("bullet", translation("vaccineportal-page5-text1")),
            ("bullet", translation("vaccineportal-page5-text2")),
            ("bullet", translation("vaccineportal-page5-text3")),
            ("bullet", translation("vaccineportal-page5-text4")),
            ("bullet", translation("vaccineportal-page5-text5")),
            ("bullet", translation("vaccineportal-page5-text6")),
            ("bullet", translation("vaccineportal-page5-text7")),
            ("bullet", translation("vaccineportal-page5-text8")),
            ("bullet", translation("vaccineportal-page5-text9")),
            ("footnote", translation("vaccineportal-page5-footnote")),
        ],
        [
            ("title", translation("vaccineportal-title")),
            ("bullet", translation("vaccineportal-page6-text1")),
        ],
    ]

    page_width = 8.27
    MARGIN = 0.5
    BUFFER = 0.1
    half_page_width = (page_width - 2 * MARGIN) * 0.485

    page_pdfs = []
    for page_idx, page_image in enumerate(page_images):
        print(f"Processing page {page_idx+2}")
        page_screenshot = Image.open(page_image)
        screenshot_width, screenshot_height = page_screenshot.size
        resize_ratio = half_page_width / screenshot_width

        page_height = screenshot_height * resize_ratio + MARGIN * 2 + 1

        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                with tag('style'):
                    doc.asis(doc_style)
            with tag('body'):
                with tag('div', style="display: -webkit-box; display: flex; flex-direction: row"):
                    with tag('div', style=f"width: 49%; height: {(page_height-2*MARGIN)}in;"):
                        doc.stag('img', src=os.path.abspath(page_image))
                    with tag('div', style=f"width: 49%; height: {(page_height-2*MARGIN)}in;"):
                        titles = [x for x in page_texts[page_idx] if x[0] == 'title']
                        
                        for _, text_snippet in titles:
                            with tag('h2', style="margin: 0 0.2in;", klass="subheading"):
                                doc.asis(text_snippet)

                        bullets = [x for x in page_texts[page_idx] if x[0] == 'bullet']
                        with tag('ul', klass="text"):
                            for _, text_snippet in bullets:
                                with tag('li', style="margin: 0 0.2in;", klass="text"):
                                    doc.asis(text_snippet)

                        footnotes = [x for x in page_texts[page_idx] if x[0] == 'footnote']
                        for _, text_snippet in footnotes:
                            with tag('p', style="margin: 0 0.2in; position:absolute; bottom: 6px; width: 40%;", klass="footnote-red"):
                                doc.asis(text_snippet)
    
        options = {
            'page-width': f'{page_width}in',
            'page-height': f'{page_height+BUFFER}in',
            'margin-top': f'{MARGIN}in',
            'margin-right': f'{MARGIN}in',
            'margin-bottom': f'{MARGIN}in',
            'margin-left': f'{MARGIN}in',
            'encoding': "UTF-8",
            'disable-smart-shrinking': None,
            'user-style-sheet': 'main.css',
            'enable-local-file-access': None,
            'quiet': None
        }

        page_pdfs.append(pdfkit.from_string(doc.getvalue(), False, options=options))
    return page_pdfs

def render_contributers_page(translation, doc_style):
    print(f"Processing contributers page")
    page_width = 8.27
    page_height = page_width
    MARGIN = 0.5
    BUFFER = 0.1
    half_page_width = (page_width - 2 * MARGIN) / 2
    column_1_offset = 0
    column_2_offset = half_page_width

    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('style'):
                doc.asis(doc_style)
        with tag('body'):
            with tag('div', style="display: -webkit-box; display: flex; flex-direction: row"):
                with tag('div', style=f"width: 49%; height: {(page_height-2*MARGIN)}in; background-color: #a30234;"):
                    with tag('h1', style=f"padding: 0.2in;", klass="heading"):
                        text(translation('end-title'))
                    with tag('p', style=f"padding: 0.2in; position:absolute; bottom: 0px; width: 40%;", klass="footnote-yellow"):
                        text(f"v{datetime.datetime.now().strftime('%Y%m%d')}")
                        
                with tag('div', style=f"width: 49%; height: {(page_height-2*MARGIN)}in;"):
                    with tag('h2', style="margin: 0 0.2in;", klass="subheading"):
                        text(translation('contributors-title'))
                    doc.stag('br')
                    with tag('ul', style="margin: 0 0.2in; direction: ltr;", klass="text"):
                        for contributer, contributions in sorted(CONTRIBUTERS, key=lambda x: x[0]):
                            with tag('li'):
                                text(translation(f"{contributer} ({','.join(contributions)})"))
                    doc.stag('br')
                    with tag('h2', style="margin: 0 0.2in;", klass="subheading"):
                        text(translation('created-title'))
                    doc.stag('br')
                    with tag('p', style="margin: 0 0.2in; direction: ltr;", klass="text"):
                        text("Fahim Dalvi")
                    doc.stag('br')
                    with tag('p', style="margin: 0 0.2in;", klass="footnote-red"):
                        doc.asis(translation("contribution-note").replace(
                            "<CONTACT_EMAIL>",
                            '<a href="mailto:fdalvi.vaccine.guide@protonmail.com" color="blue">fdalvi.vaccine.guide@protonmail.com</a>'))
    
    options = {
        'page-width': f'{page_width}in',
        'page-height': f'{page_height+BUFFER}in',
        'margin-top': f'{MARGIN}in',
        'margin-right': f'{MARGIN}in',
        'margin-bottom': f'{MARGIN}in',
        'margin-left': f'{MARGIN}in',
        'encoding': "UTF-8",
        'disable-smart-shrinking': None,
        'user-style-sheet': 'main.css',
        'enable-local-file-access': None,
        'quiet': None
    }

    return pdfkit.from_string(doc.getvalue(), False, options=options)

def text_transformer(text, transforms):
    for k, v in transforms.items():
        text = text.replace(k, v)
    return text

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--language",
        default="en",
        choices={"en", "ur", "si", "ta", "hi"},
        help="Locale to generate the guide in",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output pdf name",
    )
    args = parser.parse_args()

    # Initialize Translation routines
    i18n.set("locale", args.language)
    i18n.load_path.append(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "translations")
    )
    i18n.set("filename_format", "{locale}.{format}")
    i18n.set("file_format", "json")
    translation = lambda text_id: i18n.t(text_id)

    if args.language == 'en':
        doc_style = '''
        @font-face {
            font-family: 'LightFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/roboto-android/Roboto-Light.ttf')}");
        ''' + '''
            font-weight: 200;
        }

        @font-face {
            font-family: 'BoldFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/roboto-android/Roboto-Bold.ttf')}");
        ''' + '''
        }
        '''
    elif args.language == 'ur':
        doc_style = '''
        @font-face {
            font-family: 'LightFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/urdu/Roboto_NotoNaskhArabic-Regular.ttf')}");
        ''' + '''
            font-weight: 200;
        }

        @font-face {
            font-family: 'BoldFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/urdu/Roboto_NotoNaskhArabic-Bold.ttf')}");
        ''' + '''
        }

        body {
            direction: rtl;
        }
        '''
    elif args.language == 'ta':
        doc_style = '''
        @font-face {
            font-family: 'LightFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/tamil/NotoSans_NotoSansTamil-Light.ttf')}");
        ''' + '''
            font-weight: 200;
        }

        @font-face {
            font-family: 'BoldFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/tamil/NotoSans_NotoSansTamil-Bold.ttf')}");
        ''' + '''
        }

        .heading {
            font-size: 36px;
            line-height: 40px;
        }

        .subheading {
            font-size: 26px;
            line-height: 30px;
        }

        .text {
            font-size: 18px;
            line-height: 22px;
            font-weight: 200;
        }

        .footnote-yellow {
            font-size: 14px;
            line-height: 18px;
            font-weight: 100;
        }

        .footnote-red {
            color: #a30234;
            font-family: 'LightFont';
            font-size: 14px;
            line-height: 18px;
            font-weight: 100;
        }
        '''
    elif args.language == 'si':
        doc_style = '''
        @font-face {
            font-family: 'LightFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/sinhala/NotoSans_NotoSansSinhala-Light.ttf')}");
        ''' + '''
            font-weight: 200;
        }

        @font-face {
            font-family: 'BoldFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/sinhala/NotoSans_NotoSansSinhala-Bold.ttf')}");
        ''' + '''
        }

        .heading {
            font-size: 36px;
            line-height: 40px;
        }

        .subheading {
            font-size: 26px;
            line-height: 30px;
        }

        .text {
            font-size: 18px;
            line-height: 22px;
            font-weight: 200;
        }

        .footnote-yellow {
            font-size: 14px;
            line-height: 18px;
            font-weight: 100;
        }

        .footnote-red {
            color: #a30234;
            font-family: 'LightFont';
            font-size: 14px;
            line-height: 18px;
            font-weight: 100;
        }
        '''
    elif args.language == 'hi':
        doc_style = '''
        @font-face {
            font-family: 'LightFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/hindi/NotoSans_NotoSansDevanagari-Light.ttf')}");
        ''' + '''
            font-weight: 200;
        }

        @font-face {
            font-family: 'BoldFont';
        ''' + f'''
            src: url("{os.path.abspath('assets/fonts/hindi/NotoSans_NotoSansDevanagari-Bold.ttf')}");
        ''' + '''
        }
        '''

        translation = lambda text_id: text_transformer(i18n.t(text_id), HINDI_TRANFORMS)

    cover_pdf = render_cover_page(translation, doc_style)
    guide_pdfs = render_guide_pages(translation, doc_style)
    contributers_pdf = render_contributers_page(translation, doc_style)

    merger = PdfFileMerger()
    for page in [cover_pdf] + guide_pdfs + [contributers_pdf]:
        merger.append(io.BytesIO(page), import_bookmarks=False)
    merger.write(args.output)
    merger.close()

if __name__ == '__main__':
    main()