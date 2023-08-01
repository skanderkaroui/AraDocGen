from fastapi import APIRouter, Response, Query
from fitz import Font

from source.exceptions.font_exceptions import FontException
from source.models.Arabic_Fonts.fonts import fonts, FontEnum
from source.services.doc_generation_service import aradoc_gen
from source.services.layouts import LayoutEnum

router = APIRouter()


# @router.post("/ultimate-arabic-doc-generator", description="Generates the whole Wikipedia library into code")
# async def generate_mega_document(
#         location: str = Query(..., description="Folder location to save the PDF files")
# ):
#     # Check if next_page_link exists in the location
#     next_page_link = aradoc_gen.read_next_page_link(location)
#     base_url = next_page_link or None
#
#     generator = aradoc_gen.ultimate_arab_doc_generator(location, base_url)
#
#     for file_path in generator:
#         # Process each file path here if needed
#         print("Generated PDF:", file_path)
#
#     return Response(
#         content="PDFs generated successfully.",
#         media_type="text/plain",
#     )


@router.post("/arabic-doc-generator",
             description="Generate a PDF document with the specified font type, number of pages, font size, and Wiki URL.")
async def generate_document(
        fontType: FontEnum = Query(..., description="fontType"),
        numberOfPages: int = Query(10, description="numberOfPages"),
        fontSize: int = Query(12, description="fontSize (greater than 10 and less than 20)", gt=10, lt=20),
        url: str = Query(..., description="wikiURL"),
        layoutNumber: LayoutEnum = Query(..., description="layoutNumber"),
):
    try:
        selectedFont = Font(fontfile=fonts.get(fontType.name))
        selectedLayout = layoutNumber.name
    except KeyError as e:
        return Response(
            content=str(e),
            media_type="text/plain",
            status_code=400
        )
    try:
        pdfBuffer = aradoc_gen.generate_pdf(selectedFont, url, selectedLayout, numberOfPages, fontSize)
        return Response(
            content=pdfBuffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={fontType.name}_{fontSize}_{numberOfPages}_{layoutNumber.name}.pdf"},
        )
    except FontException as e:
        return Response(
            content=str(e),
            media_type="text/plain",
            status_code=400
        )


@router.get("/fonts-available", description="Returns the available fonts")
async def get_available_types():
    return aradoc_gen.get_available()


@router.get("/content-extracted", description="Extract content from a given URL.")
async def extract_content(
        url: str = Query(..., description="wikiURL")
):
    return aradoc_gen.extract_content_from_website(url)
