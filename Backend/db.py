from models import check_password_hash
from models import User
from pymongo import MongoClient

# load_dotenv()
# # TODO: check the url and setting with devops team
# mongo_username = os.getenv('MONGO_USERNAME')
# mongo_password = os.getenv('MONGO_PASSWORD')

client = MongoClient('localhost', 27017)
db = client['Hackathon']

users_collection = db['users']
nlp_collection = db['nlp_url']
media_collection = db['media']
audio_collection = db['audio']
doc_collection = db['doc']
search_collection = db['search']


def add_media(document):
    media_collection.insert_one(document)

def get_document_by_url(url):
    return nlp_collection.find_one({'url': url})


def insert_document(document):
    nlp_collection.insert_one(document)


def update_document(url, new_data):
    nlp_collection.update_one({'url': url}, {'$set': new_data})

def add_nlp_url(url):
    result = nlp_collection.insert_one({'url':url})

def add_user(user):
    user_data = {
        "username": user.username,
        "email": user.email,
        "password_hash": user.password_hash,
    }
    result = users_collection.insert_one(user_data)
    user.set_id(result.inserted_id)


def find_user_by_email(email):
    return users_collection.find_one({"email": email})


def check_user_password(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False


def user_from_dict(user_dict):
    user = User(
        username=user_dict['username'],
        email=user_dict['email'],
        password=user_dict['password_hash'],
    )
    user.set_id(user_dict['_id'])
    return user


