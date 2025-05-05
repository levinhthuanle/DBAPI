from lark import Lark
from parser import grammar, SQLTransformer

# Tạo parser từ grammar và transformer
parser = Lark(grammar, start='start', parser='lalr', transformer=SQLTransformer())

# Danh sách các câu lệnh SQL mẫu để kiểm tra
queries = [
    "SELECT id, name FROM users WHERE age > 30 AND name LIKE 'John%'",
    "SELECT id FROM users WHERE age IS NULL",
    "SELECT id FROM users WHERE age >= 18 OR name = 'Jane Doe' LIMIT 10", 
    "SELECT * FROM products LIMIT",
]

# Hàm kiểm tra từng câu lệnh SQL
def test_parser():
    for query in queries:
        try:
            print(f"Query: {query}")
            result = parser.parse(query)
            print("Parsed Result:", result)
            print("-" * 50)
        except Exception as e:
            print(f"Error parsing query: {query}")
            print(f"Error: {e}")
            print("-" * 50)

# Chạy kiểm tra
test_parser()