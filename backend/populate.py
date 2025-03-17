import json
from contextlib import contextmanager

from pymongo import MongoClient


URI = "mongodb+srv://Rayze:U2DRbVjRQSFFSNCn@zach-test.lnf1p.mongodb.net/" \
      "?retryWrites=true&w=majority&appName=Zach-Test"
database = "CS4500"

client = MongoClient(URI)
db = client['CS4500']


@contextmanager
def get_mongo_collection(collection_name: str):
    collection = db[collection_name]
    try:
        yield collection
    finally:
        pass  # No need to close the client here


def get_users_collection():
    collection_name = "Users"
    with get_mongo_collection(collection_name) as collection:
        yield collection


def main():
    # Load JSON data from a file
   # path = "fake_users_db.json"
    #with open(path, 'r') as file:
     #   users_data = json.load(file)

    # Manually call the get_users_collection function to get the MongoDB collection
    collection = db["Users"]

    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents.")

    # Iterate through the JSON data and register each user
    #for user_data in users_data:
     #   registration = UserRegistration(**user_data)
      #  try:
       #     register_new_user(registration, collection)
        #    print(f"User {registration.username} registered successfully.")
        #except DuplicateValueException as e:
         #   print(f"Duplicate value found: {e.entity_field} - {e.entity_value}")
    client.close()


if __name__ == "__main__":
    main()
