import sys
import tkinter as tk
from LibrarySystem.controller import BookSystemController
from LibrarySystem.view import BookSystemView

# 支持的树类型映射
TREE_CLASSES = {
    "btree": ("btree", "BTree"),
    "ordinary": ("ordinary_tree", "OrdinaryTree"),
    "balanced": ("balanced_tree", "BalancedTree"),
}

def create_tree(tree_type):
    if tree_type not in TREE_CLASSES:
        from LibrarySystem.data_structures.btree import BTree
        return BTree(t=2)
    module_name, class_name = TREE_CLASSES[tree_type]
    module_name = f"LibrarySystem.data_structures.{module_name}"
    module = __import__(module_name, fromlist=[class_name])
    tree_class = getattr(module, class_name)
    if tree_type == "btree":
        return tree_class(t=2)
    else:
        return tree_class()

if __name__ == "__main__":
    # 通过命令行参数指定树类型，默认btree
    tree_type = "btree"
    if len(sys.argv) > 1:
        tree_type = sys.argv[1].lower()
    #创建一个主窗口对象
    root = tk.Tk()

    #创建一个图书馆里系统界面的类别
    view = BookSystemView(root, tree_type)

    #创建一棵树
    tree = create_tree(tree_type)

    #创建一个控制器
    app = BookSystemController(view, tree)

    #进入主循环
    root.mainloop()