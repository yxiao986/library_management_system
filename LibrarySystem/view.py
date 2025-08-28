import tkinter as tk

class BookSystemView:
    def __init__(self, master, tree_type="btree"):
        # 根据树类型设置窗口标题
        tree_type_map = {
            "btree": "B树版",
            "ordinary": "普通树版",
            "balanced": "平衡树版"
        }
        title = f"图书管理系统（{tree_type_map.get(tree_type, tree_type)}）"
        self.master = master
        self.master.title(title)

        self.listbox = tk.Listbox(master, width=80)
        self.listbox.pack(pady=10)

        btn_frame = tk.Frame(master)
        btn_frame.pack()

        self.btn_add = tk.Button(btn_frame, text="添加图书")
        self.btn_add.grid(row=0, column=0, padx=5)
        self.btn_delete = tk.Button(btn_frame, text="删除图书")
        self.btn_delete.grid(row=0, column=1, padx=5)
        self.btn_search = tk.Button(btn_frame, text="查找图书")
        self.btn_search.grid(row=0, column=2, padx=5)
        self.btn_update = tk.Button(btn_frame, text="修改图书")
        self.btn_update.grid(row=0, column=3, padx=5)
        self.btn_refresh = tk.Button(btn_frame, text="刷新列表")
        self.btn_refresh.grid(row=0, column=4, padx=5)