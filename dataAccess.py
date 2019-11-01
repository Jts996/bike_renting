import sqlite3
from . import app  
from flask import g
import numpy as np
import pandas as pd

#variable contains db for system used
PRJ_DB = "bikeRenting.db"

#db connection stored and shared within request context
def get_db():
    db=getattr(g,"_bikedb",None)
    if db is None:
        db= g._bikedb= sqlite3.connect(PRJ_DB)
    return db
#release connection resource after request context
@app.teardown_appcontext
def close_connection(exception):
    db=getattr(g,'_bikedb',None)
    if db is not None:
        db.close

#**********************
#*****Registration*****
#**********************

#create user account
def createUser(user_role,email,phone_no,name,password):
    try:
        current_date = ""
        cur= get_db().cursor()
        cur.execute("INSERT INTO users (email,phone_number,name,password,role_id,create_date) VALUES (?,?,?,?,?,?)", (email,phone_no,name,password,user_role,current_date))
        get_db().commit()
        return True
    except:
        print("createUser error")
        get_db().rollback()
        return False

#update user password
#present valid old password before update or
#isreset is true, no need to present old password
def updateUserPassword(email,oldpassword,newpassword,isreset=False):
    return True

#**********************
#*****Login       *****
#**********************
#Login, return user role and session no. after valid password check
def doLogin(email,password):
    try:
        cur= get_db().cursor()
        cur.execute("SELECT role_id, name, password FROM users WHERE email = ?", [email])
        row= cur.fetchone()
        role_id= row[0]
        name= row[1]
        secret= row[2]
        if password == secret:
            session_ran = np.random.randint(0,10,7)
            session_no=""
            for unit in session_ran:
                session_no= session_no + str(unit)
            return (True, role_id, name, session_no)
        else:
            return (False,-1,'','')
    except:
        print("doLogin error")
        return (False,-1,'','') 

#+++++++++++Customer+++++++++++

#**********************
#*****Rent/Return *****
#**********************

#Create order releted to rent action, return order_id,status set INUSE
def createOrder(user_id,bike_id,startDateTime):
    return True

#Update order releted to return action, to complete a order transaction, status set AVAILABLE
def updateOrder(order_id,endDateTime,amount):
    return True

#Update bike location on return action, 
def updateBikeParkingLoc(bike_id,parked_bike_stationId):
    return True

#Update bike location from GPS
def updateBikeLoc(bike_id,lat,long):
    return True

#Return bike status and location information
#Status: DEFECT/AVALIABLE/INUSE
def getBikeStatus(bike_id):
    return True

#**********************
#*****Charge/Pay  *****
#**********************

#Create one if a not existing in user account
#Deduce amount from user account, isTopup is false
#Top up acccount balance, for isTopup is true
def updateAccountBalance(user_id,amount,cardinfo,isTopup=True):
    return True

#**********************
#*****Report Defect****
#**********************

#Create Defect incident
#Status set as DEFECT
def createDefectReport(user_id,bike_id,category,details):
    return True

#+++++++++++Operator+++++++++++

#**********************
#*****Track bikes  ****
#**********************

#Return list of bikes with loc. info and status
def trackbikes():
    try:
        bikeid= []
        locs=[]
        cur= get_db().cursor()
        cur.execute("SELECT bike_id, loc_lat, loc_long FROM bikes")
        for row in cur.fetchall():
            bikeid.append(row[0])
            locs.append({'lat': row[1] , 'lng': row[2] })

        return (bikeid,locs)
    except:
        print("trackbikes error")
        return None

#**********************
#*****Repair Defect****
#**********************

#Show dash board
#Status as DEFECT
def getDashBoardFig():
    try:
        results= {}
        cur= get_db().cursor()
        cur.execute("SELECT status, count(*) FROM bikes GROUP BY status")
        for row in cur.fetchall():
            results[row[0]]= row[1]

        cur.execute("SELECT count(*) from defect_report WHERE status <> 'DF'")
        count= cur.fetchone()
        results['T']=count[0]

        return results
    except:
        print("showDashBoardFig error")
        return None 

#Show outstanding defects
#Status as DEFECT
def showDefectReport():
    try:
        cur= get_db().cursor()
        cur.execute("""SELECT D.report_id, U.email, D.bike_id, D.category, 
        D.details, D.report_datetime, D.status FROM defect_report D, 
        users U on D.user_id = U.user_id where status <> 'DF'""")
        rows=  cur.fetchall()

        return (rows)
    except:
        print("showDefectReport error")
        return None

#Change defect status
#Status as RD-REP_DEFECT/RI-REP_INVESTIGATE/DF-FIXED
def updateDefectStatus(id, new_status):
    try:
        cur= get_db().cursor()
        cur.execute("UPDATE defect_report SET status=? where report_id = ?", (new_status, id))
        get_db().commit()
        return True
    except:
        print("updateDefectStatus")
        get_db().rollback()
        return False

#**********************
#*****Move Bikes   ****
#**********************


#Show bikes that require move action, bikes station lack of bike or overcrowded
def showBikeStations():
    try:
        cur= get_db().cursor()

        sql1="""SELECT count(*) as 'num_bikes', parked_bike_station FROM bikes WHERE status <> 'U' 
        GROUP BY parked_bike_station"""

        sql2="SElECT station_id, post_code, loc_lat, loc_long, bike_rack_number FROM bike_stations"
        bikescountfrm= pd.read_sql_query(sql1,get_db())
        stationfrm= pd.read_sql_query(sql2,get_db())

        resultset= pd.merge(stationfrm,bikescountfrm,how='outer',left_on='station_id',right_on='parked_bike_station')
        resultset['occ_rate']=round(resultset['num_bikes']/resultset['bike_rack_number']*100,2)
        return (resultset)
    except:
        print("showBikeStations error")
        return None