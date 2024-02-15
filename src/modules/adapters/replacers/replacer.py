import re
from typing import Any
from typing import Dict


def get_val_from_body(path: str, body: Dict):
    levels = path.split(".")
    ref = None
    first = True
    for level in levels:
        if first:
            ref = body.get(level, None)
            first = False
        else:
            if ref is None:
                return None
            ref = ref.get(level, None)
        if ref is None:
            return None
    return ref


def clean_placeholder(placeholder: str):
    return placeholder[2:-1]


def replace_placeholder(val: Any, body: Dict):
    if isinstance(val, str):
        reg = r"\$\{[\w\.]+\}"
        placeholders = re.findall(reg, val)
        for placeholder in placeholders:
            val = val.replace(
                placeholder,
                str(get_val_from_body(clean_placeholder(placeholder), body)),
            )
            try:
                val = int(val)
            except Exception:
                pass
    return val


def crawler(d: Any, body: Dict):
    if isinstance(d, dict):
        for key, val in d.items():
            if isinstance(val, list) or isinstance(val, dict):
                crawler(val, body)
            else:
                d[key] = replace_placeholder(val, body)
    elif isinstance(d, list):
        for idx, item in enumerate(d):
            if isinstance(item, list) or isinstance(item, dict):
                crawler(item, body)
            else:
                d[idx] = replace_placeholder(item, body)
