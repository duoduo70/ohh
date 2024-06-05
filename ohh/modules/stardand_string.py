from typing import List
from ohh.easy import AutoExtractSearchType, ReplaceRule, SearchPattern, SearchResult
from ohh.modules.replace import replace_in_file
from ohh.modules.search import search_in_data

possibility = int
def auto_extract_source(filename: str, search_type = AutoExtractSearchType.NORMAL) -> List[dict[str, possibility]]:
    with open(filename) as file:
        lines = file.readlines()
    ret = dict()
    for line in lines:
        str_flag = False
        str_start_pos = None
        str_end_pos = None
        for ch_num in range(0, len(line)):
            if line[ch_num] == "\"":
                if str_flag == False:
                    str_start_pos = ch_num + 1
                    str_flag = True
                else:
                    str_end_pos = ch_num
                    str_flag = False
            ch_num += 1
        if str_end_pos != None:
            possibility = 1
            CAPITALIZE_FIRST_LETTER = 3
            UNDERLINE = -2
            SPACE = 2
            LIKE_PATH = -2
            UPPER_CAMEL_LIKE = -2
            DOT = -2
            COMMA = 2
            str_ = line[str_start_pos:str_end_pos]
            if len(str_) != 0:
                if str_[0].isupper():
                    possibility += CAPITALIZE_FIRST_LETTER
                if search_type == AutoExtractSearchType.SEGMENT:
                    lower_flag = False
                    for ch in str_:
                        if ch == '_':
                            possibility += UNDERLINE
                        if ch == ' ':
                            possibility += SPACE
                        if ch == '/':
                            possibility += LIKE_PATH
                        if ch == '.':
                            possibility += DOT
                        if ch == ',':
                            possibility += COMMA
                        if ch.islower():
                            lower_flag = True
                        if ch.isupper() and lower_flag == True:
                            possibility += UPPER_CAMEL_LIKE
                        lower_flag = False
                if len(str_) <= 2:
                    possibility = 1 # too short
                ret[str_] = possibility
    return ret

def search(file_path: str, patterns: List[SearchPattern]) -> List[SearchResult]:
    with open(file_path, 'rb') as file:
        result = search_in_data(file.read(), [bytes(e.pattern_str, encoding='utf-8') for e in patterns])
    if not result:
        return result
    else:
        search_result_list = []
        for matched_pattern_str, start_pos_list in result.items():
            for start_pos in start_pos_list:
                end_pos = start_pos + len(matched_pattern_str)
                result = SearchResult()
                result.start_pos = start_pos
                result.end_pos = end_pos
                result.matched_pattern_str = matched_pattern_str.decode()
                search_result_list.append(result)
        return search_result_list

def replace(file_path: str, replacements: List[ReplaceRule], dont_move = False):
    search_patterns = []
    simply_replacements = {e.from_ : e.to for e in replacements}
    for from_ in simply_replacements.keys():
        pattern = SearchPattern(from_)
        search_patterns.append(pattern)
    search_result = search(file_path, search_patterns)

    replace_rules = []
    for item in search_result:
        replace_rules.append((item.start_pos, item.end_pos, simply_replacements[item.matched_pattern_str]))
    replace_in_file(file_path, replace_rules, dont_move)