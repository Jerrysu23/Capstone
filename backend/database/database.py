# This file essentially acts as the "main" file for the databse, as it sets up the connections to our
# database. It creates a client, queries, etc.
#
# author: Preston Peck
# version: Sept. 3, 2024
import re
from backend.database.config import get_mongodb_uri
from pymongo.mongo_client import MongoClient
from contextlib import contextmanager

from backend.routes.user import auth as auth
from backend.schema.user import Address, UserInDB
from PIL import Image
from io import BytesIO

# setup a client to our mongoDB using the connection uri string found in config.py
client = MongoClient(get_mongodb_uri())


def get_mongo_client() -> MongoClient:
    """Returns the mongoDB client object"""

    return client


def get_users_db():
    """Returns the users database"""

    return client['users']


def get_intership_jobs_db():
    """Returns the collection in the jobs database that holds internship jobs"""

    jobs_db = client['jobs']

    return jobs_db['internship_jobs']


def get_newgrad_jobs_db():
    """Returns the collection in the jobs database that holds newgrad jobs"""

    jobs_db = client['jobs']

    return jobs_db['newgrad_jobs']


def get_saved_jobs_db():
    """Returns the collection in the jobs database that holds saved jobs for a user."""

    jobs_db = client['jobs']

    return jobs_db['saved_jobs']


def get_helper_responses_db():
    """Returns the collection in the jobs database that holds AI resume helper responses"""

    jobs_db = client['resume']

    return jobs_db['helper_responses']


def get_applications_db():
    """Returns the collection in the jobs database that holds job applications for a user."""

    jobs_db = client['jobs']

    return jobs_db['applications']


def get_cover_letters_db():
    """Returns the collection in the jobs database that holds cover letters for a user."""

    jobs_db = client['jobs']

    return jobs_db['cover_letters']


# BELOW IS ALL THE OLD DATABASE USER STUFF THAT NEEDS TO BE DELETED OR UPDATED TO USE THE NEW MONGODB DATABASE
# I'M LEAVING IT HERE JUST SO I CAN ORGANIZE OUR CODE BETTER, I AM KEEPING ANY CODE I DIDN'T WRITE MYSELF
# - PRESTON

class EntityException(Exception):
    def __init__(self, *, exception_type: str, entity_name: str, entity_id: str, status_code: int):
        self.exception_type = exception_type
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.status_code = status_code


class ValueException(Exception):
    def __init__(self, *, error: str, entity_name: str, entity_value: str, status_code: int):
        self.exception_type = "value"
        self.error = error
        self.entity_name = entity_name
        self.entity_value = entity_value
        self.status_code = status_code


class NotAuthenticatedException(Exception):
    def __init__(self, *, error: str, error_description: str, status_code: 401):
        self.error = error
        self.error_description = error_description
        self.status_code = status_code


URI = "mongodb+srv://Rayze:U2DRbVjRQSFFSNCn@zach-test.lnf1p.mongodb.net/" \
      "?retryWrites=true&w=majority&appName=Zach-Test"
database = "CS4500"

user_client = MongoClient(URI)
db = user_client['CS4500']


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


def update_user_password(collection, user, user_update):
    if auth.pwd_context.verify(user_update.oldPassword, user.get("hashed_password")):
        if auth.pwd_context.verify(user_update.newPassword, user.get("hashed_password")):
            raise EntityException(exception_type="New password cannot be the same as old password",
                                  entity_name="password",
                                  entity_id=f"new password: {user_update.newPassword}",
                                  status_code=400)
        elif user_update.newPassword == user_update.confirmPassword:
            new_hashed_password = auth.pwd_context.hash(user_update.newPassword)
            updated_password = {
                '$set': {
                    'hashed_password': new_hashed_password
                }
            }
            collection.update_one({"username": user.get("username")}, updated_password)
            return user
        else:
            raise EntityException(exception_type="New password and confirmation do not match",
                                  entity_name="password",
                                  entity_id=f"new password: {user_update.newPassword}, confirm password: "
                                            f"{user_update.confirmPassword}",
                                  status_code=400)
    else:
        raise EntityException(exception_type="Incorrect current password",
                              entity_name="password",
                              entity_id=f"current password: {user_update.oldPassword}",
                              status_code=400)


def update_user_email(collection, user, user_update_email):
    if not validate_email(user_update_email.currentEmail):
        raise EntityException(exception_type="incorrect email format",
                              entity_name="email",
                              entity_id=user_update_email.currentEmail,
                              status_code=400)

    if user.get("email") == user_update_email.currentEmail:
        if not validate_email(user_update_email.newEmail):
            raise EntityException(exception_type="incorrect email format",
                                  entity_name="email",
                                  entity_id=user_update_email.newEmail,
                                  status_code=400)
        else:
            updated_email = {
                '$set': {
                    'email': user_update_email.newEmail
                }
            }
        collection.update_one({"username": user.get("username")}, updated_email)
        return user
    else:
        raise EntityException(exception_type="incorrect current email",
                              entity_name="email",
                              entity_id=user_update_email.currentEmail,
                              status_code=400)


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False
    else:
        return True


def verify_birthday(birthday: str):
    birthday_regex = r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$'
    if not re.search(birthday_regex, birthday):
        raise EntityException(exception_type="Must be in the form MM/DD/YYYY",
                              entity_name="birthday",
                              entity_id=birthday,
                              status_code=400)


def verify_phone(phone: str):
    phone_regex = r'^\d{3}-\d{3}-\d{4}$'
    if not re.search(phone_regex, phone):
        raise EntityException(exception_type="Must be in the form XXX-XXX-XXXX",
                              entity_name="phone",
                              entity_id=phone,
                              status_code=400)


def verify_photo(photo_bytes):
    try:
        image = Image.open(BytesIO(photo_bytes))
        image.verify()  # Verify that it is, in fact, an image
        return
    except (IOError, SyntaxError):
        raise EntityException(exception_type="valid picture was not selected",
                              entity_name="photo",
                              entity_id=photo_bytes,
                              status_code=400)


def verify_ethnicity(ethnicity: str):
    ethnicity_choices = ["(Select)", "American Indian or Alaskan Native", "Asian", "Black or African Descent",
                         "Hispanic", "Native Hawaiian or Pacific Islander", "White (Caucasian)",
                         "Other"]
    if ethnicity not in ethnicity_choices:
        raise EntityException(exception_type="value entered is not a valid ethnicity",
                              entity_name="ethnicity",
                              entity_id=ethnicity,
                              status_code=400)


def verify_address(address: Address, user: UserInDB):
    valid_states = {"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
                    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
                    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
                    "WI", "WY"}
    if any(value not in [None, ''] for value in address.dict().values()) and address.line_1 == "":
        raise EntityException(exception_type="must clear all address fields",
                              entity_name="address",
                              entity_id="None",
                              status_code=400)

    if user.address.line_1 is None:
        if address.line_1 is None:
            raise EntityException(exception_type="address line 1 cannot be blank",
                                  entity_name="address line 1",
                                  entity_id="None",
                                  status_code=400)

    if address.state is not None and address.state not in valid_states and address.state != "":
        raise EntityException(exception_type="value entered is not a valid state ID",
                              entity_name="address state",
                              entity_id=address.state,
                              status_code=400)
    if address.zip != "" and re.search(r'^\d{5}$', address.zip) is None:
        raise EntityException(exception_type="Zip code must be 5 digits",
                              entity_name="address zip code",
                              entity_id=address.zip,
                              status_code=400)


def update_user_info(collection, user, user_update):
    addr = Address(line_1=user_update.line_1, line_2=user_update.line_2, city=user_update.city,
                   state=user_update.state, zip=user_update.zip)
    try:
        if user_update.birthday is not None and user_update.birthday != "":
            verify_birthday(user_update.birthday)
        if user_update.ethnicity is not None and user_update.ethnicity != "":
            verify_ethnicity(user_update.ethnicity)
            if user_update.ethnicity == "(Select)":
                user_update.ethnicity = ""
        if user_update.phone is not None and user_update.phone != "":
            verify_phone(user_update.phone)
        if addr.state == "(Select)":
            addr.state = ''
        if any(value not in [None, ""] for value in addr.dict().values()):
            verify_address(addr, user)

    except EntityException as exception:
        return exception

    updated_info = {
        '$set': {
            'name': user_update.name,
            'birthday': user_update.birthday,
            'ethnicity': user_update.ethnicity,
            'phone': user_update.phone,
            'address': addr.dict(),
            'photo': user_update.photo
        }
    }
    collection.update_one({"username": user.username}, updated_info)
    return collection.find_one({"username": user.username})
