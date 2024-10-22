import shutil
import os
import re
from htmlnode import HTMLNode
from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from copy import copy

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "text":
            return LeafNode(text_node.text)
        case "bold":
            return LeafNode(text_node.text, "b")
        case "italic":
            return LeafNode(text_node.text, "i")
        case "code":
            return LeafNode(text_node.text, "code")
        case "link":
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case "image":
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _: 
            raise Exception("No text type was matched")
    

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        is_between_delimiters = False
        old_node_copy = copy(old_node)
        while len(old_node_copy.text):
            delimiter_index = old_node_copy.text.find(delimiter)

            if delimiter_index == -1:
                new_nodes.append(old_node_copy)
                break

            text = old_node_copy.text[0:delimiter_index]
            old_node_copy.text = old_node_copy.text[delimiter_index+len(delimiter):]

            if not len(text):
                is_between_delimiters = not is_between_delimiters
                continue

            if is_between_delimiters:
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, old_node_copy.text_type))

            is_between_delimiters = not is_between_delimiters
    return new_nodes

nodes = [TextNode("**bold**", "text")]
new_nodes = split_nodes_delimiter(nodes, "**", "bold")


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        node_copy = copy(old_node)
        images = extract_markdown_images(node_copy.text)
        if len(images):
            images_index = 0
            while len(node_copy.text) and images_index < len(images): 
                sections = node_copy.text.split(f"![{images[images_index][0]}]({images[images_index][1]})", 1)
                node_copy.text = sections[1]
                new_nodes.append(create_node_from_section(sections[0]))
                new_nodes.append(TextNode(images[images_index][0], "image", images[images_index][1]))
                images_index += 1


        new_nodes.append(node_copy)
    
    new_nodes = list(filter(lambda node: (not len(node.text) == 0), new_nodes))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        node_copy = copy(old_node)
        links = extract_markdown_links(node_copy.text)
        if len(links):
            links_index = 0
            while len(node_copy.text) and links_index < len(links): 
                sections = node_copy.text.split(f"[{links[links_index][0]}]({links[links_index][1]})", 1)
                node_copy.text = sections[1]
                new_nodes.append(create_node_from_section(sections[0]))
                new_nodes.append(TextNode(links[links_index][0], "link", links[links_index][1]))
                links_index += 1


        new_nodes.append(node_copy)
    
    new_nodes = list(filter(lambda node: (not len(node.text) == 0), new_nodes))
    return new_nodes

def create_node_from_section(text):
    return TextNode(text, "text")


def text_to_textnodes(text: str) -> list[TextNode]:
    textnodes = [create_node_from_section(text)]
    block_types = [("code", "`"), ("bold", "**"), ("italic", "*")]
    for text_type, delimiter in block_types:
        textnodes  = split_nodes_delimiter(textnodes, delimiter, text_type)
    textnodes = split_nodes_image(split_nodes_link(textnodes))
    return textnodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    for i in range(len(blocks) - 1, -1, -1):
        if blocks[i].startswith("\n"):
            blocks[i] =  blocks[i][1:]
        blocks[i].strip()

        if blocks[i] == "":
            del blocks[i]
            continue    

    return blocks
    

def block_to_block_type(block: str) -> str:
    type = ""
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        type = "heading"
    elif re.match(r"^```(?!`)", block) and re.search(r"(?<!`)```$", block): 
        type = "code"
    elif all(re.match(r"^> ", line) for line in lines):
        type = "quote"
    elif all(re.match(r"^\* ", line) or re.match(r"^- ", line) for line in lines):
        type = "unordered_list"
    elif all(re.match(r"^\d+. ", line) for line in lines):
        type = "ordered_list"
    else:
        type = "paragraph"
    return type


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    main_node = ParentNode("div", [])
    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                hierarchy = 0
                i = 0
                while (block[i] == "#"): 
                    hierarchy += 1
                    i += 1
                heading = ParentNode(f"h{hierarchy}", text_to_children(block[i + 1:]))
                main_node.children.append(heading)
            case "code":
                code = ParentNode("code", text_to_children(block))
                pre = ParentNode("pre", [code])
                main_node.children.append(pre)
            case "unordered_list":
                lines = get_ul_li_items_content(block)
                children = lines_list_to_children(lines)
                ul = children_to_ul(children)
                main_node.children.append(ul)
            case "ordered_list":
                lines = get_ol_li_items_content(block)
                children = lines_list_to_children(lines)
                ol = children_to_ol(children)
                main_node.children.append(ol)
            case "paragraph":
                children = text_to_children(block)
                main_node.children.append(ParentNode("p", children))    
            case "quote":
                quote_text = get_quote_text(block)
                children = text_to_children(quote_text)
                main_node.children.append(ParentNode("blockquote", children))
                
            case _:
                raise NotImplementedError()
    return main_node
            

def text_to_children(text: str) -> list[LeafNode]:
    leaf_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    return leaf_nodes


def children_to_ul(children: list[LeafNode]) -> ParentNode:
    return ParentNode("ul", children)


def children_to_ol(children: list[LeafNode]) -> ParentNode:
    return ParentNode("ol", children)


def lines_list_to_children(lines: list[str]) -> list[LeafNode]:
    items = []
    for line in lines:
        children = text_to_children(line)
        items.append(ParentNode("li", children))
    return items


def get_ul_li_items_content(text: str) -> list[str]:
    lines = text.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i][2:]
    return lines


def get_ol_li_items_content(text: str) -> list[str]:
    lines = text.split("\n")
    for i in range(len(lines)):
        lines[i] = re.match(r"(^\d+. )(.*)", lines[i]).group(2)
    return lines


def get_quote_text(text: str) -> str:
    return " ".join(line.lstrip("> ") for line in text.splitlines())


def copy_contents(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
      
  
    if os.path.isfile(src):
        actual_dest = shutil.copy(src, dest)
        print(actual_dest)
        return    

    os.mkdir(dest)  
    paths = os.listdir(src)
    for path in paths:
        copy_contents(os.path.join(src, path), os.path.join(dest, path))


def extract_title(markdown):
    lines = markdown.split("\n")
    title = None
    for line in lines:
        if line.startswith("# "):
            title = line
            break
    if not title:
        raise Exception("Title not found")
    return title        


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path),exist_ok=True)
    f = open(dest_path, 'w')
    f.write(template)
    f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path.replace(".md", ".html"))
        return    

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)  
    paths = os.listdir(dir_path_content)
    for path in paths:
        generate_pages_recursive(os.path.join(dir_path_content, path), template_path, os.path.join(dest_dir_path, path))