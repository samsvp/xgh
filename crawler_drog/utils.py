import json
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


def load_json(filename: str) -> Dict[Any, Any]:
    """
    Loads a json with the given file name.
    If no file is found then an empty dict is returned.
    """
    try:
        with open(filename, "r", encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {}
    return history


def load_json_tmp(pid: int) -> Dict[Any, Any]:
    try:
        with open(f"data_{pid}.json.tmp", "r", encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {}
    return history


def update_json(data: Dict[Any, Any], i: str, 
        pid: int, filename:str) -> Dict[Any, Any]:
    history = load_json(filename)
    try:
        if i in history: history[i].update(data)
        else: history[i] = data

        with open(f"data_{pid}.json.tmp", "w", encoding='utf-8') as data_file:
            json.dump(history, data_file, indent=True)
    except Exception as e:
        print(e)

    return history