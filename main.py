from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deta import Deta

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

try:
    deta = Deta("your API Key")
    db = deta.Base("simple_db")
except:
    print('Error initializing the database')

# get requests -------------------------------------------->
@app.get('/')
def home_page():
    return {"home": "Welcome to FASTAPI created by Mukal Dadhwal"}

@app.get('/about')
def about_page():
    return {"about": "I am a 18 year old aspiring python developer"}

@app.get('/get-user/{user_name}')
def get_user(user_name: str):
    try:
        user = db.fetch({"name": user_name}).items[0];
        print(user)
    except:
        return {"key": "not found"}
    return {"user name": user["name"], "email id": user["email"]}


# post requests -------------------------------------------->
@app.post('/add-user/')
def add_user(user_name: str, email: str):
    try:
        db.insert({
            "name": user_name,
            "email": email,
        })
    except:
        return {"error": "Error putting the data"}
    return {user_name: "added",}


@app.delete('/delete-user/')
def delete_user(user_name: str):
    try:
        firstItem = db.fetch({"name": user_name}).items[0]
        key = firstItem["key"]
        db.delete(key)
    except:
        return {"error": "Error in deleting the user"}
    return {user_name: "deleted"}