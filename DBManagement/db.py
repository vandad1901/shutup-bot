from pymongo import MongoClient
from pymongo.database import Database

from common import database_url

database: Database = MongoClient(database_url).shutup
