from collections import deque, defaultdict

pos = int
def search_in_data(data: bytes, patterns: list[bytes]) -> dict[bytes, pos]:
    ac = AhoCorasick()
    for pattern in patterns:
        ac.add_word(pattern)
    ac.build()
    return ac.search(data)

class AhoCorasick:
    def __init__(self):
        self.adj = defaultdict(dict)  # 转移函数
        self.fail = {}  # 失败指针
        self.output = defaultdict(list)  # 输出函数

    def add_word(self, word: bytes):
        node = 0
        for byte in word:
            node = self.adj[node].setdefault(byte, len(self.adj))
        self.output[node].append(word)

    def build(self):
        self.fail[0] = 0
        queue = deque()
        for byte, node in self.adj[0].items():
            self.fail[node] = 0
            queue.append(node)
        
        while queue:
            r = queue.popleft()
            for byte, u in self.adj[r].items():
                queue.append(u)
                v = self.fail[r]
                while v != 0 and byte not in self.adj[v]:
                    v = self.fail[v]
                self.fail[u] = self.adj[v].get(byte, 0)
                self.output[u].extend(self.output[self.fail[u]])

    def search(self, data: bytes):
        node = 0
        positions = dict()
        for index, byte in enumerate(data):
            while node != 0 and byte not in self.adj[node]:
                node = self.fail[node]
            node = self.adj[node].get(byte, 0)
            for pattern in self.output[node]:
                positions[pattern] = index - len(pattern) + 1
        return positions