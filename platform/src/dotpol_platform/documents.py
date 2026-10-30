"""Opt-in, in-memory Docling extraction for locally uploaded documents.

Only selectable PDF text and DOCX are accepted: Docling's native PDF pipeline
avoids implicit OCR downloads. No URL fetching or output filesystem paths.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
from io import BytesIO
from pathlib import PurePath

from dotpol_platform.store import InvalidInput, MAX_SOURCE_BYTES


class DocumentEngineUnavailable(Exception):
    """The optional local Docling parser is not installed."""


def extract_document(name: str, kind: str, encoded: str) -> tuple[str, str, str]:
    """Extract (text, original_file_sha256, extraction_method)."""
    if kind not in {'pdf', 'docx'}:
        raise InvalidInput('Document kind must be pdf or docx')
    if not isinstance(name, str) or not name or len(name) > 180 or any(c in name for c in ('/', '\\', '\x00')):
        raise InvalidInput('Invalid document name')
    if PurePath(name).suffix.lower() != '.' + kind:
        raise InvalidInput('Document filename extension does not match kind')
    if not isinstance(encoded, str) or len(encoded) > (MAX_SOURCE_BYTES * 4 // 3 + 8):
        raise InvalidInput('Encoded document exceeds the 1 MiB preview limit')
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise InvalidInput('Document is not valid base64') from exc
    if not raw or len(raw) > MAX_SOURCE_BYTES:
        raise InvalidInput('Document must be 1–1048576 bytes')
    if kind == 'pdf' and not raw.startswith(b'%PDF-'):
        raise InvalidInput('PDF signature missing')
    if kind == 'docx' and not raw.startswith(b'PK\x03\x04'):
        raise InvalidInput('DOCX ZIP signature missing')
    try:
        from docling.datamodel.base_models import ConversionStatus, DocumentStream, InputFormat
        from docling.document_converter import DocumentConverter, NativePdfFormatOption
    except ImportError as exc:
        raise DocumentEngineUnavailable('Install Docling with pip install -e ".[documents]"') from exc
    source = DocumentStream(name=name, stream=BytesIO(raw))
    format_id = InputFormat.PDF if kind == 'pdf' else InputFormat.DOCX
    try:
        options = {InputFormat.PDF: NativePdfFormatOption()} if kind == 'pdf' else {}
        converter = DocumentConverter(allowed_formats=[format_id], format_options=options)
        result = converter.convert(source, raises_on_error=False)
        if result.status != ConversionStatus.SUCCESS:
            raise InvalidInput('Document extraction failed or was partially successful')
        content = result.document.export_to_markdown().strip()
    except InvalidInput:
        raise
    except Exception as exc:
        raise InvalidInput('Document could not be extracted locally') from exc
    if not content:
        raise InvalidInput('Document has no extractable text (OCR is not enabled)')
    if len(content.encode('utf-8')) > MAX_SOURCE_BYTES:
        raise InvalidInput('Extracted document text exceeds 1 MiB')
    return content, hashlib.sha256(raw).hexdigest(), f'docling-{kind}-native'
