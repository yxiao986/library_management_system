from LibrarySystem.book import Book

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # 最小度数
        self.leaf = leaf  # 是否为叶子节点
        self.keys = []  # 存储键（Book对象）
        self.children = []  # 存储子节点

    def __str__(self):
        return f"Keys: {self.keys}, Leaf: {self.leaf}"

class BTree:
    def __init__(self, t=2):
        self.t = t  # 最小度数
        self.root = BTreeNode(t, leaf=True)  # 初始化根节点为叶子

    # 公共方法，作为用户调用的接口
    def search(self, k):
        """在B树中查找键k，返回找到的Book对象或None"""
        return self._search(self.root, k)

    # 私有辅助方法，实现递归逻辑
    def _search(self, node, k):
        if node is None:
            return None
    
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
    
        if i < len(node.keys) and k == node.keys[i]:
            return node.keys[i]
    
        if node.leaf:
            return None
        
        return self._search(node.children[i], k)

    def insert(self, k):
        """
        插入键k到B树
        """
        root = self.root
        # 如果根节点已满，分裂根节点
        if len(root.keys) == (2 * self.t) - 1:
            s = BTreeNode(self.t, leaf=False)
            s.children.insert(0, root)
            self._split_child(s, 0)
            self.root = s
            self._insert_non_full(s, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node, k):
        """
        在非满节点node中插入k
        """
        i = len(node.keys) - 1
        if node.leaf:
            # 在叶子节点插入
            node.keys.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            # 在内部节点插入
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            # 如果子节点已满，先分裂
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, parent, i):
        """
        分裂parent的第i个子节点
        """
        t = self.t
        y = parent.children[i]
        z = BTreeNode(t, leaf=y.leaf)
        # 新节点z获得y的后t-1个键
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:t - 1]
        # 如果不是叶子节点，分配子节点
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    def delete(self, k):
        """
        删除键k
        """
        self._delete(self.root, k)
        # 如果根节点没有键且不是叶子，降级根节点
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete(self, node, k):
        """
        递归删除节点中的k
        """
        t = self.t
        idx = 0
        # 找到第一个大于等于k的位置
        while idx < len(node.keys) and k > node.keys[idx]:
            idx += 1

        # 情况1：k在当前节点
        if idx < len(node.keys) and node.keys[idx] == k:
            if node.leaf:
                # 1a：k在叶子节点，直接删除
                node.keys.pop(idx)
                return True
            else:
                # 1b：k在内部节点
                # 前驱子节点有t个及以上键
                if len(node.children[idx].keys) >= t:
                    pred = self._get_predecessor(node, idx)
                    node.keys[idx] = pred
                    self._delete(node.children[idx], pred)
                # 后继子节点有t个及以上键
                elif len(node.children[idx + 1].keys) >= t:
                    succ = self._get_successor(node, idx)
                    node.keys[idx] = succ
                    self._delete(node.children[idx + 1], succ)
                else:
                    # 合并k和右孩子到左孩子
                    self._merge(node, idx)
                    self._delete(node.children[idx], k)
                return True
        else:
            # 情况2：k不在当前节点
            if node.leaf:
                # k不在树中
                return False
            flag = (idx == len(node.keys))
            # 如果目标子节点只有t-1个键，需要填充
            if len(node.children[idx].keys) < t:
                self._fill(node, idx)
            # 填充后，递归到合适的子节点
            if flag and idx > len(node.keys):
                self._delete(node.children[idx - 1], k)
            else:
                self._delete(node.children[idx], k)
            return True

    def _get_predecessor(self, node, idx):
        """
        获取node.keys[idx]的前驱（左子树的最右节点）
        """
        cur = node.children[idx]
        while not cur.leaf:
            cur = cur.children[-1]
        return cur.keys[-1]

    def _get_successor(self, node, idx):
        """
        获取node.keys[idx]的后继（右子树的最左节点）
        """
        cur = node.children[idx + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def _merge(self, node, idx):
        """
        合并node的第idx个孩子和第idx+1个孩子，并把中间的key下移
        """
        child = node.children[idx]
        sibling = node.children[idx + 1]
        t = self.t
        # 把中间的key和右兄弟合并到左孩子
        child.keys.append(node.keys[idx])
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        node.keys.pop(idx)
        node.children.pop(idx + 1)

    def _fill(self, node, idx):
        """
        保证node.children[idx]有至少t个键
        """
        t = self.t
        # 如果左兄弟有多于t-1个键，借一个
        if idx != 0 and len(node.children[idx - 1].keys) >= t:
            self._borrow_from_prev(node, idx)
        # 如果右兄弟有多于t-1个键，借一个
        elif idx != len(node.children) - 1 and len(node.children[idx + 1].keys) >= t:
            self._borrow_from_next(node, idx)
        else:
            # 合并
            if idx != len(node.children) - 1:
                self._merge(node, idx)
            else:
                self._merge(node, idx - 1)

    def _borrow_from_prev(self, node, idx):
        """
        从左兄弟借一个key
        """
        child = node.children[idx]
        sibling = node.children[idx - 1]
        # child向左兄弟借一个key
        child.keys.insert(0, node.keys[idx - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        node.keys[idx - 1] = sibling.keys.pop()

    def _borrow_from_next(self, node, idx):
        """
        从右兄弟借一个key
        """
        child = node.children[idx]
        sibling = node.children[idx + 1]
        # child向右兄弟借一个key
        child.keys.append(node.keys[idx])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        node.keys[idx] = sibling.keys.pop(0)

    def traverse(self, node=None, result=None):
        """
        中序遍历B树，返回所有Book对象列表
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        i = 0
        for i in range(len(node.keys)):
            if not node.leaf:
                self.traverse(node.children[i], result)
            result.append(node.keys[i])
        if not node.leaf:
            self.traverse(node.children[i + 1], result)
        return result

    def update(self, old_book, new_book):
        """
        更新图书信息：先删除旧的，再插入新的
        """
        if self.search(old_book):
            self.delete(old_book)
        self.insert(new_book)

# 为了方便替换不同树结构，建议后续所有树结构都实现如下接口：
# - insert(book)
# - delete(book)
# - search(book)
# - update(old_book, new_book)
#

if __name__ == "__main__":
    # 创建一些测试图书
    book1 = Book("Python编程", "张三", "978-7-123-45678-9", "电子工业出版社", 2020)
    book2 = Book("数据结构", "李四", "978-7-123-45679-6", "高等教育出版社", 2019)
    book3 = Book("算法导论", "王五", "978-7-123-45680-2", "机械工业出版社", 2018)
    book4 = Book("人工智能", "赵六", "978-7-123-45681-9", "清华大学出版社", 2021)
    print("测试B树实现")
    print("----------------")   


    # 初始化B树
    btree = BTree(t=2)

    # 测试插入
    btree.insert(book1)
    btree.insert(book2)
    btree.insert(book3)
    btree.insert(book4)
    print("插入后遍历：")
    for b in btree.traverse():
        print(b)

    # 测试查找
    print("\n查找book2:")
    found = btree.search(book2)
    print(found if found else "未找到")

    # 测试更新
    book2_new = Book("数据结构（第二版）", "李四", "978-7-123-45679-6", "高等教育出版社", 2022)
    btree.update(book2, book2_new)
    print("\n更新后遍历：")
    for b in btree.traverse():
        print(b)

    # 测试删除
    btree.delete(book3)
    print("\n删除book3后遍历：")
    for b in btree.traverse():
        print(b)