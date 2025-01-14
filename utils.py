"""
    utility functions to get documentation and other useful contents
"""
import os

def read_file(filename: str) -> str or None:
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
        
def get_slurm_conf(file_path="/etc/slurm/slurm.conf"):
    with open(file_path, 'r') as f:
        text = f.read()
    # chop unnecessary lines and return
    return text

def get_doc_content(location="doc", extension=".md") -> str:
    markdown_text = []
    for root, _, files in os.walk(location):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        text = f.read()
                    markdown_text.append(text)
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")
    return "\n".join(markdown_text)
