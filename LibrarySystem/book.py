class Book:
    def __init__(self, title, author, isbn, publisher, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.year = year

    #对对象使用 print() 函数或 str() 函数时被调用
    def __str__(self):
        return f"《{self.title}》, 作者: {self.author}, ISBN: {self.isbn}, 出版社: {self.publisher}, 出版年份: {self.year}"

    #直接在解释器中输入对象名并回车，或者使用 repr() 函数时被调用
    def __repr__(self):
        return (f"Book(title={self.title!r}, author={self.author!r}, "
                f"isbn={self.isbn!r}, publisher={self.publisher!r}, year={self.year!r})")

    # 比较运算符重载，基于 ISBN 进行比较
    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        

    def __lt__(self, other):
        if isinstance(other, Book):
            return self.isbn < other.isbn
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Book):
            return self.isbn <= other.isbn
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Book):
            return self.isbn > other.isbn
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Book):
            return self.isbn >= other.isbn
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Book):
            return self.isbn != other.isbn
        return NotImplemented