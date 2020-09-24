import pymongo

client = pymongo.MongoClient(
   f"mongodb://127.0.0.1:27017/")
db = client['ExamBuilder']



