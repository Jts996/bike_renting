from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from . import app
from . import dataAccess as mydb

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/Register",methods=['POST','GET'])
def Register():
    if request.method=='POST':
        try:
            CUST_TYPE= 1 #1 for Customer
            email=request.form['email']
            phone_number=request.form['phone_number']
            name=request.form['name']
            password=request.form['password']
            if mydb.createUser(CUST_TYPE,email,phone_number,name,password)==True:
                return render_template("Register.html", msg="Success")
            else:
                return render_template("Register.html", msg="Registration Failed")
        except:
            return render_template("resources/templates/Register.html", msg="Error!")
    else:
        return render_template("resources/templates/Register.html", msg="Welcome")

@app.route("/Login/",methods=['POST','GET'])
def Login():
    if request.method=='POST':
        try:
            email=request.form['email']
            password=request.form['password']
            user_role=-1
            session_id=""
            user_name=""
            valid_user=False
            (valid_user,user_role,user_name,session_id) = mydb.doLogin(email,password)
            if valid_user == True:
                #put user profile into session after login success
                u_sess = User_Session(email,user_name,user_role,session_id)
                session['user_session']=u_sess.__dict__
                return render_template("resources/templates/Login.html", msg="Login Success")
            else:    
                return render_template("resources/templates/Login.html", msg="Login Failed")

        except:
            return render_template("resources/templates/Login.html", msg="Error!")
    else:
        return render_template("resources/templates/Login.html", msg="Welcome")

@app.route("/Logout/")
def AppLogout():
    session.pop('user_session',None)
    return redirect(url_for('Login'))

@app.route("/Payment/")
def Payment():
    if 'user_session' in session: #check user login before or not
        return render_template("resources/templates/Payment.html")
    else:
        return redirect(url_for('Login'))

@app.route("/Rent/")
def Rent():
    if 'user_session' in session: #check user login before or not
        return render_template("resources/templates/Rent.html")
    else:
        return redirect(url_for('Login'))

@app.route("/Report_Defects/")
def Report_Defects():
    if 'user_session' in session: #check user login before or not
        return render_template("resources/templates/Report_Defects.html")
    else:
        return redirect(url_for('Login'))

@app.route("/Check_Order/")
def Check_Order():
    if 'user_session' in session: #check user login before or not
        return render_template("resources/templates/Check_Order.html")
    else:
        return redirect(url_for('Login'))

@app.route("/api/data", methods=['POST'])
def get_data():
    if request.method == "POST":
        data =request.get_json()
    output= 'I got it ..' + data['output']
    res= { 'gotit': output}
    return res

#admin page there******************

@app.route("/logout")
def AdminLogout():
    session.pop('user_session',None)
    return redirect(url_for('AdminLogin'))

@app.route("/")
def AdminLogin():
    return render_template("login.html")

@app.route("/admin",methods=['POST','GET'])
def AdminIndex():

    if 'user_session' in session: #check user session exist or not
        my_sess= session['user_session']

        dashboard= mydb.getDashBoardFig()
        (tkbike_id, tkbike_loc) = mydb.trackbikes()
        (df_rpt) = mydb.showDefectReport()
        (parking_status)= mydb.showBikeStations()
        lststation= list(parking_status['station_id'])
        lstrate= list(parking_status['occ_rate'])
        lstcolor= []

        for i in range(0,len(lstrate)):
            if lstrate[i] >= 80:
                lstcolor.append("rgba(216,56,7,1)")
            elif lstrate[i] <=20:
                lstcolor.append("rgba(244,233,76,1)")
            else:
                lstcolor.append("rgba(2,117,216,1)")

        return render_template("index.html", dfig=dashboard, tkbikeid=tkbike_id, tkbikeloc=tkbike_loc, dfrpt=df_rpt, parkid=lststation, parkrate=lstrate, parkcolor=lstcolor)
    else:
        return redirect(url_for('AdminLogin'))

@app.route("/blank",methods=['POST','GET'])
def blankPage():
    return render_template("resources/templates/admin/blank.html")


@app.route("/api/login", methods=['POST'])
def login():
    if request.method == "POST":
        data =request.get_json()
    email= data['email']
    password= data['password']
    valid_user=False
    (valid_user,user_role,user_name,session_id) = mydb.doLogin(email,password)
    #user_session={'id':session_id,'name':user_name,'role':user_role}
    
    if (valid_user == True) and (user_role > 1):
        #write session into client

        u_sess = User_Session(email,user_name,user_role,session_id)
        session['user_session']=u_sess.__dict__

        #redirect admin home
        res= { 'token': session_id, 'result': 'login success'}
    else:
        res= { 'token': '', 'result': 'login failed, invalid username or password...'}
    return res

@app.route("/api/changeDefectStatus", methods=['POST'])
def changeDfStatus():
    if request.method == "POST":
        data =request.get_json()
    id= data['id']
    newdfStatus= data['newdfStatus']
    ok = mydb.updateDefectStatus(id,newdfStatus)
    
    if (ok == True):
        res= { 'result': 'ok'}
    else:
        res= { 'result': 'nok'}
    return res


#Class holding user profile after login
class User_Session:
    def __init__(self,usermail, username, userrole, sessionid):
        self.email = usermail
        self.name = username
        self.role = userrole
        self.sessionid = sessionid

