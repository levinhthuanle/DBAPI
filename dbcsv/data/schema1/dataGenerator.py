import csv
import random

# Filepath của file CSV
filepath = r'd:\GitHub\intern-dbcsv\dbcsv\data\schema1\table1.csv'

# Tên cột
columns = ['id', 'name', 'age', 'email']

# Hàm tạo dữ liệu mẫu
def generate_sample_data(num_rows):
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'Chris', 'Sarah', 'David', 'Laura', 'Robert', 'Sophia']
    last_names = ['Doe', 'Smith', 'Brown', 'Davis', 'Wilson', 'Johnson', 'Taylor', 'Anderson', 'Thomas', 'Moore']
    domains = ['example.com', 'test.com', 'demo.com', 'sample.com']

    for i in range(6, num_rows + 6):  # Bắt đầu từ ID 6
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        age = random.randint(18, 65)
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        yield [i, name, age, email]

# Ghi dữ liệu vào file CSV
with open(filepath, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Ghi thêm 1.000.000 dòng dữ liệu
    writer.writerows(generate_sample_data(1000000))

print("Đã thêm 1.000.000 dòng dữ liệu mẫu vào file table1.csv.")