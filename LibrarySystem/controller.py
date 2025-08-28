import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from LibrarySystem.book import Book

class BookSystemController:
    def __init__(self, view, tree):
        self.view = view
        self.tree = tree

        # 绑定按钮事件
        self.view.btn_add.config(command=self.add_book)
        self.view.btn_delete.config(command=self.delete_book)
        self.view.btn_search.config(command=self.search_book)
        self.view.btn_update.config(command=self.update_book)
        self.view.btn_refresh.config(command=self.refresh_list)

        self.refresh_list()

    def add_book(self):
        title = simpledialog.askstring("添加图书", "书名：")
        if not title or not title.strip():
            messagebox.showwarning("警告", "书名不能为空")
            return
        author = simpledialog.askstring("添加图书", "作者：")
        if not author or not author.strip():
            messagebox.showwarning("警告", "作者不能为空")
            return
        isbn = simpledialog.askstring("添加图书", "ISBN：")
        if not self._is_valid_isbn(isbn):
            messagebox.showwarning("警告", "ISBN格式无效，应为13位数字")
            return
        publisher = simpledialog.askstring("添加图书", "出版社：")
        if not publisher or not publisher.strip():
            messagebox.showwarning("警告", "出版社不能为空")
            return
        year = simpledialog.askinteger("添加图书", "出版年份：")
        if not year or year < 1000 or year > 2100:
            messagebox.showwarning("警告", "请输入有效的出版年份")
            return

        book = Book(title.strip(), author.strip(), isbn.strip(), publisher.strip(), year)
        self.tree.insert(book)
        self.refresh_list()
        messagebox.showinfo("提示", "添加成功！")

    def delete_book(self):
        idx = self.view.listbox.curselection()
        if not idx:
            messagebox.showwarning("警告", "请先选择要删除的图书")
            return
        book_str = self.view.listbox.get(idx)
        isbn = self._extract_isbn(book_str)
        book = self._find_book_by_isbn(isbn)
        if book:
            self.tree.delete(book)
            self.refresh_list()
            messagebox.showinfo("提示", "删除成功！")
        else:
            messagebox.showwarning("警告", "未找到该图书")

    def search_book(self):
        isbn = simpledialog.askstring("查找图书", "请输入ISBN：")
        if not isbn:
            return
        book = self._find_book_by_isbn(isbn)
        if book:
            messagebox.showinfo("查找结果", str(book))
        else:
            messagebox.showinfo("查找结果", "未找到该图书")

    def update_book(self):
        idx = self.view.listbox.curselection()
        if not idx:
            messagebox.showwarning("警告", "请先选择要修改的图书")
            return
        book_str = self.view.listbox.get(idx)
        isbn = self._extract_isbn(book_str)
        old_book = self._find_book_by_isbn(isbn)
        if not old_book:
            messagebox.showwarning("警告", "未找到该图书")
            return

        title = simpledialog.askstring("修改图书", "书名：", initialvalue=old_book.title)
        if not title or not title.strip():
            messagebox.showwarning("警告", "书名不能为空")
            return
        author = simpledialog.askstring("修改图书", "作者：", initialvalue=old_book.author)
        if not author or not author.strip():
            messagebox.showwarning("警告", "作者不能为空")
            return
        publisher = simpledialog.askstring("修改图书", "出版社：", initialvalue=old_book.publisher)
        if not publisher or not publisher.strip():
            messagebox.showwarning("警告", "出版社不能为空")
            return
        year = simpledialog.askinteger("修改图书", "出版年份：", initialvalue=old_book.year)
        if not year or year < 1000 or year > 2100:
            messagebox.showwarning("警告", "请输入有效的出版年份")
            return

        new_book = Book(title.strip(), author.strip(), old_book.isbn, publisher.strip(), year)
        self.tree.update(old_book, new_book)
        self.refresh_list()
        messagebox.showinfo("提示", "修改成功！")

    def refresh_list(self):
        self.view.listbox.delete(0, "end")
        books = self.tree.traverse()
        for book in books:
            self.view.listbox.insert("end", str(book))

    def _extract_isbn(self, book_str):
        import re
        match = re.search(r"ISBN: ([^,， ]+)", book_str)
        return match.group(1) if match else ""

    def _find_book_by_isbn(self, isbn):
        for book in self.tree.traverse():
            if book.isbn == isbn:
                return book
        return None

    def _is_valid_isbn(self, isbn):
        # 校验ISBN格式（13位数字，允许短横线）
        import re
        if not isbn:
            return False
        isbn = isbn.strip()
        # 允许格式如 978-7-123-45678-9 或 9787123456789
        return bool(re.fullmatch(r"\d{3}-\d-\d{3}-\d{5}-\d|\d{13}", isbn))


if __name__ == "__main__":
    # 通过命令行参数指定树类型，默认btree
    tree_type = "btree"
    if len(sys.argv) > 1:
        tree_type = sys.argv[1].lower()
    root = tk.Tk()
    app = BookSystemController(root, tree_type=tree_type)
    root.mainloop()