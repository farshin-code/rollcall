from flask import Flask,redirect,url_for,request,render_template,session,jsonify
from functools import wraps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import requests
from MongoCRUD import mongoDB_init,user_insert,userCheck,IDcheck,emailCheck,check_userPass,check_IDPass,getIDobjectById,getIDobjectByUser,sign_insert,query_signs
from bson.objectid import ObjectId
cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred)
mongoDB_init()
##################################### authorization middleware###############################
def isAuthorized(func):
    @wraps(func)
    def checktoken(*args,**keywords):
        try:
            # Verify the ID token
            auth.verify_id_token(session['token'],check_revoked=True)
            
            # The user is signed in
            return func(*args,**keywords)

        except Exception as e:
            
            print("error is:", e)
            return render_template('login.html')
    return checktoken

################################## Flask App #################################################
app = Flask(__name__)
app.secret_key = "AdrianaIloveU@1396"
app.config['SESSION_COOKIE_NAME'] = 'ROLLCALL123' # unique name for session , helps to be deleted after closing the site
app.permanent_session_lifetime = 3600 # 1 hour session lifetime

@app.get('/')
def login_get():
    return render_template('login.html')

@app.get('/index',endpoint='custom_index')
@isAuthorized
def index():
    return render_template('index.html')

@app.post('/login')
def login():

    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDVK1oXukoqOKvaDzYdb978nCbII-8S50c"
    
    email = request.form['user']
    password = request.form['pwd']

    userInfo = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=userInfo)
    
    if response.status_code == 200:
        
        # print(response.json())
        session['token'] = response.json()["idToken"]
        session['uid']= response.json()['localId']
        return render_template('index.html')
        #return redirect(url_for('custom_index'))
    else:
        return render_template("login.html",invalid="1")

@app.get('/logout')
def logout():
    
    auth.revoke_refresh_tokens(session['uid'])
    session.pop('token',None)

    #return render_template('login.html')
    return redirect(url_for('login_get'))

@app.post('/userinsert')
def userinsert():
    name=request.form['name']
    id=request.form['id']
    username=request.form['email']
    password=request.form['password']
    print(name,password)
    result = userCheck(int(id),username)
    print("az to server : ",result)
    if result =="id":
        return render_template('NewPerson.html',failure="1",id="1")
    if result =="username":
        return render_template('NewPerson.html',failure="1",username="1")
    
    try:
        user_insert(name,int(id),username,password)
        return render_template('NewPerson.html',success="1")
    except:
        print("error")
        return render_template("NewPerson.html",failure="1")

@app.get("/userinsert")
def new_person():
    return render_template("NewPerson.html")
    
@app.get('/sign')
def sign():
    
    # return render_template("sign.html")

    if 'token' in session:
        
        return render_template("sign.html",token="1")
    else:
        return render_template("sign.html")
@app.post('/sign')
def sign_post():
    condition = request.form['condition']
    date_time = request.form['timeStamp']
    id=''
    if len(request.form['password'])==0:
       whoRegistered = session['token']
    else:
       whoRegistered = None 

    if condition=='user':
        username = request.form['user']
        id =  getIDobjectByUser(username)

    else:
        id = request.form['id']
        id =  getIDobjectById(id)
    
    try:
        sign_insert(id,date_time,id if  whoRegistered == None else session['token'])
        return render_template('sign.html',success="1")
    except:
        print("error")
        return render_template("sign.html",failure="1")

    
@app.get("/query")
def query():
    return render_template('query.html')
 


        
@app.post("/checkpassword")
def check_pass():
    condition = request.form['condition']
    result =''
    print(condition)
    if condition == 'user':
        username = request.form['user']
        password = request.form['password']
        if check_userPass(username,password)==0:
           result = {
               'invalidUserPass' : "user"
           }
        else:
           result = {
               'invalidUserPass' : ""
           }
     
    else:
        id = request.form['id']
        password = request.form['password']
        if check_IDPass(id,password)==0:
            result = {
               'invalidUserPass' : "id"
            }
        else:
            result = {
               'invalidUserPass' : ""
            }
    return jsonify(result)

@app.post("/checkUserIdForQuery")
def check_user_id_for_query():
    request_data = request.get_json(force=True) # force=true because i did not use 'content type :application/json' in send part 
    
    if request_data['user'] == 'None' :
      
      if IDcheck(int(request_data['id']))==0:
          result = {
              'invalidUserID' : 'id',
              'id' : ""
            } 
      else:
          
          result = {
              'invalidUserID' : "",
              'id':  str(getIDobjectById(request_data['id']))
            }
    else:
        if emailCheck(request_data['user'])==0:
           result = {
              'invalidUserID' : 'user',
              'id':""
          } 
        else:
          result = {
              'invalidUserID' : "",
              "id":  str(getIDobjectByUser(request_data['user']))
          } 
    print(result) 
    return result

@app.post("/checkUserId")
def check_user_id():
    result=""
    condition = request.form['condition']
    if condition=='user':
       user = request.form['user']
       if emailCheck(user)==0:
           result = {
               'invalidUserID':"user"
           }
       else:
           result = {
               'invalidUserID' :""
           }
    else:
       id = request.form['id']
       if IDcheck(int(id))==0:
           result = {
               'invalidUserID':"id"
           }
       else:
            result = {
               'invalidUserID' :""
           } 
    return result  

@app.post('/query')
def query_result():
    
    request_data = request.get_json(force=True) # force=true because i did not use 'content type :application/json' in send part 
    start_date =request_data['start_date']  #request.form['start_date']
    end_date = request_data['end_date']
    id = request_data['id']
    result = query_signs(id,start_date,end_date,1)

    return  render_template('queryResult.html',filterResult = result)
# @app.post("/testAPI")
# def testAPI():
#     # condition = request.form['condition']
    
#     # username = request.form['user']
#     # password = request.form['password']
#     # if check_userPass(username,password)==0:
#     #     result = {
#     #         'invalidUserPass' : "True"
#     #     }
#     # else:
#     #         result = {
#     #             'invalidUserPass' : "False"
#     #     }
#     return jsonify(request.form) 
    

    
if __name__ == '__main__':
    app.run(debug=True)
