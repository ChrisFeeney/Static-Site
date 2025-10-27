from textnode import TextNode, TextType
from blocks import markdown_to_html_node
import os
import shutil


def copy_static_into_public():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    public_dir = os.path.join(parent_dir, "public")
    static_dir = os.path.join(parent_dir, "static")
    if os.path.exists(public_dir):
        print("Removing Public Directory")
        shutil.rmtree(public_dir)
    print("Creating Public Directory")
    os.mkdir(public_dir)
    copy_dir_recursive(static_dir, public_dir)


def copy_dir_recursive(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok = True)
    static_list = os.listdir(src_dir)
    for name in static_list:
        src_path = os.path.join(src_dir, name)
        dst_path = os.path.join(dst_dir, name)
        if os.path.isfile(src_path):
            print(f'Copying {name} from Static to Public')
            shutil.copy(src_path, dst_path)
        else:
            if os.path.exists(src_path):
                copy_dir_recursive(src_path, dst_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No Header Found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_file = f.read()
    with open(template_path) as f:
        template_file = f.read()
    html = markdown_to_html_node(markdown_file)
    html_string = html.to_html()
    title = extract_title(markdown_file)
    updated_template = template_file.replace("{{ Title }}", title)
    updated_template = updated_template.replace("{{ Content }}", html_string)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w') as fp:
        fp.write(updated_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = os.listdir(dir_path_content)
    for content in content_list:
        content_path = os.path.join(dir_path_content, content)
        dest_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(content_path):
            if dest_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
            generate_page(content_path, template_path, dest_path)
        else:
            generate_pages_recursive(content_path, template_path, dest_path)



def main():
    copy_static_into_public()
    generate_pages_recursive("content", "template.html", "public")

main()

