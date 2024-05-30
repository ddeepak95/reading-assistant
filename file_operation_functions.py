# Read txt file
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    print("File read successfully")
    return data

# Write txt file
def write_txt_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)
    print("File write successful")