# 基于B树实现的图书管理系统
这是一个使用 Python 和 Tkinter 实现的图书管理系统，支持图书条目的增 (Create)、删 (Delete)、改 (Update)、查 (Search)操作，支持三种不同树形数据结构（普通二叉搜索树、AVL树、B树）的切换并对比了它们在核心操作上的性能表现（实现操作的速度）。

## 主要功能
图形化界面 (GUI): 提供图书条目展示与交互

核心操作: 支持图书条目的增 (Create)、删 (Delete)、改 (Update)、查 (Search)。

可切换数据结构: 系统可在启动时指定使用BST、AVL树或B树作为后端数据存储

性能基准测试: 包含独立的图书条目生成和测试脚本，用于定量分析不同数据结构的性能


## 核心数据结构:

ordinary_tree.py：普通树结构，限制最大子节点数为3，使用层序插入

avl_tree.py: AVL自平衡二叉搜索树

btree.py: B树


## 如何运行

1. 安装依赖

`pip install -r requirements.txt`

2. 运行主程序
程序支持通过命令行参数指定使用的数据结构 (bst, avl, btree)，默认为btree。

```
# 运行并使用默认的B树
python -m LibrarySystem.main

# 运行并指定使用AVL树
python -m LibrarySystem.main avl
```

运行界面：

![UI screenshot](../images/UI.png)

2. 性能测试
3. 
若要复现性能测试，请先按需生成测试数据：

```
# 生成50000条数据的.pkl文件
python generate_data.py 50000
```

然后运行性能测试脚本：

`python benchmark.py`

测试结果将直接输出在控制台。

测试结果示例：

![test result screenshot](../images/test.png)
