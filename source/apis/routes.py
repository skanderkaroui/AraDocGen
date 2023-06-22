from pathlib import Path

import fitz
from fastapi import APIRouter, Response, Query

from source.services.utils import Aradocgen

router = APIRouter()

text = Path(r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\data.txt").read_text(encoding="utf-8")

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

aradocgen = Aradocgen()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"hello": f"Hello, {name}!"}


@router.get("/generate-doc")
async def generate_document(
        fonttype: str = Query(..., description="Font type"),
        n_pages: int = Query(10, description="Number of pages"),
        font_size: int = Query(12, description="Font size"),
):
    selected_font = fitz.Font(fontfile=fonts.get(fonttype))
    pdf_buffer = aradocgen.generate_pdf(selected_font, text, n_pages, font_size)
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=generated_doc.pdf"},
    )


@router.get("/get-available")
async def get_available_types():
    return aradocgen.get_available()
