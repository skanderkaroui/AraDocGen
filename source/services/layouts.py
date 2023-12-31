import urllib.request
from io import BytesIO

import arabic_reshaper
import fitz
from PIL import Image
from enum import Enum

align_param = 2


def layout1(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs, n_images, n_headlines):
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
    while (i < int(n_pages)) and ((8 * (i + 1) < n_paragraphs) if n_paragraphs > 8 else True) and (
            (2 * (i + 1) < n_images) if n_images > 2 else True) and (
    (3 * (i + 1) < n_headlines) if n_headlines > 3 else True):
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


def layout2(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs, n_images, n_headlines):
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
    while (i < int(n_pages)) and ((11 * (i + 1) < n_paragraphs) if n_paragraphs > 11 else True) and (
            (3 * (i + 1) < n_images) if n_images > 3 else True) and (
            (7 * (i + 1) < n_headlines) if n_headlines > 7 else True):
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


def layout3(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs, n_images, n_headlines):
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
    while (i < int(n_pages)) and ((11 * (i + 1) < n_paragraphs) if n_paragraphs > 11 else True) and (
            (3 * (i + 1) < n_images) if n_images > 3 else True) and (
            (7 * (i + 1) < n_headlines) if n_headlines > 7 else True):
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


def layout4(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs, n_images, n_headlines):
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
    while (i < int(n_pages)) and ((11 * (i + 1) < n_paragraphs) if n_paragraphs > 11 else True) and (
            (3 * (i + 1) < n_images) if n_images > 3 else True) and (
            (7 * (i + 1) < n_headlines) if n_headlines > 7 else True):
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


def layout5(self, n_pages, doc, title, fonttype, font_size, content_blocks, n_paragraphs, n_images, n_headlines):
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
    while (i < int(n_pages)) and ((10 * (i + 1) < n_paragraphs) if n_paragraphs > 10 else True) and (
            (2 * (i + 1) < n_images) if n_images > 2 else True) and (
            (6 * (i + 1) < n_headlines) if n_headlines > 6 else True):
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


class LayoutEnum(Enum):
    layout1 = "layout1"
    layout2 = "layout2"
    layout3 = "layout3"
    layout4 = "layout4"
    layout5 = "layout5"


layout_mapping = {
    LayoutEnum.layout1: layout1,
    LayoutEnum.layout2: layout2,
    LayoutEnum.layout3: layout3,
    LayoutEnum.layout4: layout4,
    LayoutEnum.layout5: layout5,
}

layout_paragraphs = {
    "layout1": 8,
    "layout2": 11,
    "layout3": 11,
    "layout4": 10,
    "layout5": 10,
}

layout_images = {
    "layout1": 2,
    "layout2": 3,
    "layout3": 3,
    "layout4": 3,
    "layout5": 2,
}

layout_headlines = {
    "layout1": 3,
    "layout2": 7,
    "layout3": 7,
    "layout4": 7,
    "layout5": 6,
}
