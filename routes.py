from pathlib import Path

from fastapi import APIRouter, Response

from utils import generate_pdf, get_available

router = APIRouter()

text = Path(r"C:\Users\skand\PycharmProjects\DocGeneratorFastApi\source\models\data.txt").read_text(encoding="utf-8")


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"hello": f"Hello, {name}!"}


@router.get("/generate-doc")
async def generate_document(n_pages=1, font_size=12, fontype="font1"):
    pdf_buffer = generate_pdf(text, n_pages, font_size, fontype)
    return Response(content=pdf_buffer.getvalue(), media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=generated_doc.pdf"})


@router.get("/get-available")
async def get_available_types():
    return get_available()
