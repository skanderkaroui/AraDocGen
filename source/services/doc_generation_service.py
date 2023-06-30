import fitz
import arabic_reshaper
from io import BytesIO
import requests
import bs4
from PIL import Image, ImageDraw, ImageFont
import re

from source.models.Arabic_Fonts.fonts import fonts
import urllib.request

# Open a
align_param = 2


class Aradocgen:
    def generate_pdf(self, fonttype, url, n_pages=10, font_size=12):
        doc = fitz.open()  # open the document
        title, content_blocks, n = self.extract_content_from_website(url)
        index_paragraph = index_header = index_image = 0
        found = False
        for i in range(int(n_pages)):
            page = doc.new_page()
            page = doc[i]
            # reshape the text to connect the arabic words together
            # text_reshaped = arabic_reshaper.reshape(text)
            # initializing the text writer
            text_writer = fitz.TextWriter(page.rect)
            if i == 0:
                title
                text_writer.fill_textbox(
                    (300, 60, 545, 90),
                    arabic_reshaper.reshape(title),
                    font=fonttype,
                    fontsize=int(font_size) + 10,
                    align=align_param,
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
                        fontsize=int(font_size)+2,
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
                        fontsize=int(font_size)+2,
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
                        fontsize=int(font_size)+2,
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

        paragraph_tags = soup.find_all('p')
        image_tags = soup.find_all('img', class_='thumbimage')
        image_captions = soup.find_all('div', class_='thumbcaption')
        mw_headlines = soup.find_all('span', class_='mw-headline')

        for paragraph_tag, image_tag, caption, headline in zip(paragraph_tags, image_tags, image_captions,
                                                               mw_headlines):

            text = paragraph_tag.get_text().strip()
            src = image_tag['src']
            caption_text = caption.get_text()
            headline_text = headline.get_text()
            text = re.sub(r'[^\u0600-\u06FF\s]', '', text).strip()

            if text:
                content_blocks.append({
                    'type': 'paragraph',
                    'content': text,
                    'number': counter,
                    'id': 0,
                })
                counter += 1

            if headline_text:
                content_blocks.append({
                    'type': 'headline',
                    'content': headline_text,
                    'number': counter,
                    'id': 1,
                })
                counter += 1

            if src:
                content_blocks.append({
                    'type': 'image',
                    'src': src,
                    'number': counter,
                    'caption': caption_text,
                    'id': 2
                })
                counter += 1

        return title_text, content_blocks, counter

    def calculate_text_dimension(text, fonttype=fonts.get("Decotype_Naskh"), font_size=12):
        font = ImageFont.truetype(fonttype, 12)
        image = Image.new("RGB", (1, 1), "white")  # Create a small blank image
        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
