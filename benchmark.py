import sys
from pathlib import Path

import pickle
import time
from LibrarySystem.data_structures.btree import BTree
from LibrarySystem.data_structures.ordinary_tree import OrdinaryTree
from LibrarySystem.data_structures.avl_tree import BalancedTree

def load_books(filename):
    DATA_DIR = Path(__file__).parent / 'data'
    filename = DATA_DIR / filename
    with open(filename, "rb") as f:
        return pickle.load(f)

def benchmark_insert(tree_class, books):
    tree = tree_class() if tree_class != BTree else tree_class(t=2)
    start = time.perf_counter()
    for book in books:
        tree.insert(book)
    end = time.perf_counter()
    return tree, end - start

def benchmark_search(tree, books):
    start = time.perf_counter()
    found = 0
    for book in books:
        if tree.search(book):
            found += 1
    end = time.perf_counter()
    return found, end - start

def benchmark_delete(tree_class, books):
    # 先插入所有数据
    tree = tree_class() if tree_class != BTree else tree_class(t=2)
    for book in books:
        tree.insert(book)
    # 再删除
    start = time.perf_counter()
    for book in books:
        tree.delete(book)
    end = time.perf_counter()
    return end - start

def run_benchmark(dataset_name, books):
    results = []
    for name, tree_class in [
        ("BTree", BTree),
        ("OrdinaryTree", OrdinaryTree),
        ("BalancedTree", BalancedTree)
    ]:
        print(f"测试 {name} on {dataset_name} ...")
        # 插入
        tree, insert_time = benchmark_insert(tree_class, books)
        # 查找
        found, search_time = benchmark_search(tree, books)
        # 删除
        delete_time = benchmark_delete(tree_class, books)
        results.append({
            "tree": name,
            "insert_time": insert_time,
            "search_time": search_time,
            "delete_time": delete_time,
            "found": found
        })
        print(f"{name} 插入: {insert_time:.4f}s, 查找: {search_time:.4f}s, 删除: {delete_time:.4f}s, 查找到: {found}")
    return results

if __name__ == "__main__":

    DATA_DIR = Path(__file__).parent / 'data'
    # 通过命令行参数指定数据集大小，默认5000
    DATA_SIZE = 5000
    if len(sys.argv) > 1:
        DATA_SIZE = int(sys.argv[1])

    # 加载数据
    random_books = load_books(DATA_DIR/f"random_books_{DATA_SIZE}.pkl")
    ordered_books = load_books(DATA_DIR/f"ordered_books_{DATA_SIZE}.pkl")

    all_results = {}

    # 测试随机数据集
    print("===== 随机数据集测试 =====")
    results_random = run_benchmark("random_books", random_books)
    all_results["random_books"] = results_random

    # 测试有序数据集
    print("\n===== 有序数据集测试 =====")
    results_ordered = run_benchmark("ordered_books", ordered_books)
    all_results["ordered_books"] = results_ordered
