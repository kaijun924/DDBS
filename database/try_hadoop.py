from hadoop import Hadoop_handler
from PIL import Image
from io import BytesIO
import vlc

hadoop = Hadoop_handler()
print(f"total {len(hadoop.list_files())} files in {hadoop.hdfs_dir}")
# print(f'Contents of {hadoop.hdfs_dir}: {hadoop.list_files()}')
contents = hadoop.read_file(1010)
print(contents.keys())
for key in contents.keys():
    if key.endswith('.jpg'):
        img = Image.open(BytesIO(contents[key]))
        img.save(f'./{key}')
        print(f'Image {key} saved')
    elif key.endswith('.txt'):
        print(contents[key].decode())
    else:
        print(contents[key])
        # video.save(f'./{key}')