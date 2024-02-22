import json
import logging

def json_encode(data: dict) -> str:
    return json.dumps(data)

def json_decode(data: str) -> dict:
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        logging.error("Could not decode: "+ ("%r" % data))
        return {}

def is_json(data: str) -> bool:
    return data.strip().startswith('{') and data.strip().endswith('}')
