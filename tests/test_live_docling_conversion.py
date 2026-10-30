"""Opt-in real Docling conversion test with synthetic local DOCX fixture."""
import base64
import hashlib
import io
import os
import zipfile
import pytest
from dotpol_platform.documents import extract_document


def synthetic_docx() -> bytes:
    content_types = ('<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '</Types>')
    relations = ('<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body><w:p><w:r><w:t>Synthetic public budget 42 units</w:t></w:r></w:p>'
        '<w:sectPr/></w:body></w:document>')
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('[Content_Types].xml', content_types)
        archive.writestr('_rels/.rels', relations)
        archive.writestr('word/document.xml', document)
    return out.getvalue()


@pytest.mark.skipif(os.getenv('DOTPOL_LIVE_DOCLING_TEST') != '1',
                    reason='Explicit opt-in real Docling test; no model downloads')
def test_real_docling_docx_extraction_and_hashes():
    pytest.importorskip('docling')
    file_bytes = synthetic_docx()
    text, file_sha, method = extract_document('synthetic.docx','docx',
                                              base64.b64encode(file_bytes).decode('ascii'))
    assert 'Synthetic public budget 42 units' in text
    assert file_sha == hashlib.sha256(file_bytes).hexdigest()
    assert method == 'docling-docx-native'
