from django.shortcuts import render
from CustomerApp import Database
# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'CustomerApp/Login.html')

def Register(request):
    return render(request,'CustomerApp/Register.html')


def RegAction(request):
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']
    address=request.POST['address']
    username=request.POST['username']
    password=request.POST['password']



    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from customer where  email='"+email+"' and mobile='"+mobile+"'")
    d=cur.fetchone()
    if d is not None:

     context={'msg':'Already Exist These Details...!!'}
     return render(request,'CustomerApp/Register.html', context)
    else:
        cur=con.cursor()
        cur.execute("insert into customer values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
        con.commit()
        context={'msg':'Successfully Registered Your Details...!!'}
        return render(request,'CustomerApp/Register.html', context)


def LogAction(request):
    uname=request.POST['username']
    pwd=request.POST['password']

    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from customer where username='"+uname+"' and password='"+pwd+"'")
    d=cur.fetchone()
    if d is not None:
        request.session['userid']=d[0]
        request.session['name']=d[1]
        request.session['email']=d[2]
        return render(request, 'CustomerApp/CustomerHome.html')
    else:
        context={'msg':'Login Failed...!!'}
        return render(request, 'CustomerApp/Login.html',context)

def CustomerHome(request):
    return render(request,'CustomerApp/CustomerHome.html')

def Search(request):
    return render(request,'CustomerApp/Search.html')

def SearchAction(request):
    name=request.POST['name']
    con=Database.DBConnection()
    cur1=con.cursor()
    cur1.execute("select * from products  where product like '%"+name+"%' or location like '%"+name+"%'")
    data=cur1.fetchall()
    table="<table><tr><th>ProductName</th><th>Farmer Sale Price</th><th>Location</th><th>Farmer Name</th><th>Farmer Email</th><th>Book</th></tr>"
    for d in data:
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+" Rs/Kg</td><td>"+str(d[3])+"</td><td>"+str(d[5])+"</td><td>"+str(d[6])+"</td><td><a href='/BookingConfirm/?id="+str(d[0])+"&name="+str(d[1])+"&price="+str(d[2])+"&fid="+str(d[4])+"'><font color='red'>Click</font></a></td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'CustomerApp/ViewProducts.html', context)

def BookingConfirm(request):

    iid = request.GET['id']
    name = request.GET['name']
    price=request.GET['price']
    fid=request.GET['fid']
    context = {'id': iid, 'name': name,'price':price,'fid':fid}
    return render(request,'CustomerApp/BookProducts.html', context)

def BookAction(request):
    uid=request.session['userid']
    uuid=str(uid)
    name=request.session['name']
    email=request.session['email']

    pid = request.POST['pid']
    pname = request.POST['pname']
    price=request.POST['price']
    noof=request.POST['noof']
    fid=request.POST['fid']

    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("insert into booking values(null,'"+uuid+"','"+name+"','"+email+"','"+pid+"','"+pname+"','"+price+"','"+fid+"','"+noof+"','waiting','waiting','waiting')")
    con.commit()
    context={'msg':'Booking Request Sent to Farmer Successful...!!'}
    return render(request,'CustomerApp/CustomerHome.html', context)



def Booked(request):
    uid=request.session['userid']
    uuid=str(uid)
    con=Database.DBConnection()
    cur1=con.cursor()
    cur1.execute("select * from booking b,price_details p  where b.cid='"+uuid+"' and b.pname=p.pname")
    data=cur1.fetchall()
    table="<table><tr><th>ProductName</th><th>Price/Kg</th><th>Quantity</th><th>Total</th><th>Farmer ID</th><th>Total Profit</th><th>Status</th></tr>"
    for d in data:
        p=int(d[6])
        q=int(d[8])
        dsprice=int(d[16])
        t=p*q
        tf=dsprice-p
        q=int(d[8])
        tp=tf*q

        table+="<tr><td>"+str(d[5])+"</td><td>Rs."+str(d[6])+"</td><td>"+str(d[8])+" Kg</td><td>Rs."+str(t)+"</td><td>"+str(d[7])+"</td><td style=background:orange>Rs."+str(tp)+"</td><td>"+str(d[9])+"</td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'CustomerApp/ViewBookedProducts.html', context)



