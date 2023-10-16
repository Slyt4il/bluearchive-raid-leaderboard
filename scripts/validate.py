import csv

def check_order(csv_file, range_end, encoding='utf-8'):
    num_set = set(range(1, range_end + 1))
    with open(csv_file, 'r', encoding=encoding) as file:
        reader = csv.reader(file)
        next(reader)
        data = [int(row[0]) for row in reader]

    errors = []
    if len(data) != range_end or len(set(data)) != range_end:
        for num in range(1, range_end + 1):
            if data.count(num) > 1:
                errors.append(f"Duplicate number found: {num}")
            elif data.count(num) == 0:
                errors.append(f"Missing number found: {num}")

    if errors:
        return "\n".join(errors)
    else:
        return f"All numbers from 1 to {range_end} exist without any duplicates."

last_rank = 10000

result = check_order('S46_Goz_Indoor_ASIA_TOP10000.csv', last_rank)
print(result)
