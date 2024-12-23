#!/bin/bash

# hdfs dfsadmin -report

## Create a dir, put files, and check the number of files
hdfs dfs -mkdir -p /articles

# Measure time taken for the put command
echo "Timing the put command:"
time hdfs dfs -D io.file.buffer.size=524288 -D dfs.blocksize=536870912 -put ./articles/* /articles

# Measure time taken for the ls command
echo "Timing the ls command:"
time hdfs dfs -ls /articles | wc -l


### if in safe mode:
# hdfs dfsadmin -safemode leave
# hdfs dfs -rm -r /articles