from collections import deque
from LibrarySystem.book import Book

class TreeNode:
    """
    节点类基本不变，但构造时不再需要max_children，
    因为这个限制属于树的整体属性。
    """
    def __init__(self, data):
        self.data = data
        self.children = []

    def __str__(self):
        # 方便打印Book对象的标题
        if hasattr(self.data, 'title'):
            return self.data.title
        return str(self.data)

class OrdinaryTree:
    def __init__(self, max_children_per_node=3):
        """
        初始化一棵空树，根节点为 None。
        """
        self.root = None
        self.max_children = max_children_per_node

    def is_full(self, node):
        """辅助方法，检查节点是否已满"""
        return len(node.children) >= self.max_children

    # --- 核心功能接口 ---

    def insert(self, book):
        """
        插入一本新书。如果树为空，则成为根节点。
        否则，以层序方式寻找第一个未满的节点并插入。
        """
        new_node = TreeNode(book)
        
        # 情况1：树是空的，新节点成为根节点
        if self.root is None:
            self.root = new_node
            return True

        # 情况2：树非空，层序遍历寻找插入位置
        queue = deque([self.root])
        
        while queue:
            current_node = queue.popleft()
            
            if not self.is_full(current_node):
                current_node.children.append(new_node)
                return True
            else:
                for child in current_node.children:
                    queue.append(child)
        return False

    def search(self, book_to_find):
        """
        查找一本书，会跳过数据为None的节点。
        """
        if self.root is None:
            return None
        
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            # 跳过空节点
            if current_node.data is not None and current_node.data == book_to_find:
                return current_node.data
            
            for child in current_node.children:
                queue.append(child)
        return None

    def delete(self, book_to_delete):
        """
        在树中查找一本书，并将其节点数据置为 None（逻辑删除）。
        这种方法可以保证树的物理结构不变，也不会产生“空洞”。
        """
        if self.root is None:
            return False

        # 使用队列进行广度优先搜索 (BFS) 来查找目标节点
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()

            # 检查当前节点的数据是否是我们想删除的
            # 需要处理当前节点数据可能已经是None的情况
            if current_node.data is not None and current_node.data == book_to_delete:
                # 找到了！将数据置为 None，完成逻辑删除
                current_node.data = None
                return True
            
            # 将子节点加入队列继续搜索
            for child in current_node.children:
                queue.append(child)
        
        # 遍历完也没找到
        return False
        
    def update(self, old_book, new_book):
        """
        更新图书信息，会跳过数据为None的节点。
        """
        if self.root is None:
            return False
        
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            if current_node.data is not None and current_node.data == old_book:
                current_node.data = new_book
                return True
            for child in current_node.children:
                queue.append(child)
        return False
        
    def traverse(self):
        """
        遍历并返回所有有效的图书，会跳过数据为None的节点。
        """
        if self.root is None:
            return []
            
        books = []
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            # 只收集有效数据
            if current_node.data is not None:
                books.append(current_node.data)
            for child in current_node.children:
                queue.append(child)
        return books
    

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