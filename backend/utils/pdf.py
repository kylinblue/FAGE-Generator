"""
PDF generation for the FAGE character sheet.

Fills the official Blank-Sheet.pdf AcroForm using PyPDFForm and the
character → field mapping defined in `utils.pdf_mapping`.
"""

import io
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pypdf
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
)
from PyPDFForm import PdfWrapper

from utils.pdf_mapping import map_character_to_fields


BLANK_PDF = Path(__file__).parent.parent / "data" / "Blank-Sheet.pdf"
GENERATED_PDF_DIR = Path(__file__).parent.parent / "generated_pdfs"
GENERATED_PDF_DIR.mkdir(exist_ok=True)

_MONOSPACE_FIELDS = ("Text234", "Text235", "Text251", "Text263", "Text269")
_MONOSPACE_FONT_SIZE = 7

_MULTILINE_FLAG = 1 << 12  # PDF Tx field flag bit for multiline

# DA font name → PostScript base-14 font name.
_BASE14_FONTS = {
    "/Helv": "/Helvetica",
    "/HeBo": "/Helvetica-Bold",
    "/Courier": "/Courier",
}

# Approximate character-width ratios (fraction of font size) for centering.
_WIDTH_RATIO = {
    "/Courier": 0.60,  # exact for Courier
    "/Helv": 0.50,
    "/HeBo": 0.55,
}


def _safe_filename(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_").replace("\\", "_")


def _escape_pdf_string(s: str) -> bytes:
    return (
        s.replace("\\", "\\\\")
         .replace("(", "\\(")
         .replace(")", "\\)")
    ).encode("latin-1", errors="replace")


def _add_base14_fonts(writer: pypdf.PdfWriter) -> Dict[str, Any]:
    """Register Helvetica, Helvetica-Bold, Courier as base-14 Type1 fonts.

    Returns {da_font_name: indirect_ref} so appearance streams can drop the same
    indirect reference into their own /Resources/Font dict.
    """
    refs: Dict[str, Any] = {}
    acroform = writer._root_object.get("/AcroForm")
    if hasattr(acroform, "get_object"):
        acroform = acroform.get_object()
    dr_fonts = None
    if acroform is not None:
        dr = acroform.get("/DR")
        if dr is not None:
            dr_fonts = dr.get("/Font")

    for da_name, base in _BASE14_FONTS.items():
        font = DictionaryObject({
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject(base),
            NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
        })
        ref = writer._add_object(font)
        refs[da_name] = ref
        if dr_fonts is not None and da_name not in dr_fonts:
            dr_fonts[NameObject(da_name)] = ref
    return refs


def _parse_da(da_str: Optional[str]) -> Tuple[str, float]:
    """Parse a default-appearance string into (font_name, size). Default Helv 9."""
    font = "/Helv"
    size = 9.0
    if not da_str:
        return font, size
    parts = str(da_str).split()
    for i, tok in enumerate(parts):
        if tok == "Tf" and i >= 2:
            if parts[i - 2].startswith("/"):
                font = parts[i - 2]
            try:
                parsed = float(parts[i - 1])
                if parsed > 0:
                    size = parsed
            except ValueError:
                pass
            break
    return font, size


def _approx_text_width(text: str, font: str, size: float) -> float:
    return len(text) * size * _WIDTH_RATIO.get(font, 0.5)


def _build_text_appearance(
    value: str,
    width: float,
    height: float,
    da_str: Optional[str],
    font_refs: Dict[str, Any],
    quadding: int,
    multiline: bool,
    force_font: Optional[str] = None,
    force_size: Optional[float] = None,
) -> DecodedStreamObject:
    font, size = _parse_da(da_str)
    if force_font is not None:
        font = force_font
    if force_size is not None:
        size = force_size
    if font not in font_refs:
        font = "/Helv"

    inset_x = 2.0
    inset_y = 2.0
    parts = [b"/Tx BMC\nq\nBT\n"]
    parts.append(f"{font} {size} Tf\n".encode("latin-1"))

    if multiline or "\n" in value:
        leading = size * 1.2
        first_baseline_y = height - size - inset_y
        parts.append(f"{leading} TL\n".encode("latin-1"))
        parts.append(f"{inset_x} {first_baseline_y} Td\n".encode("latin-1"))
        for i, line in enumerate(value.split("\n")):
            if i > 0:
                parts.append(b"T*\n")
            parts.append(b"(")
            parts.append(_escape_pdf_string(line))
            parts.append(b") Tj\n")
    else:
        text = value
        baseline_y = (height - size) / 2.0
        text_w = _approx_text_width(text, font, size)
        if quadding == 1:
            x = max(inset_x, (width - text_w) / 2.0)
        elif quadding == 2:
            x = max(inset_x, width - text_w - inset_x)
        else:
            x = inset_x
        parts.append(f"{x} {baseline_y} Td\n".encode("latin-1"))
        parts.append(b"(")
        parts.append(_escape_pdf_string(text))
        parts.append(b") Tj\n")

    parts.append(b"ET\nQ\nEMC\n")
    content = b"".join(parts)

    stream = DecodedStreamObject()
    stream.set_data(content)
    stream[NameObject("/Type")] = NameObject("/XObject")
    stream[NameObject("/Subtype")] = NameObject("/Form")
    stream[NameObject("/FormType")] = NumberObject(1)
    stream[NameObject("/BBox")] = ArrayObject([
        FloatObject(0), FloatObject(0),
        FloatObject(width), FloatObject(height),
    ])
    stream[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({
            NameObject(font): font_refs[font],
        }),
    })
    return stream


def _bake_all_text_appearances(pdf_bytes: bytes) -> bytes:
    """Bake a self-contained /AP appearance for every text field with a /V.

    Acrobat with NeedAppearances=false strictly trusts /AP, so any missing or
    malformed appearance shows blank. We render every text field ourselves
    using base-14 fonts (no embedding required), force /Courier for the
    tabular fields, and shut off NeedAppearances so no viewer regenerates.
    """
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    writer = pypdf.PdfWriter(clone_from=reader)
    font_refs = _add_base14_fonts(writer)
    monospace = set(_MONOSPACE_FIELDS)

    for page in writer.pages:
        annots = page.get("/Annots") or []
        for annot_ref in annots:
            annot = annot_ref.get_object()
            if str(annot.get("/FT") or "") != "/Tx":
                continue
            value = annot.get("/V")
            if value is None or value == "":
                if "/AP" in annot:
                    del annot[NameObject("/AP")]
                continue
            rect = annot.get("/Rect")
            if rect is None or len(rect) != 4:
                continue
            x0, y0, x1, y1 = (float(c) for c in rect)
            width = x1 - x0
            height = y1 - y0
            if width <= 0 or height <= 0:
                continue

            ff = int(annot.get("/Ff") or 0)
            multiline = bool(ff & _MULTILINE_FLAG)
            quadding = int(annot.get("/Q") or 0)
            field_name = str(annot.get("/T") or "")

            if field_name in monospace:
                stream = _build_text_appearance(
                    str(value), width, height, "/Courier 7 Tf 0 g",
                    font_refs, quadding=0, multiline=True,
                    force_font="/Courier", force_size=_MONOSPACE_FONT_SIZE,
                )
            else:
                stream = _build_text_appearance(
                    str(value), width, height, str(annot.get("/DA") or ""),
                    font_refs, quadding=quadding, multiline=multiline,
                )

            stream_ref = writer._add_object(stream)
            annot[NameObject("/AP")] = DictionaryObject({
                NameObject("/N"): stream_ref,
            })

    acroform = writer._root_object.get("/AcroForm")
    if acroform is not None:
        if hasattr(acroform, "get_object"):
            acroform = acroform.get_object()
        acroform[NameObject("/NeedAppearances")] = BooleanObject(False)

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()


def _fill(character: Dict[str, Any]) -> bytes:
    if not character.get("name"):
        raise ValueError("Character must have a name")
    fields = map_character_to_fields(character)
    wrapper = PdfWrapper(str(BLANK_PDF), need_appearances=True)
    for field_name in _MONOSPACE_FIELDS:
        widget = wrapper.widgets.get(field_name)
        if widget is None:
            continue
        widget.font = "/Courier"
        widget.font_size = _MONOSPACE_FONT_SIZE
    filled = wrapper.fill(fields).read()
    return _bake_all_text_appearances(filled)


def generate_character_pdf_bytes(character: Dict[str, Any]) -> bytes:
    return _fill(character)


def generate_character_pdf(character: Dict[str, Any], output_path: Optional[str] = None) -> str:
    pdf_bytes = _fill(character)
    if output_path is None:
        output_path = str(GENERATED_PDF_DIR / f"{_safe_filename(character['name'])}.pdf")
    with open(output_path, "wb+") as f:
        f.write(pdf_bytes)
    return output_path
