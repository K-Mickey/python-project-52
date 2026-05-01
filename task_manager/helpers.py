import json
from pathlib import Path


def load_data(file_path):
    file_path = Path(__file__).parent.parent / file_path
    file_data = file_path.read_text()
    return json.loads(file_data)
