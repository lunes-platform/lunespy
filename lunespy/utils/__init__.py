import json

def export_dict(path: str, name: str, dict: dict) -> bool:
    full_path = f"{path}/{name}"
    with open(full_path, 'w') as file:
        file.write(json.dumps(dict))
