from os import makedirs
from os.path import dirname


# ====================
def save_text_to_file(text: str, file_path: str):

    makedirs(dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
