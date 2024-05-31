<img src='logo.png' align='right'/>

# OHH
This project helps you non-invasive localize those niche (but nice) projects.

This project allows you to do something on binary targets (instead of source code), which greatly simplifies the entry-level localization process. For example, you don't need to run the full compilation process for the target.

You can easily extend this project and append that to [this repository](github.com/duoduo70/ohh).

## How to use
You need a Python3 runtime. After that, just import `ohh` subdirectory as a python model.   
For Exmaple:
```python
from ohh import *

for_dir("test.txt").write("OHH")
```

You can publish your example and append that to this repository.

I will push most example after the first release version.

## Tiny Document

我设计了一套较为人性化的编程方法，让你用尽可能少的代码和尝试次数就能做到很多本地化的需求。  
你可以通过很简单的方法扩展该项目，通常来说，是把你的扩展塞进 `ohh/replace_rules` 目录，然后更改 `ohh/replace_rules/__init__.py`
我们先声明我们要对哪个文件或目录进行操作，然后将指定操作作用于它。  
这样，我们便可一目了然于对哪些文件或目录进行过操作。

我推荐你通过例子快速上手，如果你记性好，也可以看一遍这里的文档。但要注意，这里的文档并不全，请以实际代码为准。

```python
from ohh import *
for_file("test.txt").write("OHH") # 我们对一个未曾创建的文件进行写操作，这会让文件被自动创建
for_dir("test").create() # 这会创建一个目录
```

我们可以进行十分复杂的操作，有时候我们可以进行流式编程：
```python
for_dir("test").skip("a.txt") # 这会在接下来的操作中跳过 test/a.txt
.replace([
    ("a", "b"),
    ("c", "d") 
])
```
这会将 test 下除 a.txt 外的所有文件按 replace 处设置的模式进行文本替换

for_dir 函数会返回一个 Directory 对象，我们可以进行流式编程。
对于 for_dir ，流中有如下方法可用：
```python
skip("a.txt") # 在接下来的处理中跳过一个文件，只需设定一次
for_subdir("subtest") # 将我们要操作的目录切换到 for_dir 处设置的目录的子目录
replace([("a", "b"), ("c", "d")]) # 尝试按指定模式进行替换
zip_files("test.zip") # 将目录压缩，这会返回一个 File 对象
copy_into("abc") # 将目录中的所有文件复制到另一个目录，这会切断流
search(["a", "b", "c"]) # 尝试在目录中搜索设置的字符串以供本地化，这会切断流并返回一个结构体
auto_extract_source() # 尝试提取可本地化的项，这会切断流并返回一个结构体
create() # 将 for_dir 设置的目录创建
get_fileobjs() # 以列表形式返回所有文件的 File 对象，被跳过的除外
```

对于 for_file ，有如下方法：
```python
unzip() # 作为压缩包解压，仍返回原来的 file 对象
remove_source_file() # 删除 file 对象对应的文件
as_dir() # 配合 unzip() 使用，将其作为目录，返回 Directory 对象
replace([("a", "b"), ("c", "d")]) # 尝试按指定模式进行替换
copy_to("a.txt") # 将文件复制到设定的位置
auto_extract_source() # 尝试提取可本地化的项，这会切断流并返回一个结构体
replace_with("a.txt") # 用设定的文件替换 for_file 设定的文件
write("OHH") # 向文件中写一些内容，总是会覆盖而非追加
```

另外，我们有这些实用的附加函数：
```python
clear_cache() # 删除缓存目录，包括 `temp` 和 `build`
is_rule_defined(search, ".json") # 检查一个规则是否存在，返回一个 bool
set_build_dir(".build") # 更改默认的目标目录，例如这里从 `build` 改到 `.build`
set_temp_dir(".temp") # 更改默认的缓存目录，例如这里从 `temp` 改到 `.temp`

print_title("this is a title") # 输出一个标题
print_info("some info")
print_warning("a warning")
print_error("a error")

# 该函数会返回一个 bool ，如果输入 Y 则返回 True ，否则返回 False
print_check("Are you sure?") # 输出 `Are you sure? [Y/n]` 并等待确认
```

```python
from ohh import *

def debug():
    print("debug version now")
def release():
    print("release version now")

DEBUG_VERSION(debug)
RELEASE_VERSION(release)
```
当你使用 `python test.py debug` 时，会看到 `debug version now` ，而当你使用 `python test.py` 时，会看到 `release version now`