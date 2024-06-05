import os
from typing import List, Optional
from ohh.easy import BUILD_DIRECTORY, AutoExtractSearchType, ReplaceRule, SearchPattern, SearchResult

class Utf8:
    str_ = str
    def __init__(self, str_: str):
        self.str_ = str_

class Integer:
    int_ = int


class Float:
    bytes_ = bytes


class Long:
    bytes_ = bytes


class Double:
    bytes_ = bytes


class Class:
    index = int


class String:
    index = int


class Fieldref:
    Class_index: int
    NameAndType_index: int


class Methodref:
    Class_index: int
    NameAndType_index: int


class InterfaceMethodref:
    Class_index: int
    NameAndType_index: int


class NameAndType:
    name_index: int
    type_index: int


class MethodHandle:
    refrence_kind: int
    refrence_index: int


class MethodType:
    descriptor_index: int


class Dynamic:
    bootstrap_method_attr_index: int
    NameAndType_index: int


class InvokeDynamic:
    bootstrap_method_attr_index: int
    NameAndType_index: int


class Module:
    name_index: int


class Package:
    name_index: int


constant = (
    Utf8
    | Integer
    | Float
    | Long
    | Double
    | Class
    | String
    | Fieldref
    | Methodref
    | InterfaceMethodref
    | NameAndType
    | MethodHandle
    | MethodType
    | Dynamic
    | InvokeDynamic
    | Module
    | Package
)

def parse(filepath: str):
    with open(filepath, "rb") as file:
        bytes_ = file.read()
    if bytes_[0:4] != b"\xca\xfe\xba\xbe":
        raise Exception("It is not class bytes file")
    classfile = ClassFile()
    classfile.minor_version = int.from_bytes(bytes_[4:6])
    classfile.major_version = int.from_bytes(bytes_[6:8])
    classfile.constant_pool = []

    constant_pool_count = int.from_bytes(bytes_[8:10]) - 1
    i = 10
    while constant_pool_count != 0:
        if bytes_[i] == 1:
            length = int.from_bytes(bytes_[i + 1 : i + 3])
            i += 3
            content = Utf8(str(bytes_[i : i + length], encoding="utf-8"))
            classfile.constant_pool.append(content)
            i += length
            constant_pool_count -= 1
            continue
        if bytes_[i] == 3:
            content = Integer()
            content.int_ = int.from_bytes(bytes_[i + 1 : i + 5])
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 4:
            content = Float()
            content.bytes_ = bytes_[i + 1 : i + 5]
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 5:
            content = Long()
            content.bytes_ = bytes_[i + 1 : i + 9]
            classfile.constant_pool.append(content)
            i += 9
            constant_pool_count -= 1
            continue
        if bytes_[i] == 6:
            content = Double()
            content.bytes_ = bytes_[i + 1 : i + 9]
            classfile.constant_pool.append(content)
            i += 9
            constant_pool_count -= 1
            continue
        if bytes_[i] == 7:
            content = Class()
            content.index = int.from_bytes(bytes_[i + 1 : i + 3])
            classfile.constant_pool.append(content)
            i += 3
            constant_pool_count -= 1
            continue
        if bytes_[i] == 8:
            content = String()
            content.index = int.from_bytes(bytes_[i + 1 : i + 3])
            classfile.constant_pool.append(content)
            i += 3
            constant_pool_count -= 1
            continue
        if bytes_[i] == 9:
            content = Fieldref()
            content.Class_index = int.from_bytes(bytes_[i + 1 : i + 3])
            content.NameAndType_index = int.from_bytes(bytes_[i + 3 : i + 5])
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 10:
            content = Methodref()
            content.Class_index = int.from_bytes(bytes_[i + 1 : i + 3])
            content.NameAndType_index = int.from_bytes(bytes_[i + 3 : i + 5])
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 11:
            content = InterfaceMethodref()
            content.Class_index = int.from_bytes(bytes_[i + 1 : i + 3])
            content.NameAndType_index = int.from_bytes(bytes_[i + 3 : i + 5])
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 12:
            content = NameAndType()
            content.name_index = int.from_bytes(bytes_[i + 1 : i + 3])
            content.type_index = int.from_bytes(bytes_[i + 3 : i + 5])
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 15:
            content = MethodHandle()
            content.refrence_kind = bytes_[i + 1]
            content.refrence_index = int.from_bytes(bytes_[i + 2 : i + 4])
            classfile.constant_pool.append(content)
            i += 4
            constant_pool_count -= 1
            continue
        if bytes_[i] == 16:
            content = MethodType()
            content.descriptor_index = int.from_bytes(bytes_[i + 1 : i + 3])
            classfile.constant_pool.append(content)
            i += 3
            constant_pool_count -= 1
            continue
        if bytes_[i] == 17:
            content = Dynamic()
            content.bootstrap_method_attr_index = int.from_bytes(bytes_[i + 1 : i + 3])
            content.NameAndType_index = int.from_bytes(bytes_[i + 3 : i + 5])
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 18:
            content = InvokeDynamic()
            content.bootstrap_method_attr_index = int.from_bytes(bytes_[i + 1 : i + 3])
            content.NameAndType_index = int.from_bytes(bytes_[i + 3 : i + 5])
            classfile.constant_pool.append(content)
            i += 5
            constant_pool_count -= 1
            continue
        if bytes_[i] == 19:
            content = Module()
            content.name_index = int.from_bytes(bytes_[i + 1 : i + 3])
            classfile.constant_pool.append(content)
            i += 3
            constant_pool_count -= 1
            continue
        if bytes_[i] == 20:
            content = Package()
            content.name_index = int.from_bytes(bytes_[i + 1 : i + 3])
            classfile.constant_pool.append(content)
            i += 3
            constant_pool_count -= 1
            continue
        break # 有些编译器自己的问题，常量池声明的比用的多，主流 JRE 也都能解析这种严格意义上来说损坏了的字节码
    classfile.access_flags = bytes_[i:i+2]
    classfile.this_class = int.from_bytes(bytes_[i+2:i+4])
    classfile.super_class = int.from_bytes(bytes_[i+4:i+6])

    classfile.interfaces = []
    interfaces_count = int.from_bytes(bytes_[i+6:i+8])
    i+=8
    while interfaces_count != 0:
        classfile.interfaces.append(int.from_bytes(bytes_[i:i+2]))
        i+=2
        interfaces_count-=1
    classfile.others = bytes_[i:]
    return classfile

class ClassFile:
    major_version: int  # JDK 1.0 is 44, 1.1 is 45, 1.2 is 46 ...
    minor_version: int
    constant_pool: List[constant]
    access_flags: bytes
    this_class: int
    super_class: int
    interfaces: List[int]
    others: bytes 

    def build_to(self, filepath: str):
        bytes_ = bytearray(b"\xca\xfe\xba\xbe")
        bytes_.extend(self.minor_version.to_bytes(length=2))
        bytes_.extend(self.major_version.to_bytes(length=2))
        bytes_.extend((len(self.constant_pool) + 1).to_bytes(length=2))
        for constant in self.constant_pool:
            constant_type = type(constant)
            print(constant_type)
            if constant_type == Utf8:
                bytes_.extend((1).to_bytes())
                bytes_.extend(len(constant.str_).to_bytes(length=2))
                bytes_.extend(constant.str_.encode('utf-8'))
                continue
            if constant_type == Integer:
                bytes_.extend((3).to_bytes())
                bytes_.extend(constant.int_)
                continue
            if constant_type == Float:
                bytes_.extend((4).to_bytes())
                bytes_.extend(constant.bytes_)
                continue
            if constant_type == Long:
                bytes_.extend((5).to_bytes())
                bytes_.extend(constant.bytes_)
                continue
            if constant_type == Double:
                bytes_.extend((6).to_bytes())
                bytes_.extend(constant.bytes_)
                continue
            if constant_type == Class:
                bytes_.extend((7).to_bytes())
                bytes_.extend(constant.index.to_bytes(length=2))
                continue
            if constant_type == String:
                bytes_.extend((8).to_bytes())
                bytes_.extend(constant.index.to_bytes(length=2))
                continue
            if constant_type == Fieldref:
                bytes_.extend((9).to_bytes())
                bytes_.extend(constant.Class_index.to_bytes(length=2))
                bytes_.extend(constant.NameAndType_index.to_bytes(length=2))
                continue
            if constant_type == Methodref:
                bytes_.extend((10).to_bytes())
                bytes_.extend(constant.Class_index.to_bytes(length=2))
                bytes_.extend(constant.NameAndType_index.to_bytes(length=2))
                continue
            if constant_type == InterfaceMethodref:
                bytes_.extend((11).to_bytes())
                bytes_.extend(constant.Class_index.to_bytes(length=2))
                bytes_.extend(constant.NameAndType_index.to_bytes(length=2))
                continue
            if constant_type == NameAndType:
                bytes_.extend((12).to_bytes())
                bytes_.extend(constant.name_index.to_bytes(length=2))
                bytes_.extend(constant.type_index.to_bytes(length=2))
                continue
            if constant_type == MethodHandle:
                bytes_.extend((15).to_bytes())
                bytes_.extend(constant.refrence_kind.to_bytes(length=2))
                bytes_.extend(constant.refrence_index.to_bytes(length=2))
                continue
            if constant_type == MethodType:
                bytes_.extend((16).to_bytes())
                bytes_.extend(constant.descriptor_index.to_bytes(length=2))
                continue
            if constant_type == Dynamic:
                bytes_.extend((17).to_bytes())
                bytes_.extend(constant.bootstrap_method_attr_index.to_bytes(length=2))
                bytes_.extend(constant.NameAndType_index.to_bytes(length=2))
                continue
            if constant_type == InvokeDynamic:
                bytes_.extend((18).to_bytes())
                bytes_.extend(constant.bootstrap_method_attr_index.to_bytes(length=2))
                bytes_.extend(constant.NameAndType_index.to_bytes(length=2))
                continue
            if constant_type == Module:
                bytes_.extend((19).to_bytes())
                bytes_.extend(constant.name_index.to_bytes(length=2))
                continue
            if constant_type == Module:
                bytes_.extend((20).to_bytes())
                bytes_.extend(constant.name_index.to_bytes(length=2))
                continue
        bytes_.extend(self.access_flags)
        bytes_.extend(self.this_class.to_bytes(length=2))
        bytes_.extend(self.super_class.to_bytes(length=2))
        bytes_.extend(len(self.interfaces).to_bytes(length=2))
        for e in self.interfaces:
            bytes_.extend(e.to_bytes(length=2))
        bytes_.extend(self.others)

        import os
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, "wb") as file:
            file.write(bytes_)

possibility = int
def auto_extract_source(filename: str, search_type = AutoExtractSearchType.NORMAL) -> List[dict[str, possibility]]:
    parsed_byte_code = parse(filename)
    return {e: 1 for e in get_literal_strings(parsed_byte_code.constant_pool).keys()}

def search(file_path: str, patterns: List[SearchPattern]) -> List[SearchResult]:
    parsed_byte_code = parse(file_path)
    pattern_strs = [pattern.pattern_str for pattern in patterns]
    strs_dict = get_literal_strings(parsed_byte_code.constant_pool)
    result_list = []
    for key in pattern_strs:
        if key in strs_dict:
            result = SearchResult()
            result.matched_pattern_str = key
            result.index = strs_dict[key]
            result_list.append(result)
        else:
            pass
    return result_list

def get_formatted_literal_strings_map(filename: str):
    import json
    return json.dumps(get_literal_strings(parse(filename).constant_pool), indent=4)

def get_literal_strings(constant_pool) -> dict[str, int]:
    literal_strings = dict()
    for index, constant in enumerate(constant_pool):
        if is_literal_string(constant_pool, index):
            literal_strings[constant.str_] = index
        else:
            pass
    return literal_strings

def is_literal_string(constant_pool, index) -> bool:
    if type(constant_pool[index - 1]) == String and type(constant_pool[index]) == Utf8:
        return True
    else:
        return False

def replace(file_path: str, replacements: List[ReplaceRule], dont_move = False):
    parsed_byte_code = parse(file_path)
    for index, constant in enumerate(parsed_byte_code.constant_pool):
        if is_literal_string(parsed_byte_code.constant_pool, index):
            parsed_byte_code.constant_pool[index] = replaced_item(constant, replacements, parsed_byte_code.constant_pool[index - 1].index)

    if dont_move:
        parsed_byte_code.build_to(file_path)
    else:
        parsed_byte_code.build_to(os.path.join(BUILD_DIRECTORY, file_path))

def replaced_item(constant: Utf8, rules: List[ReplaceRule], index: Optional[int]) -> Utf8:
    for rule in rules:
        if hasattr(rule, "index"):
            if rule.index == index and constant.str_ == rule.from_:
                return Utf8(rule.to)
            else:
                return constant
        else:
            if constant.str_ == rule.from_:
                return Utf8(rule.to)
            else:
                return constant