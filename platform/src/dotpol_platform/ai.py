"""One model provider boundary. No automatic network calls or model downloads."""
import os
from urllib.parse import urlsplit


def status() -> dict:
    endpoint=os.getenv('DOTPOL_OLLAMA_URL','http://127.0.0.1:11434')
    parsed=urlsplit(endpoint)
    if parsed.scheme != 'http' or parsed.hostname not in ('127.0.0.1','localhost','::1') or parsed.username or parsed.password:
        return {'available':False,'provider':'ollama','status':'invalid-local-endpoint',
                'message':'DOTPOL_OLLAMA_URL must be local HTTP; external providers are not enabled by default.'}
    # No probing or download automatically, so cold start remains offline.
    return {'available':False,'provider':'ollama','status':'not-probed',
            'message':'Local model optional; source search works without AI. Model execution is not activated in this preview.'}
