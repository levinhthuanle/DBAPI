import re
from lark import Lark, Tree, Token

from parser import grammar, SQLTransformer

# Tạo parser từ grammar và transformer
parser = Lark(grammar, start="start", parser="lalr", transformer=SQLTransformer())

# Danh sách các câu lệnh SQL mẫu để kiểm tra

queries = [
    {
        "query": "SELECT id, name FROM users WHERE age > 30 AND name LIKE 'John'",
        "expected": Tree(
            Token("RULE", "start"),
            [
                {
                    "type": "select",
                    "columns": ["id", "name"],
                    "table": "users",
                    "where": {
                        "op": "AND",
                        "left": {"left_operand": "age", "op": ">", "right_operand": 30},
                        "right": {
                            "left_operand": "name",
                            "op": "LIKE",
                            "right_operand": "'John'",
                        },
                    },
                    "limit": None,
                }
            ],
        ),
    },
    {
        "query": "SELECT id FROM users WHERE age IS NULL",
        "expected": Tree(
            Token("RULE", "start"),
            [
                {
                    "type": "select",
                    "columns": ["id"],
                    "table": "users",
                    "where": {"left_operand": "age", "op": "IS NULL"},
                    "limit": None,
                }
            ],
        ),
    },
    {
        "query": "SELECT id FROM users WHERE age >= 18 OR name = 'Jane Doe' LIMIT 10",
        "expected": Tree(
            Token("RULE", "start"),
            [
                {
                    "type": "select",
                    "columns": ["id"],
                    "table": "users",
                    "where": {
                        "op": "OR",
                        "left": {
                            "left_operand": "age",
                            "op": ">=",
                            "right_operand": 18,
                        },
                        "right": {
                            "left_operand": "name",
                            "op": "=",
                            "right_operand": "'Jane Doe'",
                        },
                    },
                    "limit": 10,
                }
            ],
        ),
    },
    {
        "query": "SELECT * FROM products LIMIT 5",
        "expected": Tree(
            Token("RULE", "start"),
            [
                {
                    "type": "select",
                    "columns": ["*"],
                    "table": "products",
                    "where": None,
                    "limit": 5,
                }
            ],
        ),
    },
]


# Hàm kiểm tra từng câu lệnh SQL
def test_parser():
    for case in queries:
        query = case["query"]
        expected = case["expected"]
        result = parser.parse(query)
        print(f"Query: {query}")
        print("Parsed Result:", result)
        assert result == expected, f"Failed for query: {query} \n  Got: {result}"
