"""P1.06 typed project-bound deterministic tools for AI and OpenClaw adapters.

No network, shell, device or arbitrary gateway commands. A ToolGrant is made
only by trusted application policy after actor/project authorization.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from pydantic import BaseModel, Field, StrictInt, ValidationError
from .store import Store, InvalidInput
from .research import search
from .political_identity import list_entities

TOOLS = {
    'source.search': 'Read exact project-scoped source line matches',
    'source.inspect': 'Inspect one source from the authorized project',
    'artifact.read': 'Read one saved canonical artifact from the project',
    'entity.list': 'Read user-declared entity IDs in the project',
}


@dataclass(frozen=True)
class ToolGrant:
    actor_id: str
    project_id: str
    allowed_tools: frozenset[str]


class SearchArgs(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    limit: StrictInt = Field(default=8, ge=1, le=25)
    model_config = {'extra': 'forbid'}


class IdArgs(BaseModel):
    id: str = Field(pattern='^[a-f0-9]{32}$')
    model_config = {'extra': 'forbid'}


class ListArgs(BaseModel):
    kind: Literal['jurisdiction','administrative-area','electoral-area','constituency','boundary-version','polling-station','person','party','alliance','organisation','office','election','contest'] | None = None
    model_config = {'extra': 'forbid'}


def invoke(store: Store, grant: ToolGrant, tool: str, arguments: dict) -> dict:
    """Execute only granted, typed, deterministic tools against one project."""
    if not grant.actor_id or not grant.project_id or not grant.allowed_tools:
        raise InvalidInput('Tool invocation requires an authorized actor and project')
    if tool not in TOOLS or tool not in grant.allowed_tools:
        raise InvalidInput('Tool is not approved for this actor/project')
    if not isinstance(arguments, dict):
        raise InvalidInput('Tool arguments must be an object')
    store.project(grant.project_id)
    try:
        if tool == 'source.search':
            body = SearchArgs.model_validate(arguments)
            data = search(store, grant.project_id, body.query, body.limit)
        elif tool == 'source.inspect':
            body = IdArgs.model_validate(arguments)
            data = store.source(grant.project_id, body.id)
            if data['status'] != 'active':
                raise InvalidInput('Source was withdrawn')
        elif tool == 'artifact.read':
            body = IdArgs.model_validate(arguments)
            data = store.artifact(grant.project_id, body.id)
        elif tool == 'entity.list':
            body = ListArgs.model_validate(arguments)
            data = list_entities(store, grant.project_id, body.kind)
        else:
            raise InvalidInput('Unknown tool')
    except ValidationError as exc:
        raise InvalidInput('Tool arguments do not match the approved schema') from exc
    return {'tool': tool, 'project_id': grant.project_id,
            'result': data, 'authoritative_store': 'dotpol-local-sqlite'}
