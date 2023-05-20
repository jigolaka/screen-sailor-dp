import os


def find_path(file_name: str):
    script_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))

    for root, _, files in os.walk(root_dir):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            return file_path

    return None
