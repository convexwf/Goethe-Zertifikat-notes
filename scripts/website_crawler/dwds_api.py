# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : Goethe-Zertifikat-notes
# @FileName : dwds_api.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-06-06 18:01
# @UpdateTime : 2024-06-27 17:44

import csv
import json
import os
import random
import time
from collections import defaultdict

import requests
from reverso_conjugation import fetch_reverso_conjugation

output_dir = "output"


def fetch_goethe_words():
    """
    Fetch the Goethe words from the DWDS API
    """
    base_url = "https://www.dwds.de/api/lemma/goethe/{level}.{ext}"

    csv_root = f"{output_dir}/goethe_word/csv"
    os.makedirs(csv_root, exist_ok=True)
    json_root = f"{output_dir}/goethe_word/json"
    os.makedirs(json_root, exist_ok=True)

    # csv file
    for level in ["A1", "A2", "B1"]:
        url = base_url.format(level=level, ext="csv")
        response = requests.get(url)
        response.raise_for_status()
        csv_path = f"{csv_root}/{level}.csv"
        with open(csv_path, "wb") as f:
            f.write(response.content)

    # json file
    for level in ["A1", "A2", "B1"]:
        url = base_url.format(level=level, ext="json")
        response = requests.get(url)
        response.raise_for_status()
        json_path = f"{json_root}/{level}.json"
        json_obj = response.json()
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=2)


def fetch_word_ipa(word):
    """
    Fetch the IPA of the given word list from the DWDS API
    """
    base_url = "https://www.dwds.de/api/ipa/?q={word}"

    url = base_url.format(word=word)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text} for {url}")
        return None
    return response.json()


def fetch_word_freq(word):
    """
    Fetch the frequency of the given word list from the DWDS API
    """
    base_url = "https://www.dwds.de/api/frequency/?q={word}"

    url = base_url.format(word=word)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text} for {url}")
        return None
    response_dict = response.json()
    response_dict.pop("q")
    return response_dict


def check_goethe_words():
    """
    Check the Goethe words
    """
    csv_root = f"{output_dir}/goethe_word/csv"

    goethe_word_list = []
    for level in ["A1", "A2", "B1"]:
        csv_path = f"{csv_root}/{level}.csv"
        # use csv package
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for no, row in enumerate(reader):
                if no == 0:
                    continue
                Lemma = row[0]
                dwds_url = row[1]
                Wortarten = row[2]
                nur_im_Plural = row[5]
                goethe_word_list.append(
                    {
                        "Lemma": Lemma,
                        "Wortarten": Wortarten,
                        "nur_im_Plural": nur_im_Plural,
                        "level": level,
                        "dwds_url": dwds_url,
                    }
                )
    with open(
        f"{output_dir}/goethe_word/goethe_word_list.json", "w", encoding="utf-8"
    ) as f:
        json.dump(goethe_word_list, f, ensure_ascii=False, indent=2)


def check_goethe_word_ipa():
    """
    Check the IPA of the Goethe words
    """
    with open(
        f"{output_dir}/goethe_word/goethe_word_list.json", "r", encoding="utf-8"
    ) as f:
        goethe_word_list = json.load(f)

    for i, goethe_word in enumerate(goethe_word_list):
        Lemma = goethe_word["Lemma"]
        if "dwds_ipa" in goethe_word:
            continue
        time.sleep(random.uniform(0.1, 3))
        ipa_dict = fetch_word_ipa(Lemma)
        if ipa_dict:
            goethe_word["dwds_ipa"] = ipa_dict
            print(f"Successfully fetched the IPA for the word: {Lemma}")
        else:
            print(f"******* Error: Failed to fetch the IPA for the word: {Lemma}")

        if i % 50 == 0:
            with open(
                f"{output_dir}/goethe_word/goethe_word_list.json", "w", encoding="utf-8"
            ) as f:
                json.dump(goethe_word_list, f, ensure_ascii=False, indent=2)

    with open(
        f"{output_dir}/goethe_word/goethe_word_list.json", "w+", encoding="utf-8"
    ) as f:
        json.dump(goethe_word_list, f, ensure_ascii=False, indent=2)


def check_goethe_word_freq():
    """
    Check the frequency of the Goethe words
    """
    with open(
        f"{output_dir}/goethe_word/goethe_word_list.json", "r", encoding="utf-8"
    ) as f:
        goethe_word_list = json.load(f)

    for i, goethe_word in enumerate(goethe_word_list):
        Lemma = goethe_word["Lemma"]
        if "dwds_freq" in goethe_word:
            continue
        time.sleep(random.uniform(0.1, 3))
        freq_dict = fetch_word_freq(Lemma)
        if freq_dict:
            goethe_word["dwds_freq"] = freq_dict
            print(f"Successfully fetched the frequency for the word: {Lemma}")
        else:
            print(f"******* Error: Failed to fetch the frequency for the word: {Lemma}")

        if i % 50 == 0:
            with open(
                f"{output_dir}/goethe_word/goethe_word_list.json", "w", encoding="utf-8"
            ) as f:
                json.dump(goethe_word_list, f, ensure_ascii=False, indent=2)

    with open(
        f"{output_dir}/goethe_word/goethe_word_list.json", "w+", encoding="utf-8"
    ) as f:
        json.dump(goethe_word_list, f, ensure_ascii=False, indent=2)


def check_goethe_word_Wortarten():
    """
    Extract the Wortarten from the csv file
    """
    with open(
        f"{output_dir}/goethe_word/goethe_word_list.json", "r", encoding="utf-8"
    ) as f:
        goethe_word_list = json.load(f)

    Wortarten_dict = defaultdict(int)
    for goethe_word in goethe_word_list:
        Wortarten = goethe_word["Wortarten"]
        Wortarten_dict[Wortarten] += 1
    Wortaarten_count_list = sorted(
        Wortarten_dict.items(), key=lambda x: x[1], reverse=True
    )
    for Wortarten, count in Wortaarten_count_list:
        print(f"{Wortarten}: {count}")

    return Wortarten_dict


def extract_goethe_verb_conjugation():
    """
    Extract the Goethe verb conjugation from the csv file
    """
    with open(
        f"{output_dir}/goethe_word/goethe_verb_list.json", "r", encoding="utf-8"
    ) as f:
        goethe_word_list = json.load(f)

    verb_list = []
    for goethe_word in goethe_word_list:
        Wortarten = goethe_word["Wortarten"]
        # goethe_word.pop("nur_im_Plural")
        if "Verb" == Wortarten:
            verb_list.append(goethe_word)

    for verb in verb_list:
        if "reverso_url" in verb:
            continue
        Lemma = verb["Lemma"]
        is_success, conj_result_dict = fetch_reverso_conjugation(Lemma)
        if is_success:
            verb["reverso_url"] = (
                f"https://conjugator.reverso.net/conjugation-german-verb-{Lemma}.html"
            )
            verb["conjugation"] = conj_result_dict
            print(f"Successfully fetched the conjugation for the verb: {Lemma}")
        else:
            print(
                f"******* Error: Failed to fetch the conjugation for the verb: {Lemma}"
            )

    with open(
        f"{output_dir}/goethe_word/goethe_verb_list.json", "w", encoding="utf-8"
    ) as f:
        json.dump(verb_list, f, ensure_ascii=False, indent=2)

    return verb_list


if __name__ == "__main__":
    # fetch_goethe_words()
    # check_goethe_words()
    # check_goethe_word_ipa()
    check_goethe_word_freq()
