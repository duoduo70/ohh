import json
from typing import List
from ohh.easy import AutoExtractSearchType

possibility = int
def auto_extract_source(filename: str, search_type = AutoExtractSearchType.NORMAL) -> List[dict[str, possibility]]:
    NORMAL = 0
    CAPITALIZE_FIRST_LETTER = 1
    possibility_list = dict()
    with open(filename) as file:
        json_ = json.loads(file.read())
        for str_ in find_str_value(json_):
            if str_[0].isupper():
                possibility_list[str_] = CAPITALIZE_FIRST_LETTER
            elif search_type != AutoExtractSearchType.FAST:
                possibility_list[str_] = NORMAL
            else:
                pass
    if search_type == AutoExtractSearchType.SEGMENT:
        PUNCTUATION = 2
        LIKE_PATH = -1
        for str_ in possibility_list.keys():
            if len(str_) > 20:
                possibility_list[str_] += len(str_) // 20
            for ch in str_:
                if ch == ',' or ch == '.':
                    possibility_list[str_] += PUNCTUATION
                    break
                if ch == '/':
                    possibility_list[str_] += LIKE_PATH
    return possibility_list

def find_str_value(json_: json) -> List[str]:
    str_list = []
    if isinstance(json_, str):
        str_list.append(json_)
    elif isinstance(json_, dict):
        for _, value in json_.items():
            str_list.extend(find_str_value(value))
    elif isinstance(json_, list):
        for _, value in enumerate(json_):
            str_list.extend(find_str_value(value))
    return str_list