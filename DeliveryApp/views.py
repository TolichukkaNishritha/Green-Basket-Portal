from django.shortcuts import render
from CustomerApp import Database
# Create your views here.
def login(request):
    return render(request,'DeliveryApp/Login.html')

def register(request):
    return render(request,'DeliveryApp/Register.html')

def RegAction(request):
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']
    address=request.POST['address']
    username=request.POST['username']
    password=request.POST['password']



    con=Database.DBConnection()
    cur = con.cursor()
    cur.execute("select * from delivery where  email='"+email+"' and mobile='"+mobile+"' and address='"+address+"'")
    d=cur.fetchone()
    if d is not None:

     context={'msg':'Already Exist These Details...!!'}
     return render(request,'DeliveryApp/Register.html', context)
    else:
        cur=con.cursor()
        cur.execute("insert into delivery values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
        con.commit()
        context={'msg':'Successfully Registered Your Details...!!'}
        return render(request,'DeliveryApp/Register.html', context)


def LogAction(request):
    uname=request.POST['username']
    pwd=request.POST['password']

    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from delivery where username='"+uname+"' and password='"+pwd+"'")
    d=cur.fetchone()
    if d is not None:
        request.session['userid']=d[0]
        request.session['name']=d[1]
        request.session['email']=d[2]
        request.session['location']=d[4]
        return render(request, 'DeliveryApp/DeliveryHome.html')
    else:
        context={'msg':'Login Failed...!!'}
        return render(request, 'DeliveryApp/Login.html',context)

def DeliveryHome(request):
    return render(request,'DeliveryApp/DeliveryHome.html')

def Dproducts(request):
    userid=request.session['userid']
    uuid=str(userid)
    con=Database.DBConnection()
    cur1=con.cursor()
    cur1.execute("select * from booking b,customer c where b.dp_id='"+uuid+"' and c.id=b.cid")
    data=cur1.fetchall()
    table="<table><tr><th>Customer Name</th><th>Customer Email</th><th>Delivery Location</th><th>Product Name</th><th>Quantity</th><th>Delivery Status</th></tr>"
    for d in data:
        status=str(d[11])
        if status=='waiting':
            table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td><a href='/deliveryapp/UpdateDeliver?id="+str(d[0])+"'><font color='red'>Update Delivery</font></a></td></tr>"
        else:
            table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>"+str(d[11])+"</td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'DeliveryApp/DeliveryProducts.html',context)

def UpdateDeliver(request):
    userid=request.session['userid']
    uuid=str(userid)
    id=request.GET['id']
    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("update booking set dp_status='Delivered',status='Delivered' where id='"+id+"'")
    con.commit()
    cur1=con.cursor()
    cur1.execute("select * from booking b,customer c where b.dp_id='"+uuid+"' and c.id=b.cid")
    data=cur1.fetchall()
    table="<table><tr><th>Customer Name</th><th>Customer Email</th><th>Delivery Location</th><th>Product Name</th><th>Quantity</th><th>Delivery Status</th></tr>"
    for d in data:
      table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>"+str(d[11])+"</td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'DeliveryApp/DeliveryProducts.html',context)



