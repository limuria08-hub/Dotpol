"""P1.03 document ingestion: only local Docling, source original/normalized checksums."""
import base64
import hashlib
import sys
import types

from fastapi.testclient import TestClient
from app import create_app
from dotpol_platform.store import Store

LOCAL = {'X-Dotpol-Local': '1'}


def client(tmp_path):
    c = TestClient(create_app(tmp_path / 'local.sqlite3'))
    project = c.post('/api/projects', headers=LOCAL, json={'title':'Document research'}).json()['id']
    return c, project


def fake_docling(monkeypatch, content='Documented public figures 41 percent'):
    base = types.ModuleType('docling.datamodel.base_models')
    class Formats:
        PDF='pdf'; DOCX='docx'
    class Status:
        SUCCESS='success'
    class Stream:
        def __init__(self, name, stream):
            self.name=name; self.stream=stream
    base.InputFormat=Formats
    base.ConversionStatus=Status
    base.DocumentStream=Stream
    module=types.ModuleType('docling.document_converter')
    class Native:
        pass
    class Converter:
        def __init__(self,allowed_formats,format_options):
            assert allowed_formats in ([Formats.PDF],[Formats.DOCX])
            if allowed_formats==[Formats.PDF]:
                assert isinstance(format_options[Formats.PDF],Native)
            else:
                assert not format_options
        def convert(self, source, raises_on_error):
            assert source.name in ('record.pdf','record.docx')
            assert source.stream.read()
            return types.SimpleNamespace(status=Status.SUCCESS,document=types.SimpleNamespace(export_to_markdown=lambda:content))
    module.DocumentConverter=Converter
    module.NativePdfFormatOption=Native
    monkeypatch.setitem(sys.modules,'docling',types.ModuleType('docling'))
    monkeypatch.setitem(sys.modules,'docling.datamodel',types.ModuleType('docling.datamodel'))
    monkeypatch.setitem(sys.modules,'docling.datamodel.base_models',base)
    monkeypatch.setitem(sys.modules,'docling.document_converter',module)


def test_pdf_docling_citations_and_provenance(tmp_path, monkeypatch):
    fake_docling(monkeypatch)
    c,p=client(tmp_path)
    data=b'%PDF-1.7\nsynthetic'
    row=c.post(f'/api/projects/{p}/documents',headers=LOCAL,json={
        'name':'record.pdf','kind':'pdf','content_base64':base64.b64encode(data).decode()})
    assert row.status_code==201,row.text
    src=row.json()
    assert src['file_sha256']==hashlib.sha256(data).hexdigest()
    assert src['sha256']==hashlib.sha256(b'Documented public figures 41 percent').hexdigest()
    assert src['extraction_method']=='docling-pdf-native'
    result=c.post(f'/api/projects/{p}/research',headers=LOCAL,json={'question':'public figures','mode':'extractive'})
    assert result.status_code==200 and result.json()['has_evidence']
    assert result.json()['artifact']['evidence'][0]['sha256']==src['sha256']
    assert Store(tmp_path / 'local.sqlite3').source(p,src['id'])['kind']=='pdf'


def test_docx_and_migration_safe_txt_source(tmp_path,monkeypatch):
    fake_docling(monkeypatch)
    c,p=client(tmp_path)
    data=b'PK\x03\x04synthetic'
    r=c.post(f'/api/projects/{p}/documents',headers=LOCAL,json={
        'name':'record.docx','kind':'docx','content_base64':base64.b64encode(data).decode()})
    assert r.status_code==201 and r.json()['file_sha256']==hashlib.sha256(data).hexdigest()
    text=c.post(f'/api/projects/{p}/sources',headers=LOCAL,json={'name':'x.txt','kind':'txt','content':'normal text'})
    assert text.status_code==201 and text.json()['file_sha256'] is None


def test_invalid_base64_signature_name_and_size_do_not_insert(tmp_path,monkeypatch):
    fake_docling(monkeypatch)
    c,p=client(tmp_path)
    target=f'/api/projects/{p}/documents'
    samples=[
        ('record.pdf','pdf','not-base64%%'),
        ('record.pdf','pdf',base64.b64encode(b'not-pdf').decode()),
        ('../record.pdf','pdf',base64.b64encode(b'%PDF-test').decode()),
        ('record.docx','docx',base64.b64encode(b'not-docx').decode()),
        ('record.pdf','pdf',base64.b64encode(b'%PDF-'+b'x'*1048576).decode()),
    ]
    for name,kind,encoded in samples:
        r=c.post(target,headers=LOCAL,json={'name':name,'kind':kind,'content_base64':encoded})
        assert r.status_code==422,(name,r.text)
    assert c.post(target,json={'name':'record.pdf','kind':'pdf',
       'content_base64':base64.b64encode(b'%PDF-test').decode()}).status_code==403
    assert c.get(f'/api/projects/{p}/sources').json()==[]


def test_empty_and_oversize_extraction_rejected(tmp_path,monkeypatch):
    c,p=client(tmp_path)
    raw=base64.b64encode(b'%PDF-test').decode()
    for text in ('', 'x'*1048577):
        fake_docling(monkeypatch,text)
        r=c.post(f'/api/projects/{p}/documents',headers=LOCAL,json={
            'name':'record.pdf','kind':'pdf','content_base64':raw})
        assert r.status_code==422
    assert c.get(f'/api/projects/{p}/sources').json()==[]


def test_missing_project_does_not_convert(tmp_path,monkeypatch):
    fake_docling(monkeypatch)
    c,p=client(tmp_path)
    r=c.post(f'/api/projects/{"0"*32}/documents',headers=LOCAL,json={
        'name':'record.pdf','kind':'pdf','content_base64':base64.b64encode(b'%PDF-test').decode()})
    assert r.status_code==404
    assert c.get(f'/api/projects/{p}/sources').json()==[]
