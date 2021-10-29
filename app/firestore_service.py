import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import initialize_app

credential = credentials.ApplicationDefault()
initialize_app(credential)

db = firestore.client()

def get_users():
    return db.collection('Users').get()

def get_user(user_id):
    return db.collection('Users').document(user_id).get()

def put_user(user_data):
    user_ref = db.collection('Users').document(user_data.username)
    user_ref.set({'password': user_data.password})

def get_todos(user_id):
    return db.collection('Users').document(user_id)\
        .collection('todos').get()

def put_todo(user_id, description):
    todo_collection_ref = db.collection('Users').document(user_id).collection('todos')
    todo_collection_ref.add({'descripcion': description, 'done':False})

def delete_todo(user_id, todo_id):
    todo_ref = get_todo_ref(user_id=user_id, todo_id=todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = get_todo_ref(user_id=user_id, todo_id=todo_id)
    todo_ref.update({'done': todo_done})

def get_todo_ref(user_id, todo_id):
    return db.document('Users/{}/todos/{}'.format(user_id, todo_id))
