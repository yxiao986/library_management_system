from LibrarySystem.book import Book
from collections import deque 

class OrdinaryTreeNode:
    def __init__(self, book):
        self.book = book  # 当前节点存储的图书对象
        self.children = []  # 子节点列表

class OrdinaryTree:
    def __init__(self):
        self.root = None  # 树的根节点

    def insert(self, book):
        """
        插入一本图书到普通树。
        采用广度优先搜索（BFS）找到第一个未满（子节点少于3个）的节点进行插入。
        """
        new_node = OrdinaryTreeNode(book)
        if self.root is None:
            self.root = new_node
            return

        # 使用队列实现广度优先搜索
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()

            # 找到了有空位的节点，插入并结束
            if len(current_node.children) < 3:
                current_node.children.append(new_node)
                return

            # 如果当前节点已满，将其所有子节点加入队列，继续寻找
            for child in current_node.children:
                queue.append(child)

    def search(self, book, node=None):
        """
        在树中查找指定图书，返回Book对象或None。
        """
        if node is None:
            node = self.root
        if node is None:
            return None
        if node.book == book:
            return node.book
        for child in node.children:
            result = self.search(book, child)
            if result:
                return result
        return None

    def delete(self, book):
        """
        删除指定图书。
        不支持删除根节点，只能删除根节点以下的节点。
        """
        if self.root is None:
            return False
        if self.root.book == book:
            # 不支持删除根节点
            return False
        return self._delete(self.root, book)

    def _delete(self, node, book):
        """
        辅助删除函数。递归查找并删除目标节点。
        """
        for i, child in enumerate(node.children):
            if child.book == book:
                node.children.pop(i)
                return True
            if self._delete(child, book):
                return True
        return False

    def update(self, old_book, new_book):
        """
        更新图书信息：查找目标节点并替换为新图书。
        """
        node = self._find_node(self.root, old_book)
        if node:
            node.book = new_book
            return True
        return False

    def _find_node(self, node, book):
        """
        辅助查找函数，返回存储指定图书的节点。
        """
        if node is None:
            return None
        if node.book == book:
            return node
        for child in node.children:
            found = self._find_node(child, book)
            if found:
                return found
        return None

    def traverse(self, node=None, result=None):
        """
        前序遍历整棵树，返回所有图书对象的列表。
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result
        result.append(node.book)
        for child in node.children:
            self.traverse(child, result)
        return result

if __name__ == "__main__":
    # 创建一些测试图书
    book1 = Book("Python编程", "张三", "978-7-123-45678-9", "电子工业出版社", 2020)
    book2 = Book("数据结构", "李四", "978-7-123-45679-6", "高等教育出版社", 2019)
    book3 = Book("算法导论", "王五", "978-7-123-45680-2", "机械工业出版社", 2018)
    book4 = Book("人工智能", "赵六", "978-7-123-45681-9", "清华大学出版社", 2021)

    print("测试普通树实现")
    print("----------------")

    # 初始化普通树
    tree = OrdinaryTree()

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