import re
from typing import Any
from typing import Dict


def get_val_from_replacers(path: str, replacers: Dict):
    # Raises key error when key is not in dict
    levels = path.split(".")
    ref = None
    first = True
    for level in levels:
        if first:
            ref = replacers[level]
            first = False
        else:
            if ref is None:
                return None
            ref = ref[level]
        if ref is None:
            return None
    return ref



def clean_placeholder(placeholder: str):
    return placeholder[2:-1]


def replace_placeholder(val: Any, replacers: Dict):
    if isinstance(val, str):
        reg = r"\$\{[\w\[\]]+[\w\.]+\}"
        placeholders = re.findall(reg, val)
        for placeholder in placeholders:
            try:
                val = val.replace(
                    placeholder,
                    str(get_val_from_replacers(clean_placeholder(placeholder), replacers)),
                )
            except KeyError:
                pass
            try:
                val = int(val)
            except Exception:
                pass
    return val


def replacer(d: Any, replacers: Dict):
    if isinstance(d, dict):
        for key, val in d.items():
            if isinstance(val, list) or isinstance(val, dict):
                replacer(val, replacers)
            else:
                d[key] = replace_placeholder(val, replacers)
    elif isinstance(d, list):
        for idx, item in enumerate(d):
            if isinstance(item, list) or isinstance(item, dict):
                replacer(item, replacers)
            else:
                d[idx] = replace_placeholder(item, replacers)
