# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : Goethe-Zertifikat-notes
# @FileName : scripts/epub_parser/extract_epub.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-07-11 09:43
# @UpdateTime : 2024-07-14 09:49

import os

import ebooklib
from ebooklib import epub


def epub_to_html(epub_path, output_html_dir):
    """
    Extract the content of an epub file to html files

    :param epub_path: str, the path of the epub file
    :param output_html_dir: str, the directory to save the html files

    :return: str, the directory to save the html files
    """
    book = epub.read_epub(epub_path)
    epub_name = os.path.basename(epub_path).replace(".epub", "")
    output_dir = os.path.join(output_html_dir, epub_name)
    os.makedirs(output_dir, exist_ok=True)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_body_content()
            content_str = content.decode("utf-8").replace("&#13;", "")

            html_filename = f"{item.get_id()}.html"
            html_path = os.path.join(output_dir, html_filename)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(content_str)
    return output_dir
