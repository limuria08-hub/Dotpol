"""P1.06 one deterministic tool registry with deny-by-default grants."""
import pytest
from dotpol_platform.store import Store, InvalidInput, NotFound
from dotpol_platform.political_identity import initialize, register
from dotpol_platform.approved_tools import ToolGrant, invoke


def test_tools_are_project_scoped_and_not_arbitrary_rpc(tmp_path,monkeypatch):
    monkeypatch.setenv('DOTPOL_SEARCH_ENGINE','literal')
    s=Store(tmp_path/'db.sqlite3');initialize(s)
    a=s.create_project('A')['id'];b=s.create_project('B')['id']
    sa=s.import_source(a,'a.txt','txt','Public budget 20')
    sb=s.import_source(b,'b.txt','txt','Private project budget 90')
    g=ToolGrant('owner',a,frozenset({'source.search','source.inspect','entity.list'}))
    hit=invoke(s,g,'source.search',{'query':'budget'})
    assert [r['source_id'] for r in hit['result']['matches']]==[sa['id']]
    assert sb['id'] not in str(hit)
    with pytest.raises(NotFound):
        invoke(s,g,'source.inspect',{'id':sb['id']})
    for name in ('openclaw.gateway.call','source.delete','subprocess.exec','artifact.read'):
        with pytest.raises(InvalidInput):
            invoke(s,g,name,{})
    with pytest.raises(InvalidInput):
        invoke(s,g,'source.search',{'query':'budget','gateway_method':'agent.run'})
    with pytest.raises(InvalidInput):
        invoke(s,ToolGrant('',a,frozenset({'source.search'})),'source.search',{'query':'budget'})


def test_entity_and_withdrawal_boundaries(tmp_path):
    s=Store(tmp_path/'db.sqlite3');initialize(s)
    p=s.create_project('P')['id']
    ent=register(s,p,'party','Synthetic party')
    g=ToolGrant('owner',p,frozenset({'entity.list','source.inspect'}))
    assert invoke(s,g,'entity.list',{'kind':'party'})['result'][0]['id']==ent['id']
    with pytest.raises(InvalidInput):
        invoke(s,g,'entity.list',{'kind':'voter-preference'})
    src=s.import_source(p,'a.txt','txt','Synthetic data')
    s.withdraw(p,src['id'])
    with pytest.raises(InvalidInput):
        invoke(s,g,'source.inspect',{'id':src['id']})
