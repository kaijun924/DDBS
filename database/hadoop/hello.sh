hdfs dfsadmin -report

#开始加入
Namenode UI: http://localhost:9870
ResourceManager UI: http://localhost:8088

hdfs dfs -mkdir -p articles
hdfs dfs -D io.file.buffer.size=524288 -D dfs.blocksize=536870912 -put ./articles/* articles
# hdfs dfs -put ./articles/* articles