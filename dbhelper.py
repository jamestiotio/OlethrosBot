import dateparser
import json
import pymongo
import botinfo
from bson import json_util

class DBHelper:
    def __init__(self):
        self.client = pymongo.MongoClient(botinfo.MONGODB_ATLAS_CONNECTION_STRING)
        self.db = self.client.olethrosbot

        self.class_list = self.db.class_list
        self.reminder_list = self.db.reminder_list

    def get_class_list(self):
        return [document for document in self.class_list.find({})]

    def parse_time(self, time):
        parsed_time = dateparser.parse(time)
        return parsed_time

    def time_string(self, time):
        string = time.strftime("%m/%d/%Y, %H:%M:%S")
        return string

    def add_reminder(self, user_id, time, reminder):
        # Work in progress
        pass

    def check_reminder_list(self, chat_id):
        # Work in progress
        pass

    def delete_reminder(self, user_id, time, reminder):
        # Work in progress
        pass

    def remind(self, time: str, reminder: str):
        # Work in progress
        pass
