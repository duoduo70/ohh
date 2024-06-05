from typing import List, Optional

import os
import ohh.modules as modules

BUILD_DIRECTORY = 'build'
TEMP_DIRECTORY = 'build/.temp'

def set_build_dir(dirname: str):
    global BUILD_DIRECTORY
    BUILD_DIRECTORY = dirname
def set_temp_dir(dirname: str):
    global TEMP_DIRECTORY
    TEMP_DIRECTORY = dirname

class AutoExtractSearchType:
    FAST = 0
    NORMAL = 1
    SEGMENT = 2

start_pos = int
end_pos = int

class SearchPattern:
    pattern_str: str
    def __init__(self, pattern_str: str):
        self.pattern_str = pattern_str

class ReplaceRule:
    from_: str
    to: str
    def __init__(self, arg1: str, to: Optional[str] = None):
        if type(arg1) == tuple:
            self.from_ = arg1[0]
            self.to = arg1[1]
            return
        else:
            self.from_ = arg1
            self.to = to

class SearchResult:
    start_pos: Optional[str]
    end_pos: Optional[str]
    matched_pattern_str: str
    def __repr__(self):
        return str(self.__dict__)

class Directory:
    '''
    该类成员可额外动态注入，而无需在此声明。
    在此声明的成员不必要全部实例化。
    若 dirname 为 "a/b"
    则 filenames 类似 ["a/b/c.txt"]
    '''
    dirpath: str
    includingfiles: List[str]
    skippedfiles: List[str]
    def skip(self, path: str):
        '''
        Example: for_dir("a/b/c").skip("a.json").auto_extract_source()
        则跳过 a/b/c/a.json
        '''
        self.includingfiles = [e for e in self.includingfiles
                               if e[:len(self.dirpath)+len(path) + 1] != os.path.join(self.dirpath, path)]
        self.skippedfiles.append(path)
        return self
    def for_subdir(self, dirname: str):
        self.includingfiles = [e for e in self.includingfiles 
                               if e[len(self.dirpath) + 1:len(self.dirpath)+len(dirname) + 1] == dirname]
        self.dirpath = os.path.join(self.dirpath, dirname)
        return self
    filename = str
    possibility = int
    def auto_extract_source(self, search_type = AutoExtractSearchType.NORMAL) -> dict[filename, List[tuple[str, possibility]]]:
        source = dict()
        for filepath in self.includingfiles:
            if os.path.splitext(filepath)[1] in modules.AUTO_EXTRACT_SOURCE:
                source[filepath] = modules.AUTO_EXTRACT_SOURCE[os.path.splitext(filepath)[1]](filepath, search_type)
        return source
    def search(self, *patterns: List[str | SearchPattern] | str | SearchPattern):
        patterns = _preprocessing_patterns(str, SearchPattern, patterns)
        ret = []
        for filepath in self.includingfiles:
            if os.path.splitext(filepath)[1] in modules.SEARCH:
                result = modules.SEARCH[os.path.splitext(filepath)[1]](filepath, patterns)
                if result == []:
                    pass
                else:
                    ret.append((filepath, result))
            else:
                pass
        return ret
    def replace(self, *patterns: List[tuple[str, str] | ReplaceRule] | tuple[str, str] | ReplaceRule):
        patterns = _preprocessing_patterns(tuple, ReplaceRule, patterns)
        for filepath in self.includingfiles:
            if os.path.splitext(filepath)[1] in modules.REPLACE:
                modules.REPLACE[os.path.splitext(filepath)[1]](filepath, patterns)
            else:
                pass
        return self
    def copy_into(self, to_path: str):
        import shutil
        if not os.path.exists(to_path):
            os.makedirs(os.path.dirname(to_path))
        shutil.copytree(self.dirpath, to_path)
    def zip_files(self, output_path):
        import zipfile
        import shutil
        for file in self.skippedfiles:
            os.remove(file)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.dirpath):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), self.dirpath))
        shutil.rmtree(self.dirpath)
        file = File()
        file.filepath = output_path
        return file
    def create(self):
        os.makedirs(self.dirpath)
        return self
    def get_fileobjs(self) -> List: # ret: List[File]
        return [for_file(file) for file in self.includingfiles]
    def segment_dump(self, min_possibility=2):
        result = self.auto_extract_source(AutoExtractSearchType.SEGMENT)
        print("[")
        for filename, data in result.items():
            for str_, p in data:
                if p >= min_possibility:
                    print("    ", end="")
                    print((str_, filename), end="")
                    print(",")
        print("]")

def for_dir(dirpath: str) -> Directory:
    import os
    file_list = []
    for root, directories, files in os.walk(dirpath):
        for filename in files:
            file_list.append(os.path.join(root, filename))
    dir = Directory()
    dir.includingfiles = file_list
    dir.dirpath = dirpath
    return dir

class File:
    filepath: str
    def unzip(self):
        import zipfile
        with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(TEMP_DIRECTORY, self.filepath))
        self.adjoint_dir_info = for_dir(os.path.join(TEMP_DIRECTORY, self.filepath))
        return self
    def remove_source_file(self):
        os.remove(self.filepath)
        return self
    def as_dir(self) -> Directory:
        dir = self.adjoint_dir_info
        return dir
    from_ = str
    to = str
    def replace(self, *patterns: List[tuple[str, str] | ReplaceRule] | tuple[str, str] | ReplaceRule):
        patterns = _preprocessing_patterns(tuple, ReplaceRule, patterns)
        if os.path.splitext(self.filepath)[1] in modules.REPLACE:
            modules.REPLACE[os.path.splitext(self.filepath)[1]](self.filepath, patterns)
        else:
            raise Exception("The file do not have replace support")
        return self
    def copy_to(self, to_path: str):
        import shutil
        if not os.path.exists(os.path.dirname(to_path)):
            os.makedirs(os.path.dirname(to_path))
        shutil.copy(self.filepath, to_path)
    possibility = int
    def auto_extract_source(self, search_type = AutoExtractSearchType.NORMAL) -> List[tuple[str, possibility]]:
        if os.path.splitext(self.filepath)[1] in modules.AUTO_EXTRACT_SOURCE:
            return modules.AUTO_EXTRACT_SOURCE[os.path.splitext(self.filepath)[1]](self.filepath, search_type)
        else:
            return []
    def replace_with(self, filepath: str):
        import shutil
        os.remove(self.filepath)
        shutil.copy(filepath, self.filepath)
        return self
    def write(self, context: str | bytes):
        if isinstance(context, str):
            opentype = 'w'
        else:
            opentype = 'wb'
        with open(self.filepath, opentype) as file:
            file.write(context)
    def search(self, *patterns: List[str | SearchPattern] | str | SearchPattern):
        patterns = _preprocessing_patterns(str, SearchPattern, patterns)
        ret = []
        if os.path.splitext(self.filepath)[1] in modules.SEARCH:
            result = modules.SEARCH[os.path.splitext(self.filepath)[1]](self.filepath, patterns)
            if result == []:
                return []
            else:
                return result
        else:
            raise Exception("The file do not have search support")

def for_file(filepath) -> File:
    file = File()
    file.filepath = filepath
    return file

def clear_cache():
    import shutil
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)
    if os.path.exists(TEMP_DIRECTORY):
        shutil.rmtree(TEMP_DIRECTORY)

def is_rule_defined(rules_dict_name, rule) -> bool:
    if rule in rules_dict_name:
        return True
    else:
        return False

def _preprocessing_patterns(SimplyType, AdvancedType, *patterns):
    '''
        Example: replace 函数定义中的 _preprocessing_patterns(tuple, ReplaceRule, patterns)
        则以下参数等价：
        1. replace([ReplaceRule("1", "2")])
        2. replace([("1", "2")])
        3. replace(ReplaceRule(("1", "2")))
        4. replace(("1", "2"))
        5. replace("1", "2")
        6. replace(ReplaceRule("1", "2"))
        你必须为 ReplaceRule 手动定义形如 ReplaceRule(("1", "2")) 和 ReplaceRule("1", "2") 的构造

        该函数返回 List[AdvancedType] ，例如在示例中，返回 List[ReplaceRule]
    '''
    if len(patterns) != 1 and type(patterns) != SimplyType:
        return [(patterns)]
    elif type(patterns[0]) == SimplyType:
        return [AdvancedType(patterns[0][0])]
    elif type(patterns[0]) == AdvancedType:
        return [patterns[0]]
    else:
        ret_list = []
        for p in patterns[0]:
            if type(p) == SimplyType:
                ret_list.append(AdvancedType(p))
            else:
                ret_list.append(p)
        return ret_list