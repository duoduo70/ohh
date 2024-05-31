from typing import List

import os
import ohh.replace_rules as rules

BUILD_DIRECTORY = 'build'
TEMP_DIRECTORY = 'temp'

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
StandardSearchResult = List[tuple[int, int, str]]
StandardPatterns = List[str]

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
        Example: for_dir("a/b/c").skip("a.json")
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
            if os.path.splitext(filepath)[1] in rules.auto_extract_source:
                source[filepath] = rules.auto_extract_source[os.path.splitext(filepath)[1]](filepath, search_type)
        return source
    def search(self, patterns: StandardPatterns):
        ret = []
        for filepath in self.includingfiles:
            if os.path.splitext(filepath)[1] in rules.search:
                result = rules.search[os.path.splitext(filepath)[1]](filepath, patterns)
                if result == []:
                    pass
                else:
                    ret.append((filepath, result))
        return ret
    from_ = str | bytes
    to = str | bytes
    def replace(self, patterns: List[tuple[from_, to]]):
        for filepath, result in self.search([e for e, _ in patterns]):
            if os.path.splitext(filepath)[1] in rules.search:
                will_replace_patterns = []
                for search_ret_pattern in result:
                    for pattern in patterns:
                        if search_ret_pattern[2] == pattern[0]:
                            will_replace_patterns.append((search_ret_pattern[0], search_ret_pattern[1], pattern[1]))
                rules.replace[os.path.splitext(filepath)[1]](filepath, will_replace_patterns)
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
    def replace(self, patterns: List[tuple[from_, to]]):
        standard_pattern = []
        if (os.path.splitext(self.filepath)[1] in rules.replace) and (os.path.splitext(self.filepath)[1] in rules.search):
            result = rules.search[os.path.splitext(self.filepath)[1]](self.filepath, [e for e, _ in patterns])
            for start_pos, end_pos, str_ in result:
                for from_, to in patterns:
                    if str_ == from_:
                        standard_pattern.append((start_pos, end_pos, to))
            rules.replace[os.path.splitext(self.filepath)[1]](self.filepath, standard_pattern)
        return self
    def copy_to(self, to_path: str):
        import shutil
        if not os.path.exists(os.path.dirname(to_path)):
            os.makedirs(os.path.dirname(to_path))
        shutil.copy(self.filepath, to_path)
    possibility = int
    def auto_extract_source(self, search_type = AutoExtractSearchType.NORMAL) -> List[tuple[str, possibility]]:
        source = dict()
        if os.path.splitext(self.filepath)[1] in rules.auto_extract_source:
            source[self.filepath] = rules.auto_extract_source[os.path.splitext(self.filepath)[1]](self.filepath, search_type)
        return source
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