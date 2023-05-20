import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import requests

cred = credentials.Certificate("firebase-sdk.json")
id_token = ""
firebase_admin.initialize_app(cred)


def signup():
    print("----SignUP-----")
    email = input("Enter email:")
    password = input("Enter Password:")
    newuser = auth.create_user(email=email, password=password)


def login():
    global id_token
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDVK1oXukoqOKvaDzYdb978nCbII-8S50c"
    print("----Login-----")
    email = input("Enter email:")
    password = input("Enter Password:")
    userInfo = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=userInfo)
    if response.status_code == 200:
        id_token = response.json()["idToken"]

        print(f"Logged in with ID token: {id_token}")

    else:
        print("Login failed.")


# login()


def checkIflogin(id_token):
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)

        # The user is signed in
        uid = decoded_token["uid"]
        print("User is signed in with UID:", uid)

    except auth.InvalidIdTokenError:
        # The ID token is invalid or expired
        print("Invalid ID token")

    except auth.RevokedIdTokenError:
        # The ID token has been revoked
        print("Revoked ID token")

    except auth.ExpiredIdTokenError:
        # The ID token has expired
        print("Expired ID token")

    except Exception as e:
        # Handle other exceptions
        print("Error:", e)


login()
checkIflogin(id_token)
