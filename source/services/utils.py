import fitz
import arabic_reshaper
from io import BytesIO
import requests
import bs4
from PIL import Image, ImageDraw, ImageFont

img = open(r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\image.jpg", "rb").read()
fonts = \
    {
        "Advertising_Bold": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Advertising_Bold.ttf",
        "Af_Diwani": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\AF_Diwani.ttf",
        "Andalus": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Andalus.ttf",
        "Arabic_transparent": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Arabic_transparent.ttf",
        "Arslan_Wessam_A": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Arslan_Wessam_A.ttf",
        "Decotype_Naskh": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Decotype_Naskh.ttf",
        "Decotype_Thuluth": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Decotype_Thuluth.ttf",
        "M_Unicode_Sara": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\M_Unicode_Sara.ttf",
        "Decotype_Naskh": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Sakkal_Majalla.ttf",
        "Simplified_Arabic": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Simplified_Arabic.ttf",
        "Tahoma": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Tahoma.ttf",
        "Traditional_Arabic": r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\Arabic Fonts\Traditional_Arabic.ttf"
    }
class Aradocgen:
    def generate_pdf(self, fonttype, text, n_pages=10, font_size=12):
        doc = fitz.open()  # open the document
        for i in range(int(n_pages)):
            page = doc.new_page()
            page = doc[i]
            # reshape the text to connect the arabic words together
            text_reshaped = arabic_reshaper.reshape(text)
            # initializing the text writer
            text_writer = fitz.TextWriter(page.rect)
            # first block of text
            text_writer.fill_textbox(
                (300, 100, 550, 800),
                text_reshaped,
                font=fonttype,
                fontsize=int(font_size),
                align=3,
                right_to_left=True
            )
            # second block of text
            text_writer.fill_textbox(
                (30, 100, 280, 350),
                text_reshaped,
                font=fonttype,
                fontsize=int(font_size),
                align=3,
                right_to_left=True
            )
            page.insert_image(
                (30, 100, 280, 1085),
                stream=img,
            )

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

    def extract_content_from_website(url):
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