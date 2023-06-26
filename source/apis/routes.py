from fastapi import APIRouter, Response, Query
from fitz import Font

from source.models.Arabic_Fonts.fonts import fonts
from source.services.doc_generation_service import Aradocgen

router = APIRouter()


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
        url: str = Query(..., description="URL of the Wikipedia article")
):
    selected_font = Font(fontfile=fonts.get(fonttype))
    pdf_buffer = Aradocgen().generate_pdf(selected_font, url, n_pages, font_size)
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename={ftt}_{fs}_{np}.pdf".format(ftt=fonttype, fs=font_size,
                                                                                     np=n_pages)},
    )


@router.get("/get-available")
async def get_available_types():
    return Aradocgen().get_available()


@router.get("/extract-content")
async def extract_content(
        url: str = Query(..., description="URL")
):
    return Aradocgen().extract_content_from_website(url)
