from typing import Any, Dict


def find_by_key(data: Dict[Any, Any], target: Any) -> Any:
    """
    Finds the target key given a nested dictionary
    and return its value
    """
    for key, value in data.items():
        if key == target:
            yield value
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif isinstance(value, list):
            for v in value:
                if isinstance(v, dict):
                    yield from find_by_key(v, target)


def price_to_num(price: str) -> float:
    """
    Converts a price string (format-> "R$ 5.555,99") into a float
    """
    return float(price[3:].replace(".","").replace(",","."))
