import sys
from ohh import *

# 可以通过命令直接调用部分函数

eval(f'''print({sys.argv[1]}({
    ','.join(sys.argv[2::])
}))''')