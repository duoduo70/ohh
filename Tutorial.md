# Ohh Tutorial

因为我几个月没编码（除了调那些愚蠢的 Lisp 遗留代码，顺便一提，我确实还在用那个我“小时候”用 Lisp 写的 Markdown 解析器生成博客代码，因为确实没有更好的方案），却又总是想写点什么，所以我就创造了这个项目（我食言了）。这套工具基本上服务于一种查找与替换的循环，最好的用途就是拿来本地化一些小众且简单的项目，例如各种基于 Electron 的项目，可能还有一些小厂 Galgame 。内置一套调试和查找工具，效率比手动一个个替换要高，尤其是本地化可以跟随源项目的更新而仍适用——只需要再那时候再跑一遍脚本即可。所以说，这个项目随时可以拿来干一些别的事情，只是我写它的主要需求是做一些自己要玩的游戏的本地化——磨磨唧唧一周过去，游戏已经打通关了，这一千行代码终于写出来了。虽然只有一千行，但这些代码都经过了不少的考量。当然，这不是我摸鱼的借口。

无论如何，请你记住，这个项目是一种服务于查找与替换的编译脚本，用以应对那种没有内置 i18n 且加入 i18n 的开销（主要是编程所要花费的时间）对你来说太大的情况，以至于我最初想要叫它 Transmake。它和一般的编译脚本不一样，一般的编译脚本是把代码编译到程序的程序，而 Ohh 主要是把程序编译到程序，只是语言改变了，所以这实际上是转换脚本而非编译脚本。按照数学家的命名方法，这应该是一个 2-program ，所以我在 logo 里用了代表 2-morphism 的双线箭头——这些都是废话，但或许可以让你会心一笑。

那么，让我们来替换第一个文件：
```json
{
    "a": "Some English"
}
```
如果其名字是 a.json ，我们编写这样的代码：
```python
from ohh import *
for_file("a.json").replace("Some English", "一些中文")
```
这会创建 build 文件夹并在其下生成 a.json 文件，其内容为：
```json
{
    "a": "一些中文"
}
```
我们先声明自己要操作哪个文件，然后说明我们要进行那些操作，语法十分简洁，可读性很强。

你可能会想，我们为什么不能直接根据 `a` 替换，而是要根据其值替换？
这样设计是经过考量的，如果键对应的英文改变了，而你还在用旧的中文，就会造成误解。

最简单的替换已经实现了，那么“查找”体现在哪里？还是那个例子，你只需要用这样的代码（之后省略 `import`）：
```python
ret = for_file("a.json").auto_extract_source()
print(ret)
```
它会输出：
```
{'Some English': 1}
```
auto_extract_source 函数会尝试提取所有可能需要本地化的项，你会注意到冒号后面跟着的数字 1 ，那是什么？那是一个项是否需要本地化（而非只是一些可配置的数据）的可能性。
我尝试尽可能量化可能性，例如如果项中有空格，可能性就大一些，因为 UUID 或 Base64 不会存在空格。即便这个方法看似很草台班子，但是很有效。TeX 中也用了许多概率有效的设定，以至于其在一段时间内被诟病，但历史证明这些选择是正确的。说实话，这个算法估计经常要更改，因为我没有真的做过统计。

事实上，上述代码应该改一下，以避免问题：
```python
clear_cache()
ret = for_file("a.json").auto_extract_source()
print(ret)
```
这会在正式执行操作之前清除上一次操作的缓存，否则可能会出现奇怪的问题。

你可能会想，对于这样的操作，也可以得到满意的结果：
```python
clear_cache()

ret = for_file("a.txt").auto_extract_source()
print(ret)
```
但实际上不行，因为程序不知道要对 txt 类型的文件做怎样的操作。对于每种不同的文件，我们可能要做不同的操作，于是对于同样的函数，其服务的文件扩展名不同，实现也就不同。截至我写这篇文章的时间点，我还没有为 txt 文件编写一个绑定，因为我个人没有这方面的需求。但你可以这么做，然后把你的实现发给我。

我们可以考虑一个更复杂的例子，对于一个文件夹，我们有：
```python
clear_cache()

result = for_dir("my_dir").auto_extract_source(AutoExtractSearchType.SEGMENT)
print("[")
for filename, data in result.items():
    for str_, p in data:
        if p >= 2:
            print("    ", end="")
            print((str_, filename), end="")
            print(",")
print("]")
```
这可以让我们在几万个文件里肉眼筛选需要本地化的字符串所在的文件位置，当然，这么好用的代码已经变成了内置函数：
```python
for_dir("my_dir").segment_dump()
```

你可能会想要为未受支持的文件格式绑定一个已有的实现，或替换标准实现到你自己的实现，你只需要在所有操作之前这样做：
```python
AUTO_EXTRACT_SOURCE[".java"] = modules.standard_string.auto_extract_source
SEARCH[".java"] = modules.standard_string.search
REPLACE[".java"] = modules.standard_string.replace
```
对于大多数格式，都是兼容 `standard_string` 的。

对于 for_dir ，如果碰到不支持的文件，则会跳过，对于 for_file ，则会报错。

关于 for_file 和 for_dir ，还有许多实用函数，且在增加中，详见 [ohh/easy.py](ohh/easy.py)

你现在应该已经可以编写一个脚本了，当你想要将其发布出去，我同样提供了一些实用函数，它们在 [ohh/cliutil.py](ohh/cliutil.py) 中：
```python
print_title("This is a title")
print_warning("This is a warning")
print_error("This is a error")
print_info("This is a info")
print_checking("Are you sure?") # 返回 bool
```
它们可以提供不同样式的输出，你可以运行一下试试。

以及，像几乎所有编译脚本一样，你可以编写 DEBUG 版 和 RELEASE 版，并将其放在一个文件里：
```python
from ohh import *

clear_cache()

def debug_version():
    print("It is debug version.")

def release_version():
    print("It is release version")

DEBUG_VERSION(debug_version)
RELEASE_VERSION(release_version)
```
当你用 `python test.py` 运行程序，你会看到输出 `It is release version`，当你用 `python test.py debug` 运行程序，你会看到输出 `It is debug version`。

## 示例：
在任意 Minecraft 模组中扫描可汉化（包括硬编码的）内容：
```python
from ohh import *

clear_cache()

for_file("your_mod.jar").unzip().as_dir().segment_dump()
```

Plasma
2024 年 6 月 5 日