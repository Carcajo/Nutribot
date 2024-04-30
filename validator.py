import re


def validate_target(target: str) -> bool:
    pattern = r"^(похудеть|набрать вес|поддержать вес)$"
    return bool(re.match(pattern, target.lower()))
