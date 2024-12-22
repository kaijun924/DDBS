from base_handler import MongoDBHandler, TableHandler
"""
id, timestamp, aid, readNum, readUidList, commentNum, commentUidList, 
agreeNum, agreeUidList, shareNum, shareUidList 

id = br{aid}
timestamp = time.time()
aid = aid (article id)
readNum = len(read_uid_list)
readUidList = read_uid_list
commentNum = len(comment_uid_list) 
commentUidList = comment_uid_list (for commentorNot: 1)
agreeNum = len(agree_uid_list)
agreeUidList = agree_uid_list (for agreeorNot: 1)
shareNum = len(share_uid_list)
shareUidList = share_uid_list (for sharerNot: 1)
"""
#所以需要article,read
# from handler import ReadTableHandler
import time
import pandas as pd

class BeReadTools:
    """"
    initialize, make sure the read and article table is ready
    """
    def __init__(self):
        pass
        # self.readTableHandler = ReadTableHandler(db_handler)

    """
    用 article 方式来迭代,给一个aid,返回一个beRead的list
    """
    def _get_beRead_by_aid(self, article, readTableHandler):
        #全部改成get, 可能会有问题
        aid = article.get("aid")
        read = readTableHandler.fetch_reads_to_beread({"aid": aid})
        beRead_entity = {}

        beRead_entity["id"] = "br" + aid
        beRead_entity["timestamp"] = str(time.time())
        beRead_entity["aid"] = aid
        beRead_entity["readNum"] = str(len(read))
        beRead_entity["readUidList"] = [r["uid"] for r in read]
        commentUidList = [r["uid"] for r in read if r["commentOrNot"] == "1"]
        beRead_entity["commentNum"] = str(len(commentUidList))
        beRead_entity["commentUidList"] = commentUidList

        agreeUidList = [r["uid"] for r in read if r["agreeOrNot"] == "1"]
        beRead_entity["agreeNum"] = str(len(agreeUidList))
        beRead_entity["agreeUidList"] = agreeUidList

        shareUidList = [r["uid"] for r in read if r["shareOrNot"] == "1"]
        beRead_entity["shareNum"] = str(len(shareUidList))
        beRead_entity["shareUidList"] = shareUidList

        #添加tag, 类似article
        beRead_entity["category"] = article.get("category")
        if article.get("category") == "science":
            r1 = beRead_entity.copy()
            r2 = beRead_entity.copy()
            r1["shardCopy"] = "1"
            r2["shardCopy"] = "2"
            return [r1, r2]


        return [beRead_entity]

class ReadTime:
    def __init__(self, timestamp):
        t = pd.to_datetime(int(timestamp), unit='ms')
        self.read_timestamp = {
            'daily': f'{t.day}-{t.month}-{t.year}',
            'weekly': f'{t.week}-{t.year}',
            'monthly': f'{t.month}-{t.year}'
        }

class DateToTimestamp:
    @classmethod
    def day_tmp(cls, day):
        return str(pd.to_datetime(day, format='%d-%m-%Y').value // 10 ** 6)

    @classmethod
    def week_tmp(cls, week):
        return str(pd.to_datetime('0-' + week, format='%w-%W-%Y').value // 10 ** 6)

    @classmethod
    def month_tmp(cls, month):
        return str(pd.to_datetime(month, format='%m-%Y').value // 10 ** 6)