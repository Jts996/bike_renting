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


# !!!!!!!!!!!!!!!!!!!!!! THIS METHODIS NOT USED
#update user password
#present valid old password before update or
#isreset is true, no need to present old password
def updateUserPassword(email,oldpassword,newpassword,isreset=False):
    try:
        cur = get_db().cursor()
        cur.execute("UPDATE users SET password = newpassword  WHERE email = targetemail and password = oldpassword")
        get_db().commit()
    except:
        print("Fail to update Password")
        return False

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

# **********************
# * UpdatePersonalInfo *
# **********************
# Update the personal info-checked-need exception modify


def updatePersonalInfo(user_id,email,phone_number,name,password):
    try:
        cur = get_db().cursor()
        cur.execute(
        "UPDATE users SET email = '%s', phone_number = '%d', name = '%s', password = '%s'  where user_id = %d" % (
        email, phone_number, name, password, user_id))
        get_db().commit()
    except:
        print("Fail to update personal info")
        return False

# Update payment card info


def updateCardInfo(user_id,card_num,card_name,exp_mm,exp_yy,cvv):
    def updateCardInfo(user_id, card_num, card_name, exp_mm, exp_yy, cvv):
        try:
            cur = get_db().cursor()
            cur.execute(
                "UPDATE accounts SET card_num = '%s', card_name = '%s', exp_mm = '%s', exp_yy = '%s', cvv = '%s' WHERE user_id = '%d'" % (
                card_num, card_name, exp_mm, exp_yy, cvv, user_id))
            get_db().commit()
        except:
            print("Fail to update card info")
            return False


# Send default card info to page


def sendCardInfo(user_id):
    def sendCardInfo(user_id):
        try:
            cur = get_db().cursor()
            cur.execute("SELECT card_num,card_name,exp_mm,exp_yy,cvv FROM accounts WHERE user_id = '%d'" % user_id)
            result = cur.fetchall()
            card_num = result[0][0]
            card_name = result[0][1]
            exp_mm = result[0][2]
            exp_yy = result[0][3]
            cvv = result[0][4]
            return card_num, card_name, exp_mm, exp_yy, cvv
        except:
            print("Fail to return")
            return False


#**********************
#*****Rent/Return *****
#**********************

#Create order releted to rent action, return order_id,status set INUSE
def createOrder(user_id,bike_id,startDateTime):
    try:
        import time
        cur = get_db().cursor()
        time = int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        order = time + user_id
        cur.execute("INSERT INTO orders (order_id, user_id, bike_id, start_datetime, end_datetime, amount) VALUES (?, ?, ?, ?, ?, ?)",(order, user_id, bike_id,startDateTime, 0, 0))
        get_db().commit()
    except:
        print("Fail to create order!")
        return False

#Update order releted to return action, to complete a order transaction, status set AVAILABLE
def updateOrder(order_id,endDateTime,amount):
    try:
        import time
        import datetime
        cur = get_db().cursor()
        cur.execute("SELECT start_datetime FROM orders WHERE order_id = '%d'" % order_id)
        start_datetime = str(cur.fetchall()[0][0])
        end_datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

        s_year = int(start_datetime[:4])
        s_month = int(start_datetime[4:6])
        s_day = int(start_datetime[6:8])
        s_hour = int(start_datetime[8:10])
        s_min = int(start_datetime[10:12])
        start_time = datetime.datetime(s_year, s_month, s_day, s_hour, s_min)

        e_year = int(end_datetime[:4])
        e_month = int(end_datetime[4:6])
        e_day = int(end_datetime[6:8])
        e_hour = int(end_datetime[8:10])
        e_min = int(end_datetime[10:12])
        end_time = datetime.datetime(e_year, e_month, e_day, e_hour, e_min)

        sum_minute = (end_time - start_time).seconds/60
        amount = int(sum_minute/30 * 1.5)

        cur.execute("UPDATE orders SET end_datetime = '%s',amount = '%f' WHERE order_id = '%d'" % (end_datetime,amount,order_id))
        get_db().commit()
    except:
        print("Fail to calculate the time")
        return False
    return True

#Update bike location on return action, 
def updateBikeParkingLoc(bike_id,parked_bike_stationId):
    try:
        cur = get_db().cursor()
        cur.execute("UPDATE bikes SET parked_bike_station = '%d' WHERE bike_id = '%d'" % (parked_bike_stationId,bike_id))
        get_db().commit()
        return True
    except:
        print("Fail to update the bike parking loc!")
        return False

#Update bike location from GPS
def updateBikeLoc(bike_id,lat,long):
    try:
        cur = get_db().cursor()
        cur.execute("UPDATE bikes SET loc_lat='%f', loc_long='%f' WHERE bike_id ='%d'" % (lat, long, bike_id))
        get_db().commit()
        return True
    except:
        print("Fail to update bike location")
        return False

#Return bike status and location information
#Status: DEFECT/AVALIABLE/INUSE
def getBikeStatus(bike_id):
    try:
        cur = get_db().cursor()
        cur.execute("SELECT status FROM bikes where bike_id = '%d'" % bike_id)
        status = cur.fetchall()[0][0]
        return bike_id , status
    except:
        print("Bike_id does not exist!")
        return False

#**********************
#*****Charge/Pay  *****
#**********************

#Create one if a not existing in user account
#Deduce amount from user account, isTopup is false
#Top up acccount balance, for isTopup is true
def updateAccountBalance(user_id,amount,cardinfo,isTopup=True):
    def updateAccountBalance(user_id, amount, cardinfo, isTopup=True):
        try:
            import time
            cur = get_db().cursor()
            cur.execute("SELECT total_amount FROM accounts WHERE user_id ='%d'" % user_id)
            balance = cur.fetchall()[0][0]
            new_amount = balance + amount
            timerecord = time.strftime('%Y%m%d%H%M%S', timestamp)
            cur.execute(
                "UPDATE accounts SET total_amount = '%f' last_topup_date = '%s' last_topup_amount = '%f' WHERE user_id = '%d'" % (
                new_amount, amount, timerecord, user_id))
            get_db().commit()
        except:
            return False

#**********************
#*****Report Defect****
#**********************

#Create Defect incident
#Status set as DEFECT
def createDefectReport(user_id,bike_id,category,details):
    def createDefectReport(user_id, bike_id, category, details):
        try:
            import time
            cur = get_db().cursor()
            timestamp = time.localtime(time.time())
            timerecord = time.strftime('%Y%m%d%H%M%S', timestamp)

            report_id = timerecord + str(bike_id)
            report_datetime = time.strftime('%Y-%m-%d %H:%M', timestamp)
            status = "Unsolved"  # default
            cur.execute(
                "INSERT INTO defect_report (report_id,user_id,bike_id,category,details,report_datetime,status) VALUES (?,?,?,?,?,?,?)",
                (report_id, user_id, bike_id, category, details, report_datetime, status))
            get_db().commit()
        except:
            print("Fail to create defect report")
            return False

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