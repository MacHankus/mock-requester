import random
import uuid
from decimal import Decimal


def get_random_string(length: int = 30) -> str:
    return f"{uuid.uuid4().hex[0:length]}"


def get_random_int(start: int = 1, stop: int = 1_000_000) -> int:
    return random.randint(start, stop)


def get_random_float(
    start: float = 0.1, stop: float = 0.9, round_num: int = 2
) -> float:
    return round(random.uniform(start, stop), round_num)


def get_random_decimal() -> Decimal:
    return Decimal(str(random.randint(0, 99)) + "." + str(random.randint(1, 90_000)))
