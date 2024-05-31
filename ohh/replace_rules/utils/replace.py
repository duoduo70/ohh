from typing import List
import os

from ohh.easy import BUILD_DIRECTORY

def replace_in_file(file_path: str, replacements: List[tuple[int, int, bytes | str]]):
    # 读取原始文件内容
    with open(file_path, 'rb') as file:
        content = file.read()

    # 将内容转换为可修改的 bytearray
    content = bytearray(content)

    # 计算偏移量
    offset_changes = []
    current_offset = 0
    for start, end, new_data in replacements:
        if isinstance(new_data, str):
            new_data = new_data.encode('utf-8')
        new_length = len(new_data)
        offset_change = new_length - (end - start)
        offset_changes.append((start + current_offset, end + current_offset, new_data))
        current_offset += offset_change

    # 应用替换
    for start, end, new_data in offset_changes:
        content[start:end] = new_data

    # 确保目标目录存在
    target_dir = os.path.join(BUILD_DIRECTORY, os.path.dirname(file_path))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 写入新文件
    with open(os.path.join(BUILD_DIRECTORY, file_path), 'wb') as targetfile:
        targetfile.write(content)