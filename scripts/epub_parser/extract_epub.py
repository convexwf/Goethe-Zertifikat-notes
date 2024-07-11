# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : Goethe-Zertifikat-notes
# @FileName : scripts/epub_parser/extract_epub.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-07-11 09:43
# @UpdateTime : 2024-07-11 09:43

import os
from collections import defaultdict

import ebooklib
from ebooklib import epub
from pyquery import PyQuery as pq

RESOURCE_EPUB_ROOT = "../../resources/epub"
TMP_ROOT = "output"


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


def extract_most_frequent_seven_thousand_words():
    """
    Extract the most frequent 7000 German words from the epub file

    :return: None
    """
    epub_file = "使用频率最高的7000德语单词.epub"
    epub_path = os.path.join(RESOURCE_EPUB_ROOT, epub_file)
    output_dir = epub_to_html(epub_path, TMP_ROOT)

    def preprocess_content(html):
        doc = pq(html)
        doc("a").remove()
        doc('span[class="kindle-cn-specialtext-bg"]').remove()
        return doc.html()

    result = defaultdict(list)
    info_list = []
    for _id in range(7, 23, 1):
        html_path = f"{output_dir}/id_{_id}.html"
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
            processed_html = preprocess_content(html)
        doc = pq(processed_html)

        title, subtitle = "title", "subtitle"
        for child in doc.children():
            if child.tag == "h2":
                title = pq(child).text().strip()
                info_list.append(f"\n## {title}\n")
            if child.tag == "h3":
                subtitle = pq(child).text().strip()
                info_list.append(f"\n### {subtitle}\n\n")
            if child.tag != "p":
                continue
            child_doc = pq(child)
            if child_doc.attr("class") and child_doc.attr("class") not in [
                "kindle-cn-para-h5"
            ]:
                continue
            word_text = (
                child_doc.text()
                .strip()
                .replace("\n", "")
                .replace("（", " (")
                .replace("）", ")")
            )
            try:
                word = word_text.split("(")[0].strip()
                word_type = word_text.split("(")[1].split(")")[0]
                word_meaning = word_text.split(")", 1)[1].strip()
                result[f"{title} - {subtitle}"].append((word, word_type, word_meaning))
                info_list.append(f"- {word} ({word_type}): {word_meaning}\n")
            except IndexError:
                print(f"Error: {word_text}, IndexError: list index out of range")
                info_list.append(f"- ☆{word_text}☆\n")
                continue
    with open(
        os.path.join(TMP_ROOT, "most_frequent_seven_thousand_words.md"),
        "w+",
        encoding="utf-8",
    ) as f:
        f.writelines(info_list)
    return result


if __name__ == "__main__":
    extract_most_frequent_seven_thousand_words()
