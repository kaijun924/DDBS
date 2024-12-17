from hdfs import InsecureClient
from PIL import Image
import hdfs
import os
from io import BytesIO

# # 连接到 HDFS
# hdfs_client = InsecureClient('http://localhost:9870', user='root')  # NameNode Web UI 地址
# hdfs_dir = 'articles'
# contents = hdfs_client.list(hdfs_dir)
# print(f"total {len(contents)} files in {hdfs_dir}")
# print(f'Contents of {hdfs_dir}: {contents}')

class Hadoop_handler:
    def __init__(self):
        self.hdfs_client = InsecureClient('http://localhost:9870', user='root')
        self.hdfs_dir = 'articles/'
    
    def list_files(self):
        contents = self.hdfs_client.list(self.hdfs_dir)
        return contents
    
    def read_file(self,article_id):
        article = f'article{article_id}'
        try:
            list_in_article = self.hdfs_client.list(self.hdfs_dir + article)
            print(f'Contents of {self.hdfs_dir + article}: {list_in_article}')
            contents = {}
            for file in list_in_article:
                with self.hdfs_client.read(self.hdfs_dir + article + '/' + file) as reader:
                    contents[file] = reader.read()
            return contents
        except hdfs.HdfsError as e:
            print(e)
    
    def write_file(self, article_id, file_name, content):
        article = f'article{article_id}'
        try:
            self.hdfs_client.write(self.hdfs_dir + article + '/' + file_name, data=content, overwrite=True)
        except hdfs.HdfsError as e:
            print(e)
    
    def delete_file(self, article_id, file_name):
        article = f'article{article_id}'
        try:
            self.hdfs_client.delete(self.hdfs_dir + article + '/' + file_name)
        except hdfs.HdfsError as e:
            print(e)

# hadoop = Hadoop_handler()
# print(f"total {len(hadoop.list_files())} files in {hadoop.hdfs_dir}")
# # print(f'Contents of {hadoop.hdfs_dir}: {hadoop.list_files()}')
# contents = hadoop.read_file(3)
# print(contents.keys())
# for key in contents.keys():
#     if key.endswith('.jpg'):
#         img = Image.open(BytesIO(contents[key]))
#         img.save(f'./{key}')
#         print(f'Image {key} saved')
#     else:
#         print(contents[key].decode())