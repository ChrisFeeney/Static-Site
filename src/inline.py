import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
        else:
            if delimiter is not None:
                if node.text.count(delimiter)%2 == 0:
                    split_text = node.text.split(delimiter)
                    for i in range(len(split_text)):
                        if split_text[i] == "":
                            continue
                        if i % 2 ==0:
                            new_node.append(TextNode(split_text[i], TextType.TEXT))
                        elif i % 2 != 0:
                            new_node.append(TextNode(split_text[i], text_type))
                else:
                    raise ValueError("invalid markdown, formatted section not closed")
    return new_node

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        remaining = node.text
        images = extract_markdown_images(remaining)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections= remaining.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            sections= remaining.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        remaining = node.text
        links = extract_markdown_links(remaining)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = remaining.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0]!= "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    starting = [TextNode(text, TextType.TEXT)]
    starting = split_nodes_delimiter(starting, "`", TextType.CODE)
    starting = split_nodes_delimiter(starting, "**", TextType.BOLD)
    starting = split_nodes_delimiter(starting, "_", TextType.ITALIC)
    starting = split_nodes_image(starting)
    starting = split_nodes_link(starting)
    return starting

