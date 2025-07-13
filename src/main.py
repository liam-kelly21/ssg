from nodes import *
from node_utils import *
import shutil
import os
from pathlib import Path
import sys

TEMPLATE_PATH = "template.html"

def copy_recursive(source,destination):
    #copy recursively
    for entry in os.listdir(source):
        src = os.path.join(source,entry)
        dst = os.path.join(destination,entry)
        if os.path.isfile(src):
            print(shutil.copy(src,dst))
        elif os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            os.mkdir(dst)
            copy_recursive(src,dst)
        else:
            print("Not a file or directory, skipping")
    
    return

def generate_page(from_path,template_path,dest_path,base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    #Read source
    try:
        with open(from_path) as file:
            markdown = file.read()
    except OSError as e:
        print(f"Source file error: {e}")
    #Read template
    try:
        with open(template_path) as file:
            template = file.read()
    except OSError as e:
        print(f"Template file error: {e}")
    #Convert MD to HTML
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    #Create page
    page = template.replace("{{ Title }}",title).replace("{{ Content }}",content)
    #set link paths
    page = page.replace("href=\"/",f"href=\"{base_path}").replace("src=\"/",f"src=\"{base_path}")

    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'w') as f:
            f.write(page)
    except IOError as e:
        print(f"Error writing file {dest_path}: {e}")

def generate_pages_recursively(dir_path_content,template_path,dest_dir_path,base_path):
    for entry in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content,entry)
        dst = os.path.join(dest_dir_path,entry)
        if os.path.isfile(src):
            dst = Path(dst).with_suffix(".html")
            generate_page(src,template_path,dst,base_path)
        elif os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            os.mkdir(dst)
            generate_pages_recursively(src,template_path,dst,base_path)
        else:
            print("Not a file or directory, skipping")

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1] + "/"
    copy_recursive("static","docs")
    generate_pages_recursively("content",TEMPLATE_PATH,"docs",basepath)

if __name__ == "__main__":
    main()