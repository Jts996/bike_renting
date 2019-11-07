from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from . import app
from . import dataAccess as mydb


from flask import Flask,jsonify,render_template
from . import malipulate_database
from . import generateData_method
from . import visual_method
from . import Visual
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import random

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
    ret = mydb.createUser(1,data['email'],data['fname'],data['lname'],data['password'])
    if ret == False:
        output="Registration faiiled"
    else:
        output="Registration Success"
    res= { 'retstatus': output}
    return res


@app.route("/Rent")
def rent():
    if 'user_session' in session: #check user login before or not
        return render_template("rent.html")
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


#Manager pages methos  ******************:

#extract data from database or csv file.
def querydatabase(end):
    # database = 'bikehistoryall.db'
    # db = connet_datebase(database)
    # sql_query = 'SELECT * FROM alldata'
    # df = pd.read_sql(sql_query, con=db)
    # db.commit()
    # db.close()
    original_data = pd.read_csv('train.csv')
    #end = random.randint(0,10000)
    df = original_data.loc[:end]
    return df

#method for count all order in a year. It process data query from database or csv file.
def countall_hours(df):
    count_all = pd.DataFrame({'Time': np.arange(0, 24, 1), 'Count': [0] * 24})
    for i in range(df.shape[0]):
        time = int(df.loc[i, 'datetime'][11:13])
        count_all.iloc[time, 1] += int(df.loc[i, 'count'])

    startDate = df.iloc[0, 0][0:10]
    endDate = df.iloc[df.shape[0] - 1, 0][0:10]
    x = np.arange(0, 24, 1)
    y = count_all['Count']
    return x,y,startDate,endDate

#method for count all order in a year. It process data query from database or csv file.
def countall_year():
    df1 = querydatabase(4000)
    df2 = querydatabase(50000)
    count_all1 = pd.DataFrame({'Month': np.arange(0, 12, 1), 'Count': [0] * 12})
    count_all2 = pd.DataFrame({'Month': np.arange(0, 12, 1), 'Count': [0] * 12})
    for i in range(df1.shape[0]):
        month = int(df1.loc[i, 'datetime'][5:7])
        count_all1.iloc[month-1, 1] += int(df1.loc[i, 'count'])
    for i in range(df2.shape[0]):
        month = int(df2.loc[i, 'datetime'][5:7])
        count_all2.iloc[month-1, 1] += int(df2.loc[i, 'count'])

    startDate1 = df1.iloc[0, 0][0:10]
    endDate1 = df1.iloc[df1.shape[0] - 1, 0][0:10]
    startDate2 = df2.iloc[0, 0][0:10]
    endDate2 = df2.iloc[df2.shape[0] - 1, 0][0:10]

    x1 = count_all1['Month']
    y1 = count_all1['Count']
    x2 = count_all2['Month']
    y2 = count_all2['Count']

    return x1,y1,startDate1,endDate1,x2,y2,startDate2,endDate2

# render index page for manager & also page for user to select date period and download custome report
@app.route('/manager')
def showmanagerHome():
    return render_template('manager/manager.html')


@app.route('/manager/producereport', methods=['POST'])
def produecereport():
    print('ative drawing')
    req = request.get_json()
    # word = req['megs']
    # startTime = req['startTime']
    # endTime = req['endTime']
    # startTime1 = req['startTime1']
    # endTime1 = req['endTime1']
    # startTime2 = req['startTime2']
    # endTime2 = req['endTime2']
    # startTime3 = req['startTime3']
    # endTime3 = req['endTime3']
    # startTime4 = req['startTime4']
    # endTime4 = req['endTime4']
    # startTime5 = req['startTime5']
    # endTime5 = req['endTime5']
    # print(word)
    # print(startTime)
    # print(endTime)
    # Visual.produceReport(startTime,endTime,startTime1,endTime1,startTime2,endTime2,startTime3,endTime3,
    #               startTime4,endTime4,startTime5,endTime5,word)
    Visual.produceReport()
    #np.savetxt('test.txt',startTime)
    if not req:
        return jsonify({'error' : 'Missing data!'})
    return redirect(url_for('showmanagerHome'))

#render defectinfo page
@app.route('/defectinfo')
def showdefectinfo():
    return render_template('manager/defectinfo.html')


#render showshowTotalCounts/24H page
@app.route('/showTotalCounts/24H')
def showTotalCounts24H():
    df = querydatabase(500)
    x,y,startDate,endDate  = countall_hours(df)
    x = list(x)
    y = list(y)
    return render_template('manager/showTotalCounts24H.html', x=x, y=y)

#render showTotalCounts/year page
@app.route('/showTotalCounts/year')
def showTotalCountsYear():
    x1,y1,startDate1,endDate1,x2,y2,startDate2,endDate2 = countall_year()
    x1 = list(x1)
    y1 = list(y1)
    x2 = list(x2)
    y2 = list(y2)
    return render_template('manager/showTotalCountsYear.html', x1=x1, y1=y1, x2=x2, y2=y2)


