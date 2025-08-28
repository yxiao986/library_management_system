import sys
from pathlib import Path

from faker import Faker
from LibrarySystem.book import Book
import pickle
import random
from pathlib import Path

def generate_books(n, ordered=False, seed=42):
    fake = Faker("zh_CN")
    Faker.seed(seed)
    books = []
    for i in range(n):
        # 生成13位ISBN
        isbn = f"{random.randint(100,999)}-{random.randint(1,9)}-{random.randint(100,999)}-{random.randint(10000,99999)}-{random.randint(0,9)}"
        book = Book(
            title=fake.sentence(nb_words=3),
            author=fake.name(),
            isbn=isbn,
            publisher=fake.company(),
            year=random.randint(1990, 2024)
        )
        books.append(book)
    if ordered:
        # 按ISBN排序，生成有序数据
        books.sort(key=lambda b: b.isbn)
    return books

if __name__ == "__main__":

    DATA_DIR = Path(__file__).parent / 'data'
    
    # 通过命令行参数指定数据集大小，默认5000
    DATA_SIZE = 5000
    if len(sys.argv) > 1:
        DATA_SIZE = int(sys.argv[1])

    # 生成随机数据集
    random_books = generate_books(DATA_SIZE, ordered=False)
    with open(DATA_DIR/f"random_books_{DATA_SIZE}.pkl", "wb") as f:
        pickle.dump(random_books, f)
    print(f"已生成随机数据集 random_books_{DATA_SIZE}.pkl")

    # 生成有序数据集
    ordered_books = generate_books(DATA_SIZE, ordered=True)
    with open(DATA_DIR/f"ordered_books_{DATA_SIZE}.pkl", "wb") as f:
        pickle.dump(ordered_books, f)
    print(f"已生成有序数据集 ordered_books_{DATA_SIZE}.pkl")

