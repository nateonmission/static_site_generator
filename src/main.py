import os
import sys
import shutil

from textnode import TextNode, TextTypes
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from textprocessing import split_nodes_delimiter, split_nodes_image, split_nodes_link, blocks_to_BlockNodes, markdown_to_blocks, block_nodes_to_html

def move_content_tree(source_dir, dest_dir):
    print("Moving content tree...")
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


def generate_page(from_path, template_path, dest_path, basepath=""):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")

    with open(from_path, "r") as f:

        markdown_content = f.read()

    title = extract_title(markdown_content)

    blocks = markdown_to_blocks(markdown_content)
    block_nodes = blocks_to_BlockNodes(blocks)
    new_html = block_nodes_to_html(block_nodes)

    with open(template_path, "r") as f:
        template_content = f.read()

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", new_html)
    template_content = template_content.replace('href="/', f'href="{basepath}/')
    template_content = template_content.replace('src="/', f'src="{basepath}/')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path.replace(".md", ".html"), "w") as f:
        f.write(template_content)



def update_site(source_dir, dest_dir, template_path, basepath=""):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isdir(source_path):
            print(f"Processing file: {source_path}")
            os.makedirs(dest_path, exist_ok=True)
            update_site(os.path.join(source_dir, item), os.path.join(dest_dir, item), template_path, basepath)
            print(f"Generated content in: {dest_path}")
        else:
            print(f"Processing file: {source_path}")
            generate_page(source_path, template_path, dest_path)
            print(f"Generated content in: {dest_path}")



def main(*args):
    basepath = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"{basepath = }")
    base_dir = os.getcwd()
    static_source_dir = os.path.join(base_dir, "static")
    content_source_dir = os.path.join(base_dir, "content")
    dest_dir = os.path.join(base_dir, "docs")
    template_path = os.path.join(base_dir, "src", "template.html")

    move_content_tree(static_source_dir, dest_dir)

    update_site(content_source_dir, dest_dir, template_path, basepath)
    print("Site generation complete.")

# Main
if __name__ == "__main__":
    main()
