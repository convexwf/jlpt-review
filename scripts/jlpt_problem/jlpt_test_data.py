# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : JLPT-review
# @FileName : ts/jlpt_problem/jlpt_test_data.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-12-21 10:41
# @UpdateTime : 2024-12-29 22:13

import re
import time

import requests
from pyquery import PyQuery as pq

# https://www.dethitiengnhat.com/en/jlpt/N1/201012/1

BASE_URL = "https://www.dethitiengnhat.com/en/jlpt/{level}/{year_month}/{part}"


def retry_url(url: str, retry_times: int = 5) -> str:
    for i in range(retry_times):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response
        except Exception as e:
            pass
        time.sleep(1)
        print(f"Retry {url} . Retry times: {i + 1}")
    raise Exception(f"Failed to get {url}")


def extract_jlpt_N1_vocab_1to3(year_month_list):

    info_list = "# JLPT N1 Vocabulary (Type 1-3)\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="1")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Vocabulary (Type 1-3) ...")

        result = [[] for _ in range(19)]
        question_block = doc("div[class='question_list']")
        for number, question in enumerate(list(question_block.items())[0:19]):
            u_tag = question("u")
            u_text = ""
            if u_tag:
                u_text = u_tag.text().strip()
            question_text = question.text().strip()
            pivot = 1 if number < 9 else 2
            question_no = question_text[0:pivot]
            question_text = (
                "**【" + question_no + "】** " + question_text[pivot + 1 :].strip()
            )
            question_text = question_text.replace(f"\n{u_text}\n", f"<u>{u_text}</u>")
            result[number].append(question_text)

        answer_block = doc("div[class='answers']")
        four_answers = list(answer_block.items())[0 : 19 * 4]
        for number in range(19):
            answer_text = ">"
            for answer in four_answers[number * 4 : number * 4 + 4]:
                choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                answer_text += " " + choice_text
            result[number].append(answer_text)

        info_list += f"## {year_month}\n\n"
        for question, answer in result:
            info_list += f"{question}\n\n{answer}\n\n"

    with open("jlpt_N1_vocab_type1to3.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def extract_jlpt_N1_vocab_type4(year_month_list):

    info_list = "# JLPT N1 Vocabulary (Type 4)\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="2")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Vocabulary (Type 4) ...")

        result = [[] for _ in range(6)]
        question_block = doc("div[class='question_list']")
        for number, question in enumerate(list(question_block.items())[19 : 19 + 6]):
            question_text = question.text().strip()
            question_no = question_text[0:2]
            question_text = "**【" + question_no + "】** " + question_text[3:].strip()
            result[number].append(question_text)

        answer_block = doc("div[class='answers']")
        four_answers = list(answer_block.items())[76 : 76 + 6 * 4]
        for number in range(6):
            answer_text = ""
            for answer in four_answers[number * 4 : number * 4 + 4]:
                choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                u_tag = answer("u")
                u_text = ""
                if u_tag:
                    u_text = u_tag.text().strip()
                answer_text += (
                    "> "
                    + choice_text.replace(f"\n{u_text}\n", f"<u>{u_text}</u>")
                    + "\n"
                )
            result[number].append(answer_text)

        info_list += f"## {year_month}\n\n"
        for question, answer in result:
            info_list += f"{question}\n\n{answer}\n"

    with open("jlpt_N1_vocab_type4.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def extract_jlpt_N1_grammar_type4(year_month_list):

    info_list = "# JLPT N1 Grammar (Type 4)\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="1")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Grammar (Type 4) ...")

        result = [[] for _ in range(10)]
        question_block = doc("div[class='question_list']")
        for number, question in enumerate(list(question_block.items())[25 : 25 + 10]):
            question_text = question.text().strip()
            question_no = question_text[0:2]
            question_text = "**【" + question_no + "】** " + question_text[3:].strip()
            result[number].append(question_text)

        answer_block = doc("div[class='answers']")
        four_answers = list(answer_block.items())[100 : 100 + 10 * 4]
        for number in range(10):
            answer_text = ">"
            for answer in four_answers[number * 4 : number * 4 + 4]:
                choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                answer_text += " " + choice_text
            result[number].append(answer_text)

        info_list += f"## {year_month}\n\n"
        for question, answer in result:
            info_list += f"{question}\n\n{answer}\n\n"

    with open("jlpt_N1_grammar_type4.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def extract_jlpt_N1_grammar_type5(year_month_list):

    info_list = "# JLPT N1 Grammar (Type 5)\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="2")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Grammar (Type 5) ...")

        result = [[] for _ in range(5)]
        question_block = doc("div[class='question_list']")
        for number, question in enumerate(list(question_block.items())[35 : 35 + 5]):
            question_text = question.text().strip()
            question_no = question_text[0:2]
            question_text = "**【" + question_no + "】** " + question_text[3:].strip()
            result[number].append(question_text)

        answer_block = doc("div[class='answers']")
        four_answers = list(answer_block.items())[140 : 140 + 5 * 4]
        for number in range(5):
            answer_text = ">"
            for answer in four_answers[number * 4 : number * 4 + 4]:
                choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                answer_text += " " + choice_text
            result[number].append(answer_text)

        info_list += f"## {year_month}\n\n"
        for question, answer in result:
            info_list += f"{question}\n\n{answer}\n\n"

    with open("jlpt_N1_grammar_type5.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def extract_jlpt_N1_grammar_type6(year_month_list):

    info_list = "# JLPT N1 Grammar (Type 6)\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="1")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Grammar (Type 6) ...")

        question_block = doc("div[class='question_content']")
        if not question_block:
            continue
        question_text = question_block.text().strip()
        info_list += f"## {year_month}\n\n"
        info_list += f"{question_text}\n\n"

        answer_block = doc("div[class='answers']")
        four_answers = list(answer_block.items())[160 : 160 + 4 * 5]
        for number in range(5):
            answer_text = f"**【{40 + number + 1}】**\n"
            for answer in four_answers[number * 4 : number * 4 + 4]:
                choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                answer_text += "> " + choice_text + "\n"
            info_list += f"{answer_text}\n"

    with open("jlpt_N1_grammar_type6.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def extract_jlpt_N1_reading(year_month_list):
    filename_list = [
        "JLPT.N1.短文内容理解",
        "JLPT.N1.中文内容理解",
        "JLPT.N1.長文内容理解",
        "JLPT.N1.統合理解",
        "JLPT.N1.主張内容理解",
    ]
    info_list = [
        [f"# JLPT N1 短文内容理解\n\n"],
        [f"# JLPT N1 中文内容理解\n\n"],
        [f"# JLPT N1 長文内容理解\n\n"],
        [f"# JLPT N1 統合理解\n\n"],
        [f"# JLPT N1 主張内容理解\n\n"],
    ]

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="3")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Reading (Type 1) ...")

        div_form = doc("form[name='dttn']")
        section_list = []
        big_index = 0
        for div_child in div_form.children():
            if div_child.tag != "div":
                continue
            if not div_child.attrib.get("class"):
                continue
            if div_child.attrib.get("class") == "big_item":
                big_index += 1
                if big_index == 6:
                    break
                section_list.append([])
            elif div_child.attrib.get("class") == "question_content":
                question_content_block = doc(div_child)
                question_content = question_content_block.text().strip()
                u_tag = list(question_content_block("u").items())
                if u_tag:
                    for _u_tag in u_tag:
                        u_text = _u_tag.text().strip()
                        question_content = question_content.replace(
                            f"\n{u_text}\n", f"<u>{u_text}</u>"
                        )
                section_list[big_index - 1].append([question_content])
            elif div_child.attrib.get("class") == "question_list":
                question_list_block = doc(div_child)
                question_list = question_list_block.text().strip()
                u_tag = question_list_block("u")
                if u_tag:
                    u_text = u_tag.text().strip()
                    question_list = question_list.replace(
                        f"\n{u_text}\n", f"<u>{u_text}</u>"
                    )
                question_no = question_list[0:2]
                question_list = (
                    "**【" + question_no + "】** " + question_list[3:].strip()
                )
                section_list[big_index - 1][-1].append(question_list)
            elif div_child.attrib.get("class").startswith("answer"):
                four_answers = list(doc(div_child)("div[class='answers']").items())
                answer_text = ""
                for answer in four_answers:
                    choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                    answer_text += "> " + choice_text + "  \n"
                section_list[big_index - 1][-1].append(answer_text[:-1])

        # print(section_list)

        for index in range(big_index - 1):
            info_list[index] += f"## {year_month}\n\n"
            for _text in section_list[index]:
                for text in _text:
                    info_list[index] += f"{text}\n\n"

    for index in range(5):
        with open(
            f"{filename_list[index]}.md", "w+", encoding="utf-8", newline="\n"
        ) as f:
            f.writelines(info_list[index])


def extract_jlpt_vocabulary(year_month_list):
    filename_list = [
        "JLPT.N1.漢字読み",
        "JLPT.N1.文脈規定",
        "JLPT.N1.言い換え類義",
    ]
    info_list = [
        [f"# JLPT N1 漢字読み\n\n"],
        [f"# JLPT N1 文脈規定\n\n"],
        [f"# JLPT N1 言い換え類義\n\n"],
    ]
    # search_word_list = [[] for _ in range(3)]

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="1")
        response = retry_url(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Vocabulary ...")

        div_form = doc("form[name='dttn']")
        section_list = []
        big_index = 0
        title_no = 0
        for div_child in div_form.children():
            if div_child.tag != "div":
                continue
            if not div_child.attrib.get("class"):
                continue
            if div_child.attrib.get("class") == "big_item":
                big_index += 1
                if big_index == 4:
                    break
                section_list.append([])
            elif div_child.attrib.get("class") == "question_list":
                title_no += 1
                question_list_block = doc(div_child)
                question_list = question_list_block.text().strip()
                u_tag = question_list_block("u")
                if u_tag:
                    u_text = u_tag.text().strip()
                    # search_word_list[big_index - 1].append(u_text)
                    question_list = question_list.replace(
                        f"\n{u_text}\n", f"<u>{u_text}</u>"
                    )
                pivot = 1 if title_no < 10 else 2
                question_no = question_list[:pivot]
                question_list = (
                    "**【"
                    + question_no
                    + "】** "
                    + question_list[pivot:].strip().lstrip(".").strip()
                )
                section_list[big_index - 1].append([question_list])
            elif div_child.attrib.get("class").startswith("answer"):
                four_answers = list(doc(div_child)("div[class='answers']").items())
                answer_text = ""
                for answer in four_answers:
                    choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                    answer_text += "> " + choice_text + "  \n"
                section_list[big_index - 1][-1].append(answer_text[:-1])
        for index in range(3):
            info_list[index] += f"## {year_month}\n\n"
            for _text in section_list[index]:
                for text in _text:
                    info_list[index] += f"{text}\n\n"
    for index in range(3):
        with open(
            f"{filename_list[index]}.md", "w+", encoding="utf-8", newline="\n"
        ) as f:
            f.writelines(info_list[index])
        # print(f"index: {index}, search_word_list: {search_word_list[index]}")


def extract_jlpt_N1_reading_type1(year_month_list):
    info_list = "# JLPT N1 短文内容理解\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="3")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Reading (Type 1) ...")

        result = [[] for _ in range(4)]
        question_text_block = doc("div[class='question_content']")
        for number, question in enumerate(list(question_text_block.items())[0:4]):
            question_text = question.text().strip()
            result[number].append(question_text)

        question_block = doc("div[class='question_list']")
        for number, question in enumerate(list(question_block.items())[0:4]):
            question_text = question.text().strip()
            question_no = question_text[0:2]
            question_text = "**【" + question_no + "】** " + question_text[3:].strip()
            result[number].append(question_text)

        answer_block = doc("div[class='answers']")
        four_answers = list(answer_block.items())[0 : 0 + 4 * 4]
        for number in range(4):
            answer_text = ""
            for answer in four_answers[number * 4 : number * 4 + 4]:
                choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                answer_text += "> " + choice_text + "  \n"
            result[number].append(answer_text)

        info_list += f"## {year_month}\n\n"
        for question_text, question, answer in result:
            info_list += f"{question_text}\n\n{question}\n\n{answer}\n"

    with open("jlpt_N1_reading_type1.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def extract_jlpt_N1_reading_type2(year_month_list):
    info_list = "# JLPT N1 中文内容理解\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="3")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Reading (Type 2) ...")

        result = [[] for _ in range(3)]
        question_text_block = doc("div[class='question_content']")
        for number, question in enumerate(list(question_text_block.items())[4:7]):
            question_text = question.text().strip()
            u_tag = list(doc(question)("u").items())
            if u_tag:
                for _u_tag in u_tag:
                    u_text = _u_tag.text().strip()
                    question_text = question_text.replace(
                        f"\n{u_text}\n", f"<u>{u_text}</u>"
                    )
            result[number].append(question_text)

        question_block = list(doc("div[class='question_list']"))[4 : 4 + 3 * 3]
        for number in range(3):
            result[number].append([])
            for section in question_block[number * 3 : number * 3 + 3]:
                question_text = doc(section).text().strip()
                u_tag = doc(section)("u")

                u_text = ""
                if u_tag:
                    u_text = u_tag.text().strip()
                    question_text = question_text.replace(
                        f"\n{u_text}\n", f"<u>{u_text}</u>"
                    )

                question_no = question_text[0:2]
                question_text = (
                    "**【" + question_no + "】** " + question_text[3:].strip()
                )
                result[number][1].append(question_text)

        answer_block = doc("div[class='answers']")
        four_answers = list(answer_block.items())[16 : 16 + 3 * 3 * 4]
        for number in range(3):
            result[number].append([])
            for idx in range(3):
                answer_text = ""
                for answer in four_answers[
                    number * 3 * 4 + idx * 4 : number * 3 * 4 + idx * 4 + 4
                ]:
                    choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text().strip())
                    answer_text += "> " + choice_text + "  \n"
                result[number][2].append(answer_text)

        info_list += f"## {year_month}\n\n"

        for question_text, question_list, answer_list in result:
            info_list += f"{question_text}\n\n"
            for question, answer in zip(question_list, answer_list):
                info_list += f"{question}\n\n{answer}\n"

    with open("jlpt_N1_reading_type2.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def extract_jlpt_N1_listening(year_month_list):
    info_list = "# JLPT N1 Listening\n\n"

    for year_month in year_month_list:
        url = BASE_URL.format(level="N1", year_month=year_month, part="4")
        response = requests.get(url)
        if response.status_code != 200 or "問題" not in response.text:
            continue
        # with open(f"tmp/{year_month}.html", "w+", encoding="utf-8", newline="\n") as f:
        #     f.write(response.text)
        print(url)

        doc = pq(response.text)

        print(f"Extracting {year_month} N1 Listening ...")

        year_month = year_month[:4] + "." + year_month[4:]
        info_list = [f"# {year_month} N1 听力原文\n\n"]
        big_index = 0
        form = doc("form[name='dttn']")
        for div_child in form.children():
            if div_child.tag != "div":
                continue
            if div_child.attrib.get("class") == "big_item":
                big_index += 1
                info_list.append(f"## 問題{big_index}\n\n")
            elif div_child.attrib.get("class") == "question_list":
                bango = div_child.text.strip()
                info_list.append(f"**{bango}**\n\n")
            elif div_child.attrib.get("id", "").startswith("GT"):
                refer = (
                    pq(div_child)
                    .text()
                    .strip()
                    .replace("\n\n", "\n")
                    .replace("\n", "  \n")
                )
                if refer.startswith("Reference: "):
                    refer = refer[11:]
                info_list.append(f"{refer}\n\n")
            else:
                answers = pq(div_child)("label > div")
                if not answers:
                    continue
                if big_index == 3 or big_index == 4:
                    continue
                for answer in answers:
                    if not answer.text:
                        continue
                    choice_text = re.sub(r"\d\)", "`\g<0>`", answer.text.strip())
                    info_list.append(f"> {choice_text}\n")
                info_list.append("\n")
        with open(f"tmp/{year_month}.md", "w+", encoding="utf-8", newline="\n") as f:
            f.writelines(info_list)


def get_tuhocjlpt(url):
    response = requests.get(url)
    if response.status_code != 200:
        return
    doc = pq(response.text)

    question_block = doc("h4")
    question_list = []
    for question in question_block.items():
        question_text = question.text()[3:].strip()
        question_text = question_text.replace("\n", "<u>", 1).replace("\n", "</u>", 1)
        question_list.append(question_text)

    answer_block = doc("div[class='i-checks']")
    answer_list = []
    for answer in answer_block.items():
        answer_text = answer.text().strip()
        answer_list.append(answer_text)

    info_list = []
    for idx in range(len(question_list)):
        bango = 41 + idx
        question = question_list[idx]
        answer_choices = answer_list[idx * 4 : idx * 4 + 4]
        info_list.append(f"**【{bango}】** {question}\n\n")
        for choice_idx, choice in enumerate(answer_choices):
            choice = choice.replace("\n", "<u>", 1).replace("\n", "</u>", 1)
            choice_text = f"> `{choice_idx+1})` {choice}  \n"
            info_list.append(choice_text)
        info_list.append("\n")
    with open("tuhocjlpt.md", "w+", encoding="utf-8", newline="\n") as f:
        f.writelines(info_list)


def get_u_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    text_dict = {}
    title = ""
    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip()
        elif line.startswith("**"):
            question_no = line[3:5].rstrip("】")
            utext = re.search(r"<u>(.*?)</u>", line)
            if utext:
                text_dict[title + "_" + question_no] = utext.group(1)
    return text_dict


def get_choice_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    text_dict = {}
    title = ""
    question_no = ""
    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip()
        elif line.startswith("**"):
            question_no = line[3:5].rstrip("】")
        elif line.startswith(">"):
            choice_text = re.search(r"`(\d)\)` (.*?)  ", line)
            if choice_text:
                if title + "_" + question_no not in text_dict:
                    text_dict[title + "_" + question_no] = []
                text_dict[title + "_" + question_no].append(choice_text.group(2))
    return text_dict


if __name__ == "__main__":
    year_month_list = []
    for year in range(2024, 2025):
        for month in ["07", "12"]:
            year_month = str(year) + month
            year_month_list.append(year_month)

    # extract_jlpt_N1_vocab_1to3(year_month_list)
    # extract_jlpt_N1_vocab_type4(year_month_list)
    # extract_jlpt_N1_grammar_type4(year_month_list)
    # extract_jlpt_N1_grammar_type5(year_month_list)
    # extract_jlpt_N1_grammar_type6(year_month_list)

    # extract_jlpt_N1_reading_type1(year_month_list)
    # extract_jlpt_N1_reading(year_month_list)

    # extract_jlpt_vocabulary(year_month_list)

    # print(get_choice_text("/home/ubuntu/work/practice/jlpt-review/JLPT.N1.漢字読み.md"))

    extract_jlpt_N1_listening(year_month_list)

    # get_tuhocjlpt("https://www.tuhocjlpt.com/test/1862")
