import dbcsv
import time


def test_connection():
    conn = dbcsv.connect(
        dsn="http://localhost:80/testing", user="johndoe", password="secret"
    )

    try:
        print("Connect to database successfully")
        
        cursor = conn.cursor()
        queries = ["SELECT * FROM mock_data WHERE col_0 > 50 and col_1 < 50 or col_3 > 50",
                    ]
        times = []
        for i in range(len(queries)):
            start = time.time()
            cursor.execute(queries[i])
            res = cursor.fetchall()
            times.append(time.time() - start)
            print(f"Query {i+1}: {len(res)} rows")
        print("Times:", times , "=", sum(times) / len(times))
        return True
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return False


if __name__ == "__main__":
    test_connection()