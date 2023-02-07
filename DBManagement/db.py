from pymongo import MongoClient

from common import database_url

database = MongoClient(database_url).shutup
