import pymysql
from app import app
##from tables import Results
from db_config import mysql
from flask import flash, render_template, request, redirect
from jinja2 import Environment
from datetime import date

logged=0
Uniname=''

@app.route('/new_ad')
def add_user_view():
    return render_template('PostAdd.html')

@app.route('/filt')
def filtering():
    return render_template('FilterAd.html')

@app.route('/filter',methods = ['POST', 'GET'])
def filter():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        today = str(date.today())
        print(today)

        transport = request.form['inp_transport']
        ticketFrom = request.form['inputFrom']
        ticketTo = request.form['inputTo']
        tickets = request.form['inputTickets']
        price = request.form['inputPrice']

        cursor.execute("SELECT * FROM ad_table WHERE TicketDate >= CURDATE() AND transport= %s AND TicketFrom = %s AND TicketTo = %s AND TicketPrice <= %s ORDER BY TicketDate ASC, Tickets DESC, TicketPrice ASC",(transport,ticketFrom,ticketTo,int(price)))
        rows = cursor.fetchall()
        print(rows)
        x = len(rows)
        print("row count ",x)
        li = range(0,x)
        li = [*li]
        # li.reverse()

        #table = Results(rows)

        # table.border = True
        return render_template('tbl.html', rows=rows,li=li, logged=logged)
        # return render_template('tb.html',name=name,email=email,PhN=PhN,tickets=tickets)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/log_out',methods = ['POST', 'GET'])
def log_out():
    global logged
    logged=0
    return redirect('/')
        
@app.route('/add', methods=['POST'])
def add_post():
    try:
        """name = request.form['inputName']
        email = request.form['inputEmail']
        phoneNumber = request.form['inputPN']"""
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        name = Uniname

        cursor.execute("SELECT email, phone FROM userinfo WHERE name=%s", Uniname)

        myresult = cursor.fetchone()
        
        create="CREATE TABLE if not exists `roytuts`.`ad_table` ( `user_id` BIGINT UNIQUE AUTO_INCREMENT, `transport` TEXT (15), `user_Name` TEXT (30), `user_Email` TEXT(30), `user_PhoneNumber` TEXT (15), `TicketFrom` TEXT (20), `TicketTo` TEXT (20), `TicketTime` TEXT (20), `TicketDate` TEXT (20), `Tickets` TEXT (5), `TicketPrice` TEXT (8), PRIMARY KEY (`user_id`))"
        cursor.execute(create)
        
        email = myresult["email"]
        phoneNumber = myresult["phone"]
        transport = request.form['inp_transport']
        ticketFrom = request.form['inputFrom']
        ticketTo = request.form['inputTo']
        ticketTime = request.form['inputTime']
        ticketDate = request.form['inputDate']
        tickets = request.form['inputTickets']
        price = request.form['inputPrice']

        # validate the received values
        if name and email and phoneNumber and transport and ticketFrom and ticketTo and ticketTime and ticketDate and tickets and price and request.method == 'POST':
            sql = "INSERT INTO ad_table(transport, user_Name, user_Email, user_PhoneNumber, TicketFrom, TicketTo, TicketTime, TicketDate, Tickets, TicketPrice) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (transport, name, email, phoneNumber, ticketFrom, ticketTo, ticketTime, ticketDate, tickets, price,)
            
            cursor.execute(sql, data)
            conn.commit()
            flash('New ad posted successfully!')
            return redirect('/')
        else:
            return 'Error while posting ad'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
@app.route('/')
def ads():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        today = str(date.today())
        print(today)
        cursor.execute("SELECT * FROM ad_table WHERE TicketDate >= CURDATE() ORDER BY TicketDate ASC")
        rows = cursor.fetchall()
        x = len(rows)
        li = range(0,x)
        li = [*li]
        # li.reverse()

        # print("Rows",rows)
        # print("li",li)

        name = []
        email = []
        PhN = []
        tickets = []

        """for row in rows:
            print(row["user_Name"], row["user_Email"], row['user_PhoneNumber'], row['Tickets'])
            name.append(row["user_Name"])
            email.append(row["user_Email"])
            PhN.append(row["user_PhoneNumber"])
            tickets.append(row["Tickets"])"""

        # table = Results(rows)

        # table.border = True
        return render_template('tbl.html', rows=rows,li=li, logged=logged)
        # return render_template('tb.html',name=name,email=email,PhN=PhN,tickets=tickets)
    except Exception as e:
        print(e)

    finally:
        cursor.close() 
        conn.close()

@app.route('/edit/<int:id>')
def edit_view(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM ad_table WHERE user_id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('EditPost.html', row=row)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update', methods=['POST'])
def update_user():
    try:        
        name = request.form['inputName']
        email = request.form['inputEmail']
        phoneNumber = request.form['inputPN']
        ticketFrom = request.form['inputFrom']
        ticketTo = request.form['inputTo']
        ticketTime = request.form['inputTime']
        ticketDate = request.form['inputDate']
        tickets = request.form['inputTickets']
        price = request.form['inputPrice']
        _id = request.form['id']
        # validate the received values
        if name and email and phoneNumber and ticketFrom and ticketTo and ticketTime and ticketDate and tickets and price and _id and request.method == 'POST':
            sql = "UPDATE ad_table SET user_name=%s, user_email=%s, user_PhoneNumber=%s, TicketFrom=%s, TicketTo=%s, TicketTime=%s, TicketDate=%s, Tickets=%s, TicketPrice=%s WHERE user_id=%s"
            data = (name, email, phoneNumber, ticketFrom, ticketTo, ticketTime, ticketDate, tickets, price, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('Ad updated successfully!')
            return redirect('/')
        else:
            return 'Error while updating ad'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
@app.route('/delete/<int:id>')
def delete_user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ad_table WHERE user_id=%s", (id,))
        conn.commit()
        flash('Ad deleted successfully!')
        return redirect('/')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/loginpage', methods=['POST', 'GET'])
def loginpage():
    return render_template('login/login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
   global logged
   global Uniname
   if request.method == 'POST':
        user = request.form['username']
        userpass = request.form['pass']
        print("user:",user)
        print("password:",userpass)

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT pass FROM userinfo WHERE name=%s", user)

        myresult = cursor.fetchone()
        print("real password:",myresult["pass"])

        print(str(userpass),"comparing to ",str(myresult["pass"]))
        
        if(str(userpass) == str(myresult["pass"])):
          print("successful login")
          logged=1
          Uniname = user
          print("user's name",Uniname)
          return redirect('/')
        else:
          print("Failure in logging")
          return redirect('/loginpage')
   else:
        return redirect('/')


@app.route('/signuppage',methods = ['POST', 'GET'])
def signuppage():
    return render_template('signup/signup.html')


@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   global logged
   global Uniname

   if request.method == 'POST':
       
       userName = request.form['name']
       birthday = request.form['birthday']
       gender = request.form['gender']
       email = request.form['email']
       userpass = request.form['password']
       phone = request.form['phone']
       address = request.form['address']

       conn = mysql.connect()
       cursor = conn.cursor(pymysql.cursors.DictCursor)
      
       com = "CREATE TABLE if not exists `roytuts`.`userinfo` (`user_id` BIGINT UNIQUE AUTO_INCREMENT,  `name` TEXT (30), `birthday` TEXT(30), `gender` TEXT (15), `email` TEXT (20), `pass` TEXT (20), `phone` TEXT (20), `address` TEXT (20), PRIMARY KEY (`user_id`))"  

       cursor.execute(com)

       sql = "INSERT INTO userinfo (name, birthday, gender, email, pass, phone,address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
       val = (userName,birthday,gender,email,userpass,phone,address)

       cursor.execute(sql, val)
       conn.commit()
       logged=1
       Uniname = userName
       print("Signed in as",Uniname) 

       return redirect('/')
   else:
       user = request.args.get('nm')
       return redirect('/')

        
if __name__ == "__main__":
    app.run()
