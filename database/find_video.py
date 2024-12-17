import os

path = "./db-generation/articles"
files = os.listdir(path)

for file in files:
    inside = path + "/" + file
    inside_files = os.listdir(inside)
    for inside_file in inside_files:
        if inside_file.endswith(".flv"):
            print(file)
            break

