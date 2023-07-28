from flask import *
from flask_mysqldb import MySQL
from datetime import date

today = date.today()
ob=Flask(__name__)

ob.secret_key="fsdfegdsfgd$@&g2342342"

ob.config['MYSQL_USER']='root'
ob.config['MYSQL_PASSWORD']=''
ob.config['MYSQL_DB']='route'
mysql=MySQL(ob)

@ob.route('/')
@ob.route('/home')
def home():
        session['adminuser']=0
        mycur=mysql.connect.cursor()
        mycur.execute('select cities from cities')
        data=mycur.fetchall()
        return render_template("home.html",data=data)

@ob.route('/dohome',methods=['POST'])
def search():
    error=""
    start=request.form['start']
    end=request.form['end']
    bdate=request.form['date']
    newBdate=date.fromisoformat(bdate)
    if(start==end):
        mycur = mysql.connect.cursor()
        mycur.execute('select cities from cities')
        data = mycur.fetchall()
        error = "Cities should not be same"
        return render_template("home.html",error=error,data=data)
    elif(newBdate<=today):
        error ="Please Enter New Date"
        mycur = mysql.connect.cursor()
        mycur.execute('select cities from cities')
        data = mycur.fetchall()
        return render_template("home.html", error=error, data=data)
    elif(start=='From' or end=='To'):
        mycur = mysql.connect.cursor()
        mycur.execute('select cities from cities')
        data = mycur.fetchall()
        error = "please select cities properly"
        return render_template("home.html",error=error,data=data)
    else:
        mycur = mysql.connect.cursor()
        mycur.execute('select * from routes where (start=%s or end=%s) and (start=%s or end=%s)',(start,start,end,end))
        cite = mycur.fetchall()
        if(cite):
            session['start'] = start
            session['end'] = end
            session['date']=bdate
            for item in cite:
                if (start.lower() == item[1] and end.lower() == item[2]):
                    session['distance'] = item[3]
                    session['price']=item[4]
                    return render_template('booking.html')
                elif (start.lower() == item[2] and end.lower()== item[1]):
                    session['distance'] = item[3]
                    session['price'] = item[4]
                    return render_template('booking.html')
        else:
            error = "Routes not available"
            mycur = mysql.connect.cursor()
            mycur.execute('select cities from cities')
            data = mycur.fetchall()
            return render_template("home.html",error=error, data=data)

@ob.route('/doviewseat')
def doviewseat():
    return render_template("viewseat.html")


@ob.route('/goseat',methods=['GET'])
def seat():
    session['busno']=request.args['busno']
    mycur=mysql.connect.cursor()
    info=[session['start'],session['end'],session['date'],session['busno']]
    mycur.execute('select seat_no from bookinginfo where (start=%s and end=%s and date=%s and busno=%s)',info)
    bookedseat=mycur.fetchall()
    reservedseat=[]
    for copy in bookedseat:
        sep = "#"
        x=copy[0].split(sep)
        for item in x:
            reservedseat.append(int(item))

    return render_template('viewseat.html',reservedseat=reservedseat)
    # return str(reservedseat)

@ob.route('/dobook',methods=['POST'])
def book():
    seatno=request.form.getlist('seat')
    p=len(seatno)
    sep = "#"
    seatno = sep.join(seatno)
    session['seatno']=seatno
    session['p']=p
    if(seatno):
        totalfair=p*int(session['distance'])*9
        session['total']=totalfair
        return render_template('getInfo.html')
    else:
        error='Please Select seat'
        mycur = mysql.connect.cursor()
        info = [session['start'], session['end'], session['date']]
        mycur.execute('select seat_no from bookinginfo where (start=%s and end=%s and date=%s )', info)
        bookedseat = mycur.fetchall()
        reservedseat = []
        for copy in bookedseat:
            sep = "#"
            x = copy[0].split(sep)
            for item in x:
                reservedseat.append(int(item))

        return render_template('viewseat.html', reservedseat=reservedseat,error=error)


@ob.route('/bookconfirm',methods=['POST'])
def payment():
    pn=request.form.getlist('pn')
    cn = request.form['number']
    if(cn.isdigit()):
        x='pgender'
        pg=[]
        for i in range(1,session['p']+1):
                item=x+str(i)
                pg.append(request.form.get(item))

        email=request.form['email']
        session['email'] = email
        session['cn']=cn
        mycur=mysql.connect.cursor()
        sep="#"
        finalName=sep.join(pn)
        session['pn'] = finalName
        finalGender=sep.join(pg)
        session['pg'] = finalGender
        info = [session['p'],session['start'],session['end'],session['distance'],session['date'],session['busno'],session['seatno'],session['total'],session['email'],session['cn'],session['pn'],session['pg']]
        mycur.execute('insert into bookinginfo(no_of_pasenger,start,end,distance,date,busno,seat_no,total,email,contact,pass_name,pass_gender)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',info)

        info1 = [session['p'],session['start'],session['end'],session['distance'],session['date'],session['busno'],session['seatno'],session['total'],session['email'],session['cn'],session['pn'],session['pg']]
        mycur.execute('select * from bookinginfo where (no_of_pasenger=%s and start=%s and end=%s and distance=%s and date=%s and busno=%s and seat_no=%s and total=%s and email=%s and contact=%s and pass_name=%s and pass_gender=%s)',info1 )
        data2=mycur.fetchall()
        session['ticketdata']=data2
        if(session['busno']=="MP04BP1432"):
            session['time']="9:00 Am"
        elif (session['busno'] == "MP04BP1342"):
            session['time'] = "2:00 Pm"
        elif (session['busno'] == "MP04BP3142"):
            session['time'] = "7:00 Pm"
        return render_template('ticket.html',info=data2)
    else:
        error='Please Enter Correct Number'
        return render_template('getinfo.html',error=error)



@ob.route('/doprint')
def doprint():
    info = session['ticketdata']
    sep = "#"
    names = session['pn'].split(sep)
    gender=session['pg'].split(sep)
    seatno=session['seatno'].split(sep)
    return render_template("print.html",info=info,names=names,gender=gender,seatno=seatno)


# ******************************************************************************************************************************************

# managebooking


@ob.route('/domanage')
def domanage():
    return render_template("managebooking.html")

@ob.route('/manageinfo',methods=['POST'])
def getticket():
    tnumber=request.form['tnumber']
    mnumber=request.form['mnumber']
    item=[tnumber,mnumber]
    mycur=mysql.connect.cursor()
    mycur.execute('select * from bookinginfo where(uid=%s and contact=%s)',item)
    ticket=mycur.fetchall()
    if(ticket):
        dat=ticket[0][5]
        newdat = date.fromisoformat(dat)
        if(newdat >= today):
            return render_template('manageticket.html',data=ticket)
        else:
            return ('date is expired')
    else:
         return ('ticket not found')

@ob.route('/doupdateticket',methods=['POST'])
def doupdatetick():
    info=request.form
    info=[info['psngr'],info['from'],info['to'],info['distance'],info['date'],info['busno'],info['seat_no'],info['total'],info['pass_name'],info['pass_gender'],info['number'],info['email'],info['uid']]
    mycur=mysql.connect.cursor()
    mycur.execute('update bookinginfo set no_of_pasenger=%s,start=%s,end=%s,distance=%s,date=%s,busno=%s,seat_no=%s,total=%s,pass_name=%s,pass_gender=%s,contact=%s,email=%s where uid=%s',info)
    error="Data Updated"
    return render_template('managebooking.html',error=error)


@ob.route('/dogallery')
def dogallery():
    return render_template("gallery.html")

@ob.route('/doaboutus')
def doaboutus():
    return render_template("aboutus.html")

@ob.route('/docontact')
def docontact():
    return render_template("contact.html")

@ob.route('/dooffer')
def dooffers():
    return render_template("offers.html")

@ob.route('/dorefund')
def doref():
    return render_template("refund.html")

@ob.route('/checkref',methods=['POST'])
def checkref():
    error="Your Ticket Is Not Refundalbe....."
    return render_template("refund.html",error=error)


@ob.route('/docondition')
def docondition():
    return render_template("condition.html")

@ob.route('/dopolicy')
def dopolicy():
    return render_template("policy.html")

@ob.route('/dofaqs')
def dofaqs():
    return render_template("faqs.html")


#********************************************************************************************************************************************

# costumer login & Signup




@ob.route('/usersign')
def douser():
    session['user'] = 0
    return render_template("usersignup.html")


@ob.route('/dousersign',methods=['POST'])
def dousersign():
    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    password=request.form['password']
    num=[number]
    data1=[name.lower(),number,email,password]
    mycur = mysql.connect.cursor()
    mycur.execute('select * from user where number=%s',num)
    user=mycur.fetchall()
    if(user):
        error = ' This Number Already Have Account......'
        return render_template("usersignup.html", error=error)

    else:
        if(number[0].isdigit()):
                mycur.execute('insert into user(name,number,email,password)values(%s,%s,%s,%s)', data1)
                data1 = [1,name.lower(), number, email, password]
                session['user'] = data1
                return redirect('/home')
        else:
            error = ' Number should not contain charactor'
            return render_template("usersignup.html",error=error)

@ob.route('/userlogin')
def douserlogin():
    session['user']=0
    return render_template("userlogin.html")

@ob.route('/douserlogin',methods=['POST'])
def douserlog():
    session['usernumber']=request.form['number']
    session['userpassword']=request.form['password']
    info=[session['usernumber']]
    mycur = mysql.connect.cursor()
    mycur.execute('select * from user where number=%s',info)
    data = mycur.fetchone()
    if(data):
        if(data[4]==session['userpassword']):
            session['user']=data
            return redirect('/')
        else:
            error = 'Wrong Password....'
            return render_template('userlogin.html', error=error)
    else:
        error='Number Not Found Please Sign In First'
        return render_template('userlogin.html',error=error)


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# Adminpannel

@ob.route('/admin')
def admin():
    session['adminuser'] = 0
    return render_template('adminsite.html')

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Admin Login

@ob.route('/adminlogin',methods=['POST'])
def adminlogin():
    name = request.form['username']
    number = request.form['number']
    password = request.form['password']

    mycur = mysql.connect.cursor()
    mycur.execute('select * from adminuser')
    data=mycur.fetchall()
    for item in data:
        if(number==item[2]):
            if(password==item[4]):
                session['adminuser']=item
                error = 'Loged In'
                return redirect('/routes')
            else:
                error='Wrong Password'
                return render_template('adminsite.html',error=error)
        else:
            error='Number Not found '
            return render_template('adminsite.html',error=error)



#***********************************************************************************************************************************************

# Bus User

@ob.route('/user')
def user():
    if (session['adminuser']):
        mycur = mysql.connect.cursor()
        mycur.execute('select * from user')
        data = mycur.fetchall()
        if (data):
            return render_template('user.html', data=data)
        else:
            error = "No Admin Available"
            return render_template('adminsite.html', error=error)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/updateuser', methods=['GET'])
def userupdate():
        if(session['adminuser']):
            sno=request.args.get('sno')
            sno=[sno]
            mycur=mysql.connect.cursor()
            mycur.execute('select * from user where sno=%s',sno)
            data=mycur.fetchall()
            if(data):
                return render_template('changeuser.html',data=data)
            else:
                error='Not Found'
                return render_template("user.html",error=error)
        else:
            error = 'Please Login First'
            return render_template('adminsite.html', error=error)

@ob.route('/douserupdate', methods=['POST'])
def doupdate():
    sno=request.form['sno']
    name=request.form['name']
    number = request.form['number']
    email = request.form['email']
    password = request.form['password']
    info=[name,number,email,password,sno]
    mycur=mysql.connect.cursor()
    mycur.execute('update user set name=%s,number=%s,email=%s,password=%s where sno=%s',info)
    error='Data Updated'
    mycur = mysql.connect.cursor()
    mycur.execute('select * from user')
    data = mycur.fetchall()
    return render_template('user.html',data=data,error=error)


@ob.route('/deleteuser',methods=['GET'])
def deleteuser():
    if(session['adminuser']):
        sno=request.args.get('sno')
        sno=[sno]
        mycur=mysql.connect.cursor()
        mycur.execute('delete from user where sno=%s',sno)
        error = 'Data Deleted'
        mycur = mysql.connect.cursor()
        mycur.execute('select * from user')
        data = mycur.fetchall()
        if (data):
            return render_template('user.html', data=data,error=error)
        else:
            error = "No Admin Available"
            return render_template('adminsite.html', error=error)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/newuser')
def newuser():
    if(session['adminuser']):
        return render_template('adduser.html')
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)

@ob.route('/adduser',methods=['POST'])
def adduser():
    if(session['adminuser']):
        name=request.form['name']
        number = request.form['number']
        email = request.form['email']
        password = request.form['password']
        info=[name.lower(),number,email,password]
        mycur=mysql.connect.cursor()
        mycur.execute('insert into user(name,number,email,password) values(%s,%s,%s,%s)',info)
        error = 'Data Added'
        mycur = mysql.connect.cursor()
        mycur.execute('select * from user')
        data = mycur.fetchall()
        return render_template('user.html',data=data,error=error)

    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Adminuser

@ob.route('/adminuser')
def adminuser():
    if(session['adminuser']):
        mycur = mysql.connect.cursor()
        mycur.execute('select * from adminuser')
        data = mycur.fetchall()
        if (data):
            return render_template('adminuser.html', data=data)
        else:
            error = "No Admin Available"
            return render_template('adminuser.html', error=error)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/adminedit',methods=['GET'])
def adminedit():
    if(session['adminuser']):
        sno=request.args.get('sno')
        mycur=mysql.connect.cursor()
        mycur.execute('select * from adminuser where uno=%s',sno)
        data=mycur.fetchall()
        return render_template('updateadmin.html',data=data)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/doadminupdate', methods=['POST'])
def doadminupdate():
    sno=request.form['sno']
    name=request.form['name']
    number = request.form['number']
    email = request.form['email']
    password = request.form['password']
    info=[name,number,email,password,sno]
    mycur=mysql.connect.cursor()
    mycur.execute('update adminuser set name=%s,number=%s,email=%s,password=%s where uno=%s',info)
    error='Data Updated'
    mycur = mysql.connect.cursor()
    mycur.execute('select * from adminuser')
    data = mycur.fetchall()
    return render_template('adminuser.html', data=data,error=error)


@ob.route('/admindelete',methods=['GET'])
def deleteadmin():
    if(session['adminuser']):
        sno=request.args.get('sno')
        sno=[sno]
        mycur=mysql.connect.cursor()
        mycur.execute('delete from adminuser where uno=%s',sno)
        error = 'Data Deleted'
        mycur = mysql.connect.cursor()
        mycur.execute('select * from adminuser')
        data = mycur.fetchall()
        if (data):
            return render_template('adminuser.html', data=data,error=error)
        else:
            error = "No Admin Available"
            return render_template('adminuser.html', error=error)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/newadminuser')
def newadminuser():
     if(session['adminuser']):
        return render_template('addadminuser.html')
     else:
         error = 'Please Login First'
         return render_template('adminsite.html', error=error)


@ob.route('/addadminuser',methods=['POST'])
def addadminuser():
    name=request.form['name']
    number = request.form['number']
    email = request.form['email']
    password = request.form['password']
    info=[name.lower(),number,email,password]
    mycur=mysql.connect.cursor()
    mycur.execute('insert into adminuser(name,number,email,password) values(%s,%s,%s,%s)',info)
    error = 'Data Added'
    mycur = mysql.connect.cursor()
    mycur.execute('select * from adminuser')
    data = mycur.fetchall()
    return render_template('adminuser.html',data=data,error=error)


# **********************************************************************************************************************************************
# Routes


@ob.route('/routes')
def routes():
    if(session['adminuser']):
        mycur = mysql.connect.cursor()
        mycur.execute('select * from routes')
        data = mycur.fetchall()
        return render_template('routes.html',data=data)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html',error=error)


@ob.route('/updateroute',methods=['GET'])
def updateroute():
    if(session['adminuser']):
        sno = request.args.get('sno')
        nm = [sno]
        mycur = mysql.connect.cursor()
        mycur.execute('select * from routes where sno=%s', nm)
        data = mycur.fetchall()
        if (data):
            return render_template('changeroute.html', data=data)
        else:
            return ("Not Correct option")
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)

@ob.route('/dorouteupdate', methods=['POST'])
def dorouteupdate():
    sno=request.form['sno']
    s=request.form['from']
    e = request.form['to']
    distance= request.form['distance']
    price = request.form['price']
    info=[s,e,distance,price,sno]
    mycur=mysql.connect.cursor()
    mycur.execute('update routes set start=%s,end=%s,km=%s,price=%s where sno=%s',info)
    return redirect('/routes')


@ob.route('/deleteroute',methods=['GET'])
def deleteroute():
    if(session['adminuser']):
        sno = request.args.get('sno')
        nm = [sno]
        mycur = mysql.connect.cursor()
        mycur.execute('delete from routes where sno=%s', nm)
        return redirect('/routes')
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/newroute')
def newroute():
    if(session['adminuser']):
        return render_template('addroute.html')
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/addroute',methods=['POST'])
def addroute():
    s= request.form['from']
    e = request.form['to']
    distance = request.form['distance']
    price = request.form['price']
    info = [s,e,distance,price]
    mycur = mysql.connect.cursor()
    mycur.execute('insert into routes(start,end,km,price) values(%s,%s,%s,%s)', info)
    return redirect('/routes')


# **********************************************************************************************************************************************
# Bookingdata


@ob.route('/bookingdata',methods=['GET'])
def bookingdata():
    if(session['adminuser']):
        no=request.args.get('book')
        if(no=='1'):
            tdate=[today]
            mycur = mysql.connect.cursor()
            mycur.execute('select * from bookinginfo where date>%s',tdate)
            data = mycur.fetchall()
            if(data):
                return render_template('bookingdata.html',data=data)
            else:
                error = "NO Advance Boooking Available"
                data = "There Is No Data...."
                return render_template('bookingdata.html',emp=data,error=error)
        elif(no == '2'):
            tdate = [today]
            mycur = mysql.connect.cursor()
            mycur.execute('select * from bookinginfo where date=%s', tdate)
            data = mycur.fetchall()
            if (data):
                return render_template('bookingdata.html', data=data)
            else:
                error = "No Todays Booking Available"
                data="There Is No Data...."
                return render_template('bookingdata.html',emp=data,error=error)
        elif(no == '3'):
            tdate = [today]
            mycur = mysql.connect.cursor()
            mycur.execute('select * from bookinginfo where date<%s', tdate)
            data = mycur.fetchall()
            if (data):
                return render_template('bookingdata.html', data=data)
            else:
                error = "No Old Booking Available"
                data = "There Is No Data...."
                return render_template('bookingdata.html',emp=data, error=error)
        else:
            mycur = mysql.connect.cursor()
            mycur.execute('select * from bookinginfo')
            data = mycur.fetchall()
            if (data):
                return render_template('bookingdata.html', data=data)
            else:
                error = "No Booking Available"
                return render_template('adminsite.html', error=error)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/editbooking',methods=['GET'])
def editbooking():
    if(session['adminuser']):
        sno = request.args.get('uid')
        nm = [sno]
        mycur = mysql.connect.cursor()
        mycur.execute('select * from bookinginfo where uid=%s', nm)
        data = mycur.fetchall()
        if (data):
            return render_template('updatebooking.html',data=data)

        else:
            return ("Not Correct option")
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


@ob.route('/doupdatebook',methods=['POST'])
def doupdatebook():
    info=request.form
    info=[info['psngr'],info['from'],info['to'],info['distance'],info['date'],info['busno'],info['seat_no'],info['total'],info['pass_name'],info['pass_gender'],info['number'],info['email'],info['uid']]
    mycur=mysql.connect.cursor()
    mycur.execute('update bookinginfo set no_of_pasenger=%s,start=%s,end=%s,distance=%s,date=%s,busno=%s,seat_no=%s,total=%s,pass_name=%s,pass_gender=%s,contact=%s,email=%s where uid=%s',info)
    error="Data Updated"
    return render_template('adminsite.html',error=error)


@ob.route('/deletebooking',methods=['GET'])
def deletebooking():
    if(session['adminuser']):
        error="Data Deleted"
        uid=request.args.get('uid')
        uid=[uid]
        mycur=mysql.connect.cursor()
        mycur.execute('delete from bookinginfo where uid=%s',uid)
        return render_template('adminsite.html',error=error)
    else:
        error = 'Please Login First'
        return render_template('adminsite.html', error=error)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Search Bar for User, Bookingdata and routes


@ob.route('/dousersearch',methods=['POST'])
def usersearch():
    search = request.form['search']
    error = ''
    if (search):
        search = [search.lower(),search,search, search]
        mycur = mysql.connect.cursor()
        mycur.execute('select * from user where(name=%s or number=%s or email=%s or name=%s)', search)
        data = mycur.fetchall()
        if (data):
            return render_template('user.html', data=data)
        else:
            error = 'User Not available'
            mycur = mysql.connect.cursor()
            mycur.execute('select * from user')
            data = mycur.fetchall()
            return render_template('user.html', data=data, error=error)

    else:
        error = 'Please Enter Valid Input'
        mycur = mysql.connect.cursor()
        mycur.execute('select * from user')
        data = mycur.fetchall()
        return render_template('user.html', data=data, error=error)


@ob.route('/doroutesearch',methods=['POST'])
def routesearch():
    search=request.form['search']
    if(search):
        search=[search.lower(),search.lower()]
        mycur = mysql.connect.cursor()
        mycur.execute('select * from routes where(start=%s or end=%s)',search)
        data = mycur.fetchall()
        if(data):
            return render_template('routes.html',data=data)
        else:
            error='Route Not available OR Search Correct Name of Destination'
            mycur = mysql.connect.cursor()
            mycur.execute('select * from routes')
            data = mycur.fetchall()
            return render_template('routes.html', data=data, error=error)

    else:
        error='Please enter route'
        mycur = mysql.connect.cursor()
        mycur.execute('select * from routes')
        data = mycur.fetchall()
        return render_template('routes.html', data=data,error=error)


@ob.route('/dobookingsearch', methods=['POST'])
def bookingsearch():
    search = request.form['search']
    error = ''
    if (search):
        search = [search]
        mycur = mysql.connect.cursor()
        mycur.execute('select * from bookinginfo where uid=%s', search)
        data = mycur.fetchall()
        if (data):
            return render_template('bookingdata.html', data=data)
        else:
            error = 'Booking Not available'
            mycur = mysql.connect.cursor()
            mycur.execute('select * from bookinginfo')
            data = mycur.fetchall()
            return render_template('bookingdata.html',data=data,error=error)

    else:
        error = 'Please enter PNR Number'
        mycur = mysql.connect.cursor()
        mycur.execute('select * from bookinginfo')
        data = mycur.fetchall()
        return render_template('bookingdata.html', data=data, error=error)





ob.run(debug=True,port=679865)