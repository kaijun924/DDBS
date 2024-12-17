from hadoop import Hadoop_handler
from PIL import Image
from io import BytesIO

hadoop = Hadoop_handler()
print(f"total {len(hadoop.list_files())} files in {hadoop.hdfs_dir}")
# print(f'Contents of {hadoop.hdfs_dir}: {hadoop.list_files()}')
contents = hadoop.read_file(3)
print(contents.keys())
for key in contents.keys():
    if key.endswith('.jpg'):
        img = Image.open(BytesIO(contents[key]))
        img.save(f'./{key}')
        print(f'Image {key} saved')
    else:
        print(contents[key].decode())