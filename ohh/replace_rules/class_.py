import os
from ohh.easy import BUILD_DIRECTORY, StandardPatterns, StandardSearchResult
from ohh.replace_rules.utils.replace import replace_in_file
from ohh.replace_rules.utils.search import search_in_data

def search(file_path: str, patterns: StandardPatterns) -> StandardSearchResult:
    with open(file_path, 'rb') as file:
        result = search_in_data(file.read(), [bytes(e, encoding='utf-8') for e in patterns])
    if not result:
        return result
    else:
        standard_list = []
        for pattern, start_pos in result.items():
            end_pos = start_pos + len(pattern)
            standard_list.append((start_pos, end_pos, pattern.decode()))
        return standard_list

def replace(file_path: str, replacements: StandardSearchResult):
    replace_in_file(file_path, replacements)
    for start_pos, end_pos, str_ in replacements:
        old_target_len = end_pos - start_pos
        new_target_len = len(bytes(str_, encoding='utf-8'))
        with open(os.path.join(BUILD_DIRECTORY, file_path), 'rb') as file:
            bytes_ = bytearray(file.read())
            old_source_len = int.from_bytes(bytes_[start_pos - 2: start_pos])
            # 这样写是为了支持不完全替换，例如 `abc` 仅替换 `ab` 到 `cd` ，那么我们会得到 `cdc`
            # 但是目前来说，我们必须提供正确的起始位置
            new_source_len = old_source_len + (new_target_len - old_target_len)
            bytes_[start_pos - 2: start_pos] = new_source_len.to_bytes().rjust(2, b'\x00')
        with open(os.path.join(BUILD_DIRECTORY, file_path), "wb") as file:
            file.write(bytes_)