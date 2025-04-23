import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

file_path = os.path.join(data_dir, "data.txt")

with open(file_path) as file:
    lines = file.readlines()

output = '<string-array name="welders">\n'
# SPLIT by comma, STRIP quotes/whitespace/newlines
for line in lines:
    names = [name.strip("[]'\" \n\r") for name in line.split(",") if name.strip()]

    for name in names:
        output += f"    <item>{name}</item>\n"

output += "</string-array>"

print(output)
