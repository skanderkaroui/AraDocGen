from io import BytesIO
import arabic_reshaper
import fitz

font1 = fitz.Font(fontfile=r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\AF_Diwani-Normal-Traditional.ttf")
font2 = fitz.Font(fontfile=r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\andlso.ttf")
img = open(r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\image.jpg", "rb").read()



def generate_pdf(text, n_pages=10, font_size=12, fonttype=font1):
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


def get_available():
    available_fonts = [
        "Droid Arabic Naskh",
        "Roboto",
        "Noto Naskh Arabic",
        "Scheherazade",
        "Amiri",
        "Lateef",
        # Add more commonly used Arabic fonts here
    ]
    font_size_range = [10, 20]  # Example font size range
    return available_fonts, font_size_range
