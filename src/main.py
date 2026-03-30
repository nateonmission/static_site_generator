import os
import shutil

from textnode import TextNode, TextTypes
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from textprocessing import split_nodes_delimiter, split_nodes_image, split_nodes_link

def move_content_tree(source_dir, dest_dir):
    try:
        shutil.rmtree(dest_dir)
        print(f"Deleted old content: {dest_dir}")
    except FileNotFoundError as e:
        print(f"Directory {dest_dir} does not exist, skipping deletion.")
        
    try:
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")
    except FileExistsError:
        print(f"Directory {dest_dir} already exists.")
        
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isdir(source_path):
            os.mkdir(dest_path)
            move_content_tree(source_path, dest_path)
            print(f"Copied directory: {source_path} to {dest_path}")
        else:
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")


def extract_title(markdown):
    lines = markdown.splitlines()
    title_found = False
    while not title_found and lines:
        line = lines.pop(0)
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown content.")

#TODO
def generate_page(source_dir, template_dir, dest_dir):
    pass

def main():

    base_dir =os.getcwd()
    source_dir = os.path.join(base_dir, "static")
    dest_dir = os.path.join(base_dir, "public")
    template_dir = os.path.join(base_dir, "template.html")
    
    
        print("Moving content tree...")
    move_content_tree(source_dir, dest_dir)
    
    


if __name__ == "__main__":
    main()
