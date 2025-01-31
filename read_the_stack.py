import csv

input_file = "the_stack.csv"

# Read the CSV file
with open(input_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    data = list(reader)


#Headers : language,stack_v2_num_files,stack_v2_dedup_num_files,stack_v2_train_num_files,stack_v2_size_bytes,stack_v2_dedup_size_bytes,stack_v2_train_size_bytes
# Sort the data by stack_v2_dedup_size_bytes (index 5)
data.sort(key=lambda x: -int(x[5]))

# Print only the language and stack_v2_dedup_size_bytes
for row in data:
    dedup_bytes = int(row[5])
    print(f"Language: {row[0]}, Dedup Size Bytes: {dedup_bytes//1_000_000} MB")