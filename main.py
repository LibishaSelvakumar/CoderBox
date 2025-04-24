from flask import Flask, render_template, request, Response, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import win32com.client 
import pythoncom
import cv2
import string
import random
import numpy as np
import time
import datetime
import mysql.connector
import math
from flask_socketio import SocketIO, emit, join_room, leave_room
from engineio.payload import Payload
Payload.max_decode_packets = 200
from werkzeug.utils import secure_filename
from flask import request as flask_request


app = Flask(__name__)
app.secret_key = "abcdef"

app.config['UPLOAD_FOLDER'] = 'C:/Users/gamin/Desktop/coderbox/static/resume'  # Folder to store songs

socketio = SocketIO(app, async_mode='eventlet')  # Explicitly set async_mode


_users_in_room = {} # stores room wise user list
_room_of_sid = {} # stores room joined by an used
_name_of_sid = {} # stores display name of users


app.config['UPLOAD_FOLDER1'] = 'C:/Users/gamin/Desktop/coderbox/static/profile'

app.config['UPLOAD_FOLDER3'] = 'C:/Users/gamin/Desktop/coderbox/static/poster'# Folder to store songs


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    database="coderbox"
)


@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('index.html')

@app.route('/profile_view', methods=['POST', 'GET'])
def profile_view():

    username=session.get('username')

    cursor=mydb.cursor(buffered=True)
    cursor.execute("Select * from profile where username=%s", (username, ))
    data=cursor.fetchone()
    cursor.close()

    return render_template('profile_view.html', data=data)


@app.route('/admin',methods=['POST','GET'])
def admin():
    
    
    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'user'
            msg="success"
            return redirect(url_for('pro'))
        else:
            msg="fail"
    
        

    return render_template('admin.html',msg=msg)


@app.route('/login',methods=['POST','GET'])
def login():
    
    
    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM seeker WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'user'
            msg="success"
            return redirect(url_for('profile'))
        else:
            msg="fail"
    
        

    return render_template('login.html',msg=msg)


@app.route('/login1',methods=['POST','GET'])
def login1():
    
    
    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM recruiter WHERE username = %s AND password = %s AND status=1', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'user'
            msg="success"
            return redirect(url_for('post'))
        else:
            msg="fail"
    
        

    return render_template('login1.html',msg=msg)


@app.route('/register',methods=['POST','GET'])
def register():
    
    msg=""
    if request.method=='POST':

        name=request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        address=request.form['address']
        username=request.form['username']
        password=request.form['password']

        
        now = datetime.datetime.now()
        date_join=now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM seeker where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM seeker")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO seeker(id, name, email, address, mobile, username, password, date_join) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, email, address, mobile, username, password, date_join)
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
            return redirect(url_for('login'))
            mycursor.close()
        else:
            msg="fail"

    return render_template('register.html', msg=msg)


@app.route('/register1',methods=['POST','GET'])
def register1():
    
    
    msg=""
    st = ""
    mess = ""
    mobile = ""
    username=""
    password=""
    name=""
    if request.method=='POST':

        name=request.form['name']
        company=request.form['company']
        company_type=request.form['company_type']
        email=request.form['email']
        mobile=request.form['mobile']
        location=request.form['location']
        username=request.form['username']
        password=request.form['password']

        
        now = datetime.datetime.now()
        date_join=now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM recruiter where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM recruiter")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO recruiter(id, name, company, company_type, email, location, mobile, username, password, date_join) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, company, company_type, email, location, mobile, username, password, date_join)
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
            mycursor.close()
            return redirect(url_for('login1'))
        else:
            msg="fail"

    return render_template('register1.html', msg=msg, st=st, mess=mess)



@app.route('/post',methods=['POST','GET'])
def post():
    
    
    msg=""
    username=session.get('username')
    cursor=mydb.cursor()
    cursor.execute("Select * from recruiter where username=%s", (username, ))
    dat=cursor.fetchone()
    cursor.close()
    name=dat[1]
    company=dat[2]
    company_type=dat[3]
    email=dat[4]
    mobile=dat[6]
    location=dat[5]
    if request.method=='POST':

        job_title=request.form['job_title']
        job_type=request.form['job_type']
        salary=request.form['salary']
        description=request.form['description']
        file = request.files['job_poster']
        if file and allowed_file(file.filename):
            # Generate a random filename
            random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER3'], random_filename)

            # Save the file
            file.save(filepath)
            now = datetime.datetime.now()
            date_join=now.strftime("%d-%m-%Y")

        
        
            mycursor = mydb.cursor()
            mycursor.execute("SELECT max(id)+1 FROM posts")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO posts(id, name, company, company_type, email, location, mobile, job_title, job_type, salary, descrip, filename, date_join, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, company, company_type, email, location, mobile, job_title, job_type, salary, description, random_filename, date_join, username)
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
            mycursor.close()
            return redirect(url_for('my_posts'))
        else:
            msg="fail"

    return render_template('post.html', msg=msg)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    msg = ""
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM seeker WHERE username=%s", (username,))
    dat = cursor.fetchone()
    cursor.close()
    
    name = dat[1]
    email = dat[3]
    mobile = dat[2]
    location = dat[4]
    
    if request.method == 'POST':
        job_category = request.form['job_category']
        skills = request.form['skills']
        experience = request.form['experience']
        
        file = request.files['resume']
        if file and allowed_file(file.filename):
            # Generate a random filename
            random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".pdf"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], random_filename)
            file.save(filepath)
            
            file1 = request.files['profile_picture']
            if file1 and allowed_file(file1.filename):
                random_filename1 = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".jpg"
                filepath1 = os.path.join(app.config['UPLOAD_FOLDER1'], random_filename1)
                file1.save(filepath1)
                
                now = datetime.datetime.now()
                date_join = now.strftime("%d-%m-%Y")

                mycursor = mydb.cursor()
                mycursor.execute("SELECT max(id)+1 FROM profile")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                
               
                sql = """INSERT INTO profile(id, name, email, location, mobile, job_category, skills, experience, resume, profile, date_join, username) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (maxid, name, email, location, mobile, job_category, skills, experience, random_filename, random_filename1, date_join, username)
                    
                    
                mycursor.execute(sql, val)
                mydb.commit()
                msg = "success"
                mycursor.close()
                return redirect(url_for('profile_view'))
            else:
                msg = "Profile picture file type not allowed."
    
    return render_template('profile.html', msg=msg)

  

@app.route('/my_posts', methods=['POST', 'GET'])
def my_posts():

    username=session.get('username')

    cursor=mydb.cursor()
    cursor.execute("Select * from posts where username=%s", (username, ))
    data=cursor.fetchall()
    cursor.close()

    return render_template('my_posts.html', data=data)


#####################################################################################################################################



import pytesseract
from PIL import Image
import cv2
import os
import re

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Predefined job titles to compare
JOB_TITLES = ["UI/UX Designer", "Video Editor", "Digital Marketing", "Graphic Designer", "Content Creator"]

def extract_full_text(image_path):
    """Extracts full text from an image using OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve OCR accuracy
    processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Extract text
    text = pytesseract.image_to_string(processed, config='--psm 6 --oem 3')
    return text.strip()

def match_job_titles(extracted_text):
    """Matches extracted text with predefined job titles."""
    matched_titles = []
    for job_title in JOB_TITLES:
        if job_title.lower() in extracted_text.lower():  # Case-insensitive partial match
            matched_titles.append(job_title)

    return matched_titles

@app.route('/view_profiles', methods=['GET'])
def view_profiles():
    try:
        poster_path = "D:/coderbox/static/poster/PbXu7dEQDq.jpg"
        
        # Extract full text from image
        extracted_text = extract_full_text(poster_path)
        print(f"Extracted Text: {extracted_text}")  # Debugging Output
        print(f"Extracted Text:\n{extracted_text}")

        # Match job titles
        matched_job_titles = match_job_titles(extracted_text)
        print(f"Matched Job Titles: {matched_job_titles}")  # Debugging Output

        profiles = []
        if matched_job_titles:
            cursor = mydb.cursor()
            query = "SELECT * FROM profile WHERE skills LIKE %s"
            cursor.execute(query, ('%' + matched_job_titles[0] + '%',))
            profiles = cursor.fetchall()
            cursor.close()

        return render_template('view_profiles.html', job_titles=matched_job_titles, profiles=profiles)

    except Exception as e:
        return f"Error processing post: {e}"



################################################################################################################################

from flask import jsonify, request

@app.route('/search_profiles', methods=['POST', 'GET'])
def search_profiles():
    row_id = request.form.get('row_id', '')
    post_id = request.args.get('post_id')
    job_title = request.args.get('job_title', '')

    # Capture voice search input
    voice_search = request.form.get('search', '')

    cursor = mydb.cursor(dictionary=True)

    if voice_search:
        cursor.execute("SELECT * FROM profile WHERE skills LIKE %s", ('%' + voice_search + '%',))
    elif row_id:
        cursor.execute("SELECT * FROM profile WHERE skills LIKE %s", ('%' + row_id + '%',))
    else:
        cursor.execute("SELECT * FROM profile WHERE skills LIKE %s", ('%' + job_title + '%',))

    profiles = cursor.fetchall()
    cursor.close()

    # Store results in session
    session['search_results'] = profiles

    return render_template('search_profiles.html', profiles=profiles, post_id=post_id)



@app.route('/request1', methods=['POST', 'GET'])
def request1():
    msg = ""
    username = session.get('username')
    postID = request.args.get('post_id')
    pro_id = request.args.get('pro_id')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM posts WHERE id=%s", (postID,))
    dat = cursor.fetchone()
    cursor.close()

    postt_id=dat[0]
    post_name=dat[1]
    company=dat[2]
    company_type=dat[3]
    post_mobile=dat[4]
    post_email=dat[5]
    post_location=dat[6]
    job_title=dat[7]
    job_type=dat[8]
    salary=dat[9]
    descrip=dat[10]
    filename=dat[11]
    date_join=dat[12]
    post_username=dat[13]

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM profile WHERE id=%s", (pro_id,))
    data = cursor.fetchone()
    cursor.close()

    profile_id=data[0]
    name=data[1]
    email=data[2]
    location=data[4]
    mobile=data[3]
    job_category=data[5]
    skills=data[6]
    experience=data[7]
    resume=data[8]
    profile=data[9]
    
    pro_username=data[11]

    now = datetime.datetime.now()
    date_join1=now.strftime("%d-%m-%Y")

        
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM request")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    sql = "INSERT INTO request(id, postt_id, post_name, company, company_type, post_email, post_location, post_mobile, job_title, job_type, salary, descrip, filename, date_join, post_username, profile_id, name,email, mobile ,location, job_category, skills, experience, resume, profile, date_join1, pro_username, action) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (maxid, postt_id, post_name, company, company_type, post_email, post_location, post_mobile, job_title, job_type, salary, descrip, filename, date_join, post_username, profile_id, name,email, mobile ,location, job_category, skills, experience, resume, profile, date_join1, pro_username, '1')
    mycursor.execute(sql, val)
    mydb.commit()

    msg="success"
    mycursor.close()
    return redirect(url_for('request_list'))



@app.route('/request_list', methods=['POST', 'GET'])
def request_list():
    msg = ""
    username = session.get('username')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM request WHERE post_username=%s", (username,))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('request_list.html', data1=data1)

@app.route('/update_request_status')
def update_request_status():
    aid = request.args.get("aid")
    status = request.args.get("status")

    cursor = mydb.cursor()
    cursor.execute("UPDATE request SET action=%s WHERE id=%s", (status, aid))
    mydb.commit()
    cursor.close()

    return redirect(url_for('request'))



@app.route('/pro', methods=['POST', 'GET'])
def pro():

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM recruiter")
    dat = cursor.fetchall()
    cursor.close()


    act=request.args.get("act")

    if act=="ok":
        rid=request.args.get("rid")
        cursor=mydb.cursor()
        cursor.execute(" UPDATE recruiter SET status=1 where id=%s", (rid, ))
        print("Data Updated Successfully")
        mydb.commit()
        return redirect(url_for('pro'))

    if act=="no":
        rid=request.args.get("rid")
        cursor=mydb.cursor()
        cursor.execute(" UPDATE recruiter SET status=2 where id=%s", (rid, ))
        print("Data Updated Successfully")
        mydb.commit()
        return redirect(url_for('pro'))


    return render_template('pro.html', data1=dat)
    


@app.route('/pro1', methods=['POST', 'GET'])
def pro1():

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM seeker")
    dat4 = cursor.fetchall()
    cursor.close()


    return render_template('pro1.html', data1=dat4)

from flask import Flask, request, jsonify



@app.route('/update_profile', methods=['POST'])
def update_profile():

    username=session.get('username')
    data = request.json
    # Process and update the database with new values
    # Assuming you have a database connection and `users` table
    try:
        
        cursor = mydb.cursor()
        sql = """UPDATE profile SET name=%s, email=%s, mobile=%s, location=%s, 
                 skills=%s, experience=%s WHERE username=%s"""
        cursor.execute(sql, (data['name'], data['email'], data['mobile'], 
                             data['location'], data['skills'], data['experience'], username))
        mydb.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    if 'username' in session:
        username = session['username']
        try:
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM profile WHERE username = %s", (username,))
            mydb.commit()
            session.clear()  # Log the user out
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "Not logged in"})



    


@app.route('/update_request', methods=['GET'])
def update_request():
    action = request.args.get('action')
    request_id = request.args.get('request_id')

    # Define allowed actions
    valid_actions = {
        'accept': 2,
        'reject': 3,
        'process': 4,
        'complete': 5
    }

    if action not in valid_actions:
        return "Invalid action", 400

    # Update the request status
    cursor = mydb.cursor()
    cursor.execute("UPDATE request SET action=%s WHERE id=%s", (valid_actions[action], request_id))
    mydb.commit()

    return redirect('/user_request')

@app.route('/pro2', methods=["GET", "POST"])
def pro2():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM request")
    requests = cursor.fetchall()
    return render_template('pro2.html', requests=requests)



@app.route('/user_request', methods=['GET'])
def user_request():
    username = session.get('username')
    if not username:
        return redirect('/login')  # Redirect to login if not logged in

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM request WHERE pro_username=%s", (username,))
    data1 = cursor.fetchall()
    cursor.close()

    return render_template('user_request.html', data1=data1)


@app.route("/call", methods=["GET", "POST"])
def call():

    aid=request.args.get("aid")
    if request.method == "POST":
        room_id = request.form['room_id']
        cursor = mydb.cursor()
        cursor.execute("update request set link=%s where id=%s",(room_id, aid))
        mydb.commit()
        
        return redirect(url_for("entry_checkpoint", room_id=room_id, aid=aid))

    return render_template("call.html")

@app.route("/room/<string:room_id>/")
def enter_room(room_id):
    act=request.args.get("act")
    
    
    if room_id not in session:
        return redirect(url_for("entry_checkpoint", room_id=room_id))
    
    return render_template("chatroom.html", room_id=room_id, display_name=session[room_id]["name"], mute_audio=session[room_id]["mute_audio"], mute_video=session[room_id]["mute_video"])

@app.route("/room/<string:room_id>/checkpoint/", methods=["GET", "POST"])
def entry_checkpoint(room_id):
    

    username=""
    
    if request.method == "POST":
        mute_audio = request.form['mute_audio']
        mute_video = request.form['mute_video']
        session[room_id] = {"name": username, "mute_audio":mute_audio, "mute_video":mute_video}
        return redirect(url_for("enter_room", room_id=room_id))

    return render_template("chatroom_checkpoint.html", room_id=room_id)

@socketio.on("connect")
def on_connect():
    sid = request.sid
    print("New socket connected ", sid)
    

@socketio.on("join-room")
def on_join_room(data):
    sid = request.sid
    room_id = data["room_id"]
    display_name = session[room_id]["name"]
    
    # register sid to the room
    join_room(room_id)
    _room_of_sid[sid] = room_id
    _name_of_sid[sid] = display_name
    
    # broadcast to others in the room
    print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
    emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)
    
    # add to user list maintained on server
    if room_id not in _users_in_room:
        _users_in_room[room_id] = [sid]
        emit("user-list", {"my_id": sid}) # send own id only
    else:
        usrlist = {u_id:_name_of_sid[u_id] for u_id in _users_in_room[room_id]}
        emit("user-list", {"list": usrlist, "my_id": sid}) # send list of existing users to the new member
        _users_in_room[room_id].append(sid) # add new member to user list maintained on server

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    room_id = _room_of_sid[sid]
    display_name = _name_of_sid[sid]

    print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    _users_in_room[room_id].remove(sid)
    if len(_users_in_room[room_id]) == 0:
        _users_in_room.pop(room_id)

    _room_of_sid.pop(sid)
    _name_of_sid.pop(sid)

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("data")
def on_data(data):
    sender_sid = data['sender_id']
    target_sid = data['target_id']
    if sender_sid != request.sid:
        print("[Not supposed to happen!] request.sid and sender_id don't match!!!")

    if data["type"] != "new-ice-candidate":
        print('{} message from {} to {}'.format(data["type"], sender_sid, target_sid))
    socketio.emit('data', data, room=target_sid)








@app.route('/logout')
def logout():
    
    session.clear()
    print("Logged out successfully", 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
