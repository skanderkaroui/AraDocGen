import itertools
import logging
import re
import urllib.request
from io import BytesIO

import arabic_reshaper
import bs4
import fitz
import requests
from PIL import Image, ImageDraw, ImageFont

from source.exceptions.page_exceptions import PageException
from source.models.Arabic_Fonts.fonts import fonts
from source.services.layouts import layout, LayoutEnum
logging.basicConfig(level=logging.INFO)
align_param = 2


class Aradocgen:
    def generate_pdf(self, fonttype, url, layout_number, n_pages=10, font_size=12):
        doc = fitz.open()  # open the document
        title, content_blocks, n_paragraphs = self.extract_content_from_website(url)
        layout_key = LayoutEnum(layout_number)
        layout_key_string = layout_key.name

        if layout_key_string == "layout1":
            try:
                if n_paragraphs < 8:
                    raise PageException("number of pages very low", 505)
            except KeyError:
                raise PageException("number of pages very low")

        elif layout_key_string == "layout1":
            try:
                if n_paragraphs < 8:
                    raise PageException("number of pages very low", 505)
            except KeyError:
                raise PageException("number of pages very low")

        if layout_key_string == "layout2":
            try:
                if n_paragraphs < 11:
                    raise PageException("number of pages very low", 505)
            except KeyError:
                raise PageException("number of pages very low")

        if layout_key_string == "layout3":
            try:
                if n_paragraphs < 7:
                    raise PageException("number of pages very low", 505)
            except KeyError:
                raise PageException("number of pages very low")

        if layout_key_string == "layout4":
            try:
                if n_paragraphs < 10:
                    raise PageException("number of pages very low", 505)
            except KeyError:
                raise PageException("number of pages very low")

        if layout_key_string == "layout5":
            try:
                if n_paragraphs < 10:
                    raise PageException("number of pages very low", 505)
            except KeyError:
                raise PageException("number of pages very low")

        if layout_key in layout:
            layout_function = layout[layout_key]
            layout_function(n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs)
        else:
            raise ValueError(f"Invalid layout number: {layout_number}")


        out = fitz.open()  # output PDF

        # making the pdf non-readable
        for page in doc:
            w, h = page.rect.br  # page width / height taken from bottom right point coords
            outpage = out.new_page(width=w, height=h)  # out page has same dimensions
            pix = page.get_pixmap(dpi=150)  # set desired resolution
            outpage.insert_image(page.rect, pixmap=pix)

        out_buffer = BytesIO()
        out.save(out_buffer)
        out_buffer.seek(0)

        output_path = "output.pdf"
        doc.save(output_path, garbage=3, deflate=True)
        doc.close()

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

    def calculate_text_dimension(text, fonttype=fonts.get("Decotype_Naskh"), font_size=12):
        font = ImageFont.truetype(fonttype, 12)
        image = Image.new("RGB", (1, 1), "white")  # Create a small blank image
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    def layout1(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs):
        """ Returns layout number 1

        Args:
            n_pages: (number) the number of pages
            doc: the doc that the file is writing on
            title: the title of the document
            font_size: pretty self-explanatory
            content_blocks: (list) returning the content of the wiki article
            n_paragraphs: (number) number of paragraphs in the file
        """
        index_paragraph = index_header = index_image = 0
        i = 0
        while (i < int(n_pages)) and ((8 * (i + 1) < n_paragraphs) if n_paragraphs > 8 else True):
            page = doc.new_page()
            page = doc[i]
            # initializing the text writer
            text_writer = fitz.TextWriter(page.rect)
            if i == 0:
                text_writer.fill_textbox(
                    (150, 25, 450, 65),
                    arabic_reshaper.reshape(title),
                    font=fonttype,
                    fontsize=int(font_size) + 30,
                    align=1,
                    right_to_left=True,
                )
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    # first block of text
                    text_writer.fill_textbox(
                        (300, 100, 550, 200),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (300, 220, 550, 240),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (300, 245, 550, 345),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        390, 355, 490, 505)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (300, 515, 550, 535),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (300, 540, 550, 640),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (300, 660, 550, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True,
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            # second block of text
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 100, 280, 235),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 245, 280, 360),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        100, 365, 200, 500)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 515, 280, 535),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 540, 280, 650),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 660, 280, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            text_writer.write_text(page)
            i += 1

    def layout2(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs):
        """ Returns layout number 1

                Args:
                    n_pages: (number) the number of pages
                    doc: the doc that the file is writing on
                    title: the title of the document
                    font_size: pretty self-explanatory
                    content_blocks: (list) returning the content of the wiki article
                    n_paragraphs: (number) number of paragraphs in the file
        """
        index_paragraph = index_header = index_image = 0
        i = 0
        while (i < int(n_pages)) and ((11 * (i + 1) < n_paragraphs) if n_paragraphs > 11 else True):
            page = doc.new_page()
            page = doc[i]
            # reshape the text to connect the arabic words together
            # text_reshaped = arabic_reshaper.reshape(text)
            # initializing the text writer
            text_writer = fitz.TextWriter(page.rect)
            if i == 0:
                text_writer.fill_textbox(
                    (150, 25, 450, 65),
                    arabic_reshaper.reshape(title),
                    font=fonttype,
                    fontsize=int(font_size) + 30,
                    align=1,
                    right_to_left=True,
                )
            # block 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    # first block of text
                    text_writer.fill_textbox(
                        (400, 100, 550, 200),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (400, 220, 550, 240),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (400, 245, 550, 345),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        450, 355, 500, 505)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (400, 515, 550, 535),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (400, 540, 550, 640),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (400, 660, 550, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True,
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            # block 2
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (210, 100, 390, 120),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1

            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (210, 125, 390, 225),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        280, 230, 350, 380)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (210, 385, 390, 405),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (210, 410, 390, 510),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (210, 515, 390, 535),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (210, 540, 390, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            # block 3
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    # first block of text
                    text_writer.fill_textbox(
                        (30, 100, 200, 200),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 220, 200, 240),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 245, 200, 345),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        90, 355, 140, 505)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 515, 200, 535),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 540, 200, 640),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 660, 200, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True,
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            text_writer.write_text(page)
            i += 1

    def layout3(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs):
        """ Returns layout number 1

                Args:
                    n_pages: (number) the number of pages
                    doc: the doc that the file is writing on
                    title: the title of the document
                    font_size: pretty self-explanatory
                    content_blocks: (list) returning the content of the wiki article
                    n_paragraphs: (number) number of paragraphs in the file
        """
        index_paragraph = index_header = index_image = 0
        i = 0
        while (i < int(n_pages)) and ((8 * (i + 1) < n_paragraphs) if n_paragraphs > 8 else True):
            page = doc.new_page()
            page = doc[i]
            # reshape the text to connect the arabic words together
            # text_reshaped = arabic_reshaper.reshape(text)
            # initializing the text writer
            text_writer = fitz.TextWriter(page.rect)
            if i == 0:
                text_writer.fill_textbox(
                    (150, 25, 450, 65),
                    arabic_reshaper.reshape(title),
                    font=fonttype,
                    fontsize=int(font_size) + 30,
                    align=1,
                    right_to_left=True,
                )
            # first block of text
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (200, 100, 550, 120),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (200, 125, 550, 225),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (200, 230, 550, 250),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (200, 255, 550, 355),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        450, 360, 550, 500)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        340, 360, 440, 500)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        230, 360, 330, 500)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (200, 505, 550, 525),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (375, 530, 550, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (200, 505, 370, 525),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (200, 530, 370, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            # second block of text
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 100, 190, 120),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 125, 190, 300),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 310, 190, 330),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 335, 190, 435),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 440, 190, 535),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 540, 190, 550),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 555, 190, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            text_writer.write_text(page)
            i += 1

    def layout4(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs):
        """ Returns layout number 1

                Args:
                    n_pages: (number) the number of pages
                    doc: the doc that the file is writing on
                    title: the title of the document
                    font_size: pretty self-explanatory
                    content_blocks: (list) returning the content of the wiki article
                    n_paragraphs: (number) number of paragraphs in the file
        """
        index_paragraph = index_header = index_image = 0
        i = 0
        while (i < int(n_pages)) and ((10 * (i + 1) < n_paragraphs) if n_paragraphs > 10 else True):
            page = doc.new_page()
            page = doc[i]
            # initializing the text writer
            text_writer = fitz.TextWriter(page.rect)
            if i == 0:
                text_writer.fill_textbox(
                    (150, 25, 450, 65),
                    arabic_reshaper.reshape(title),
                    font=fonttype,
                    fontsize=int(font_size) + 30,
                    align=1,
                    right_to_left=True,
                )
            # first block of text
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (450, 100, 550, 120),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (450, 125, 550, 225),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        320, 100, 450, 225)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (300, 230, 550, 250),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (300, 255, 550, 355),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (300, 360, 550, 380),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (300, 385, 550, 485),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (300, 490, 550, 520),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (450, 525, 550, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (300, 525, 445, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            # second block of text

            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 100, 280, 120),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (100, 125, 280, 225),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        30, 125, 100, 225)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 230, 280, 250),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (150, 255, 280, 380),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 255, 145, 380),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (200, 385, 280, 600),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        35, 385, 190, 595)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 605, 280, 615),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 625, 280, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            text_writer.write_text(page)
            i += 1

    def layout5(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs):
        """ Returns layout number 1

                        Args:
                            n_pages: (number) the number of pages
                            doc: the doc that the file is writing on
                            title: the title of the document
                            font_size: pretty self-explanatory
                            content_blocks: (list) returning the content of the wiki article
                            n_paragraphs: (number) number of paragraphs in the file
        """
        index_paragraph = index_header = index_image = 0
        i = 0
        while (i < int(n_pages)) and ((11 * (i + 1) < n_paragraphs) if n_paragraphs > 11 else True):
            page = doc.new_page()
            page = doc[i]
            # initializing the text writer
            text_writer = fitz.TextWriter(page.rect)
            if i == 0:
                text_writer.fill_textbox(
                    (150, 25, 450, 65),
                    arabic_reshaper.reshape(title),
                    font=fonttype,
                    fontsize=int(font_size) + 30,
                    align=1,
                    right_to_left=True,
                )
            # block 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (465, 100, 550, 120),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    # first block of text
                    text_writer.fill_textbox(
                        (465, 125, 550, 325),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (465, 330, 550, 350),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (465, 355, 550, 555),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (465, 560, 550, 580),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (465, 585, 550, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            # block 2
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        240, 120, 460, 320)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1

            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (220, 330, 460, 350),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1

            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (220, 350, 460, 550),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (220, 555, 460, 575),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (360, 580, 460, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_image < len(content_blocks):
                block = content_blocks[index_image]
                if block['id'] == 2:
                    image_url = 'https:' + block['src']
                    image_data = urllib.request.urlopen(image_url).read()
                    image = Image.open(BytesIO(image_data))
                    image_width, image_height = image.size
                    image_rect = (
                        240, 580, 350, 750)  # Define the new rectangle coordinates for image placement
                    page.insert_image(image_rect, stream=image_data, keep_proportion=False)
                    index_image += 1
                    break
                index_image += 1

            # block 3
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    # first block of text
                    text_writer.fill_textbox(
                        (100, 100, 200, 200),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (100, 200, 200, 220),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1

            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 100, 90, 220),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            while index_header < len(content_blocks):
                block = content_blocks[index_header]
                if block['id'] == 1:
                    text_writer.fill_textbox(
                        (30, 225, 200, 245),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size) + 2,
                        align=align_param,
                        right_to_left=True
                    )
                    index_header += 1
                    break
                index_header += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (100, 250, 200, 370),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1
            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (100, 375, 200, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True,
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            while index_paragraph < len(content_blocks):
                block = content_blocks[index_paragraph]
                if block['id'] == 0:
                    text_writer.fill_textbox(
                        (30, 250, 90, 800),
                        arabic_reshaper.reshape(block['content']),
                        font=fonttype,
                        fontsize=int(font_size),
                        align=align_param,
                        right_to_left=True,
                    )
                    index_paragraph += 1
                    break
                index_paragraph += 1

            text_writer.write_text(page)
            i += 1
