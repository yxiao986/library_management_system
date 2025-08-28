from LibrarySystem.book import Book

class AVLNode:
    def __init__(self, book):
        self.book = book      # 当前节点存储的图书对象
        self.left = None      # 左子节点
        self.right = None     # 右子节点
        self.height = 1       # 节点高度（用于平衡因子计算）

class BalancedTree:
    def __init__(self):
        self.root = None

    # 获取节点高度
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    # 计算平衡因子
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # 右旋操作
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        # 执行旋转
        x.right = y
        y.left = T2
        # 更新高度
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        return x

    # 左旋操作
    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        # 执行旋转
        y.left = x
        x.right = T2
        # 更新高度
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        return y

    # 插入图书
    def insert(self, book):
        self.root = self._insert(self.root, book)

    def _insert(self, node, book):
        # 普通BST插入
        if not node:
            return AVLNode(book)
        if book < node.book:
            node.left = self._insert(node.left, book)
        elif book > node.book:
            node.right = self._insert(node.right, book)
        else:
            # ISBN相同，不插入重复
            return node

        # 更新高度
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # 检查平衡并旋转
        balance = self._get_balance(node)

        # 左左
        if balance > 1 and book < node.left.book:
            return self._right_rotate(node)
        # 右右
        if balance < -1 and book > node.right.book:
            return self._left_rotate(node)
        # 左右
        if balance > 1 and book > node.left.book:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # 右左
        if balance < -1 and book < node.right.book:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # 查找图书
    def search(self, book):
        return self._search(self.root, book)

    def _search(self, node, book):
        if not node:
            return None
        if book == node.book:
            return node.book
        elif book < node.book:
            return self._search(node.left, book)
        else:
            return self._search(node.right, book)

    # 删除图书
    def delete(self, book):
        self.root = self._delete(self.root, book)

    def _delete(self, node, book):
        if not node:
            return node
        if book < node.book:
            node.left = self._delete(node.left, book)
        elif book > node.book:
            node.right = self._delete(node.right, book)
        else:
            # 找到要删除的节点
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # 有两个子节点，找中序后继
            temp = self._get_min_value_node(node.right)
            node.book = temp.book
            node.right = self._delete(node.right, temp.book)

        # 更新高度
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # 检查平衡并旋转
        balance = self._get_balance(node)

        # 左左
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        # 左右
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # 右右
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        # 右左
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # 获取最小值节点
    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # 更新图书信息（先删除旧的，再插入新的）
    def update(self, old_book, new_book):
        if self.search(old_book):
            self.delete(old_book)
        self.insert(new_book)

    # 中序遍历，返回所有图书对象列表
    def traverse(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result
        if node.left:
            self.traverse(node.left, result)
        result.append(node.book)
        if node.right:
            self.traverse(node.right, result)
        return result

if __name__ == "__main__":
    # 创建一些测试图书
    book1 = Book("Python编程", "张三", "978-7-123-45678-9", "电子工业出版社", 2020)
    book2 = Book("数据结构", "李四", "978-7-123-45679-6", "高等教育出版社", 2019)
    book3 = Book("算法导论", "王五", "978-7-123-45680-2", "机械工业出版社", 2018)
    book4 = Book("人工智能", "赵六", "978-7-123-45681-9", "清华大学出版社", 2021)

    print("测试平衡树实现")
    print("----------------")

    # 初始化平衡树
    tree = BalancedTree()

    # 测试插入
    tree.insert(book1)
    tree.insert(book2)
    tree.insert(book3)
    tree.insert(book4)
    print("插入后遍历：")
    for b in tree.traverse():
        print(b)

    # 测试查找
    print("\n查找book2:")
    found = tree.search(book2)
    print(found if found else "未找到")

    # 测试更新
    book2_new = Book("数据结构（第二版）", "李四", "978-7-123-45679-6", "高等教育出版社", 2022)
    tree.update(book2, book2_new)
    print("\n更新后遍历：")
    for b in tree.traverse():
        print(b)

    # 测试删除
    tree.delete(book3)
    print("\n删除book3后遍历：")
    for b in tree.traverse():
        print(b)