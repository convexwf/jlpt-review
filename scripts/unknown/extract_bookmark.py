# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : JLPT-review
# @FileName : scripts/unknown/extract_bookmark.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-12-21 10:41
# @UpdateTime : 2024-12-21 10:41

import json


def read_bookmark_file(file_path: str):
    with open(file_path, "r") as f:
        bookmark_list = json.load(f)["files"]

    bookmark_dict = {}
    for item in bookmark_list:
        file_path = item["path"]
        bookmarks = item["bookmarks"]

        bookmark_dict[file_path] = []
        for bookmark in bookmarks:
            bookmark_dict[file_path].append(bookmark["line"])
    return bookmark_dict


def preview_line(file_path: str, line_number_list: list):
    with open(file_path, "r") as f:
        lines = f.readlines()
    for line_number in line_number_list:
        print(lines[line_number])


def extract_grammar_practice(file_path: str, line_number_list: list):
    with open(file_path, "r") as f:
        lines = f.readlines()

    bango_list = []
    for line_number in line_number_list:
        bango = lines[line_number][1:].split("】")[0]
        bango_list.append(bango)
    print(bango_list)


def extract_jlpt_type(file_path: str, line_number_list: list):
    with open(file_path, "r") as f:
        lines = f.readlines()

    info_list = []
    year_month = ""
    for line_number, line in enumerate(lines):
        if line.startswith("##"):
            # info_list.append(line + "\n")
            year_month = line.split(" ")[1].strip()
            year_month = year_month[:4] + "." + year_month[4:]
            continue
        if line_number in line_number_list:
            end_line_number = line_number + 1
            while end_line_number < len(lines):
                if lines[end_line_number].startswith("##") or lines[
                    end_line_number
                ].startswith("*"):
                    break
                end_line_number += 1
            lines[line_number] = line.replace("**【", f"**【{year_month} @")
            info_list.extend(lines[line_number:end_line_number])

    with open("jlpt_type.md", "w") as f:
        f.writelines(info_list)


if __name__ == "__main__":
    bookmark_dict = read_bookmark_file(".vscode/bookmarks.json")
    print(bookmark_dict)

    # key = "resource/JLPT真题/文法/jlpt_N1_grammar_type4.md"
    # extract_jlpt_type(key, bookmark_dict[key])

    key = "resource/帝京语法练习题/语法练习题(gpt解析，有错误).md"
    extract_grammar_practice(key, bookmark_dict[key])

    # for file_path, line_number_list in bookmark_dict.items():
    #     print(file_path)
    #     preview_line(file_path, line_number_list)
    #     print()
    # ['3', '5', '7', '8', '14', '17', '18', '22', '24', '69', '74', '95', '107', '113', '119', '120', '306', '475', '486', '498', '499', '500']
