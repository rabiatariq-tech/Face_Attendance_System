from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)

db = client[DB_NAME]

collection = db[COLLECTION_NAME]


def get_all_students():
    return list(collection.find())


def find_student_by_roll(roll_no):
    return collection.find_one({"roll_no": roll_no})


def insert_student(data):
    collection.insert_one(data)


def update_attendance(roll_no, timestamp):
    collection.update_one(
        {"roll_no": roll_no},
        {"$set": {"last_attendance": timestamp}}
    )