# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : Goethe-Zertifikat-notes
# @FileName : scripts/epub_parser/most_frequent_seven_thousand.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-07-14 09:49
# @UpdateTime : 2024-07-14 09:49

import os
from collections import defaultdict

from extract_epub import epub_to_html
from pyquery import PyQuery as pq

RESOURCE_EPUB_ROOT = "../../resources/epub"
TMP_ROOT = "output"


def preprocess_content(html):
    doc = pq(html)
    doc("a").remove()
    doc('span[class="kindle-cn-specialtext-bg"]').remove()
    return doc.html()


def extract_most_frequent_seven_thousand_noun():
    """
    Extract the most frequent 7000 German words from the epub file

    :return: None
    """
    epub_file = "使用频率最高的7000德语单词.epub"
    epub_path = os.path.join(RESOURCE_EPUB_ROOT, epub_file)
    output_dir = epub_to_html(epub_path, TMP_ROOT)

    result = defaultdict(list)
    info_list = [f"# 使用频率最高的7000德语单词-名词\n"]
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
        os.path.join(TMP_ROOT, "使用频率最高的7000德语单词-名词.md"),
        "w+",
        encoding="utf-8",
    ) as f:
        f.writelines(info_list)
    return result


def extract_most_frequent_seven_thousand_verb():
    """
    Extract the most frequent 7000 German words from the epub file

    :return: None
    """
    epub_file = "使用频率最高的7000德语单词.epub"
    epub_path = os.path.join(RESOURCE_EPUB_ROOT, epub_file)
    output_dir = epub_to_html(epub_path, TMP_ROOT)

    result = defaultdict(list)
    info_list = [f"# 使用频率最高的7000德语单词-动词\n"]
    for _id in range(23, 29, 1):
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
        os.path.join(TMP_ROOT, "使用频率最高的7000德语单词-动词.md"),
        "w+",
        encoding="utf-8",
    ) as f:
        f.writelines(info_list)
    return result


def extract_most_frequent_seven_thousand_adj():
    """
    Extract the most frequent 7000 German words from the epub file

    :return: None
    """
    epub_file = "使用频率最高的7000德语单词.epub"
    epub_path = os.path.join(RESOURCE_EPUB_ROOT, epub_file)
    output_dir = epub_to_html(epub_path, TMP_ROOT)

    result = defaultdict(list)
    info_list = [f"# 使用频率最高的7000德语单词-形容词\n"]
    for _id in range(29, 31, 1):
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
        os.path.join(TMP_ROOT, "使用频率最高的7000德语单词-形容词.md"),
        "w+",
        encoding="utf-8",
    ) as f:
        f.writelines(info_list)
    return result


def extract_most_frequent_seven_thousand_adv():
    """
    Extract the most frequent 7000 German words from the epub file

    :return: None
    """
    epub_file = "使用频率最高的7000德语单词.epub"
    epub_path = os.path.join(RESOURCE_EPUB_ROOT, epub_file)
    output_dir = epub_to_html(epub_path, TMP_ROOT)

    result = defaultdict(list)
    info_list = [f"# 使用频率最高的7000德语单词-副词\n"]
    for _id in range(31, 32, 1):
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
        os.path.join(TMP_ROOT, "使用频率最高的7000德语单词-副词.md"),
        "w+",
        encoding="utf-8",
    ) as f:
        f.writelines(info_list)


if __name__ == "__main__":
    extract_most_frequent_seven_thousand_noun()
    extract_most_frequent_seven_thousand_verb()
    extract_most_frequent_seven_thousand_adj()
    extract_most_frequent_seven_thousand_adv()
