import itertools
import re
from io import BytesIO

import bs4
import fitz
import requests
from PIL import Image, ImageDraw, ImageFont

from source.exceptions.page_exceptions import PageException
from source.models.Arabic_Fonts.fonts import fonts
from source.services.layouts import layout_mapping, LayoutEnum, layout_paragraphs

align_param = 2


class Aradocgen:
    def generate_pdf(self, font_type, url, layout_number, n_pages=10, font_size=12):
        doc = fitz.open()  # open the document
        title, content_blocks, n_paragraphs = self.extract_content_from_website(url)
        layout_key = LayoutEnum(layout_number)
        layout_key_string = layout_key.name
        if layout_key_string in layout_paragraphs:
            try:
                if n_paragraphs < layout_paragraphs[layout_key_string]:
                    raise PageException("number of pages very low", 505)
            except KeyError:
                raise PageException("number of pages very low")

        layout_function = layout_mapping[layout_key]
        layout_function(self, n_pages, doc, title, font_type, font_size, content_blocks, n_paragraphs)

        out = fitz.open()  # output PDF
        out_buffer = self.non_searchable(doc, out)
        self.save(doc)

        return out_buffer

    def get_available(self):
        available_fonts = [
            "Advertising Bold",
            "Af-Diwani",
            "Andalus",
            "Arabic transparent",
            "Arslan Wessam A",
            "Decotype Thuluth",
            "M-Unicode Sara",
            "Decotype Naskh",
            "Simplified Arabic",
            "Tahoma",
            "Traditional Arabic",
        ]
        font_size_range = [10, 20]  # Example font size range
        return available_fonts, font_size_range

    def extract_content_from_website(self, url):
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = soup.find('span', class_='mw-page-title-main')
        if title:
            title_text = title.get_text()
        else:
            title_text = ""

        # Extract paragraphs, images, captions, and headlines
        content_blocks = []
        counter = 1
        counter_image = counter_text = counter_headline = 1
        paragraph_tags = soup.find_all('p')
        image_tags = soup.find_all('img', class_='thumbimage')
        image_captions = soup.find_all('div', class_='thumbcaption')
        mw_headlines = soup.find_all('span', class_='mw-headline')

        for paragraph_tag, image_tag, caption, headline in itertools.zip_longest(paragraph_tags, image_tags,
                                                                                 image_captions,
                                                                                 mw_headlines):

            text = paragraph_tag.get_text().strip() if paragraph_tag else ""
            src = image_tag['src'] if image_tag is not None else ""
            caption_text = caption.get_text() if caption else ""
            headline_text = headline.get_text() if headline else ""
            text = re.sub(r'[^\u0600-\u06FF\s]', '', text).strip()

            if text:
                content_blocks.append({
                    'type': 'paragraph',
                    'content': text,
                    'number': counter,
                    'number_text': counter_text,
                    'id': 0,
                })
                counter += 1
                counter_text += 1

            if headline_text:
                content_blocks.append({
                    'type': 'headline',
                    'content': headline_text,
                    'number': counter,
                    'number_headline': counter_headline,
                    'id': 1,
                })
                counter += 1
                counter_headline += 1

            if src:
                content_blocks.append({
                    'type': 'image',
                    'src': src,
                    'number': counter,
                    'caption': caption_text,
                    'number_image': counter_image,
                    'id': 2
                })
                counter += 1
                counter_image += 1

        return title_text, content_blocks, counter_text

    def calculate_text_dimension(self, text, font_type=fonts.get("Decotype_Naskh"), font_size=12):
        font = ImageFont.truetype(font_type, 12)
        image = Image.new("RGB", (1, 1), "white")  # Create a small blank image
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    def non_searchable(self, doc, out):
        for page in doc:
            w, h = page.rect.br  # page width / height taken from bottom right point coords
            outpage = out.new_page(width=w, height=h)  # out page has same dimensions
            pix = page.get_pixmap(dpi=150)  # set desired resolution
            outpage.insert_image(page.rect, pixmap=pix)

        out_buffer = BytesIO()
        out.save(out_buffer)
        out_buffer.seek(0)

        return out_buffer

    def save(self, doc):
        output_path = "output.pdf"
        doc.save(output_path, garbage=3, deflate=True)
        doc.close()


aradoc_gen = Aradocgen()
