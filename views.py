from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from . import app
from . import dataAccess as mydb


#Class holding user profile after login
class User_Session:
    def __init__(self,userid,userrole, sessionid):
        self.id = userid
        self.role = userrole
        self.sessionid = sessionid


@app.route("/",methods=['POST','GET'])
def login():
    return render_template("login.html")

@app.route("/api/dologin", methods=['POST'])
def dologin():
    
    data =request.get_json()
    email= data['emailLogin']
    password= data['password']
    valid_user=False
    (valid_user,user_role,user_id,session_id) = mydb.doLogin(email,password)

    if (valid_user == True):
        #write session into client

        u_sess = User_Session(user_id,user_role,session_id)
        session['user_session']=u_sess.__dict__

        #redirect admin home
        res= { 'token': session_id, 'retstatus': 'login success'}
    else:
        res= { 'token': '', 'retstatus': 'login failed, invalid username or password...'}
    return res


@app.route("/Profile")
def profile():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        (email,ph_num,fname,lname,addr,post_code,city,country) = mydb.getPersonalInfo(u_sess['id'])
        (card_num,card_name,exp_mm,exp_yy,cvv) = mydb.getCardInfo(u_sess['id'])
        user_prof= {'email':email,'ph_num':ph_num,'fname':fname,'lname':lname,'addr':addr,'post_code':post_code,'city':city,'country':country}
        card_info= {'card_num':card_num,'card_name':card_name,'exp_mm':exp_mm,'exp_yy':exp_yy,'cvv':cvv}
        return render_template("profile.html",userprof=user_prof,cardinfo=card_info)
    return render_template("profile.html")


@app.route("/api/updateprofile", methods=['POST'])
def updateprofile():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        data =request.get_json()
        ret = mydb.updatePersonalInfo(u_sess['id'],data['email'],data['phone'],data['fname'],data['lname'],data['address'],data['pincode'],data['city'],data['country'])
        if ret == True:
            output = "Update Success"
        else:
            output = "Update Failed"
        res= { 'retstatus': output}
        return res
    else:
        return None

@app.route("/api/updatecardinfo", methods=['POST'])
def updatecardinfo():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        data =request.get_json()
        ret = mydb.updateCardInfo(u_sess['id'],data['cnum'],data['cname'],data['exp_mm'],data['exp_yy'],data['cvv'])
        if ret == True:
            output = "Update Success"
        else:
            output = "Update Failed"
        res= { 'retstatus': output}
        return res
    else:
        return None

@app.route("/api/closeuseraccount", methods=['POST'])
def closeuseraccount():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        data =request.get_json()
        ret = mydb.deactivateUser(u_sess['id'],data['ca_email'])
        if ret == 0:
            output="Email mismatching, unable to close account"
        else:
            output="Account Closed Successfully"
        res= { 'retstatus': output}
        return res
    else:
        return None


@app.route("/api/doregistration", methods=['POST'])
def doregistration():
    data =request.get_json()
    ret = mydb.createUser(data['email'],data['fname'],data['lname'],data['password'])
    if ret == False:
        output="Registration faiiled"
    else:
        output="Registration Success"
    res= { 'retstatus': output}
    return res


@app.route("/Rent", methods=['POST','GET'])
def rent():
    if request.method=='POST':
        orderid=request.form['orderid']
        bikeid=request.form['bikeid']

        if 'user_session' in session: #check user login before or not
            (tkbike_id, tkbike_loc) = mydb.trackbikes(True)
            return render_template("rent.html",tkbikeid=tkbike_id, tkbikeloc=tkbike_loc,orderid=orderid,bikeid=bikeid)
        else:
            return redirect(url_for('login'))
    else:
        if 'user_session' in session: #check user login before or not
            (tkbike_id, tkbike_loc) = mydb.trackbikes(True)
            return render_template("rent.html",tkbikeid=tkbike_id, tkbikeloc=tkbike_loc,orderid='',bikeid='')
        else:
            return redirect(url_for('login'))


@app.route("/api/report_defect", methods=['POST'])
def report_defect():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        data =request.get_json()
        ret = mydb.createDefectReport(u_sess['id'],data['bike_id'],data['def_category'],data['def_details'])
        if ret== True:
            ret = mydb.updateBikeState(data['bike_id'],'D')
        if ret == False:
            output="Defect Report failed"
        else:
            output="Defect Report Success"
        res= { 'retstatus': output}
        return res
    else:
        return None

@app.route("/api/rent_bike", methods=['POST'])
def rent_bike():
    if 'user_session' in session: #check user session exist or not
        u_sess= session['user_session']
        data =request.get_json()
        (ret, orderid) = mydb.createOrder(u_sess['id'],data['bike_id'])
        ret = mydb.updateBikeState(data['bike_id'],'U')
        if ret == False:
            output="Rent failed"
        else:
            output="Rent Success"
        res= { 'retstatus': output, 'orderid': orderid}
        return res
    else:
        return None

@app.route("/api/return_bike", methods=['POST'])
def return_bike():
    if 'user_session' in session: #check user session exist or not
        data =request.get_json()
        (ret, amount) = mydb.settleOrder(data["order_id"])
        ret = mydb.updateBikeState(data['bike_id'],'A')
        if ret == False:
            output="Return failed"
        else:
            output="Return Success"
        res= { 'retstatus': output, 'amount': str(amount)+" pounds"}
        return res
    else:
        return None

@app.route("/Home")
def home():
    if 'user_session' in session: #check user login before or not
        user_role = session['user_session']['role']
        if user_role== 1:
            return render_template("index.html")
        elif user_role== 2:
            return redirect(url_for('adminIndex'))
        else:
            return redirect(url_for('logout'))
         
    else:
        return redirect(url_for('login'))

@app.route("/Logout/")
def logout():
    session.pop('user_session',None)
    return redirect(url_for('login'))


#admin page there******************

@app.route("/admin",methods=['POST','GET'])
def adminIndex():

    if 'user_session' in session: #check user session exist or not
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

        return render_template("/admin/index.html", dfig=dashboard, tkbikeid=tkbike_id, tkbikeloc=tkbike_loc, dfrpt=df_rpt, parkid=lststation, parkrate=lstrate, parkcolor=lstcolor)
    else:
        return redirect(url_for('login'))

@app.route("/blank",methods=['POST','GET'])
def blankPage():
    return render_template("/admin/blank.html")



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


