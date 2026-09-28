from django.shortcuts import render
from CustomerApp import Database

# Create your views here.
def login(request):
    return render(request,'FarmerApp/Login.html')


def Register(request):
    return render(request,'FarmerApp/Register.html')

def RegAction(request):
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']
    address=request.POST['address']
    username=request.POST['username']
    password=request.POST['password']



    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from farmer where  email='"+email+"' and mobile='"+mobile+"'")
    d=cur.fetchone()
    if d is not None:

     context={'msg':'Already Exist Email AND Mobile Details...!!'}
     return render(request,'FarmerApp/Register.html', context)
    else:
        cur=con.cursor()
        cur.execute("insert into farmer values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
        con.commit()
        context={'msg':'Successfully Registered Your Details...!!'}
        return render(request,'FarmerApp/Register.html', context)


def LogAction(request):
    uname=request.POST['username']
    pwd=request.POST['password']

    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from farmer where username='"+uname+"' and password='"+pwd+"'")
    d=cur.fetchone()
    if d is not None:
        request.session['userid']=d[0]
        request.session['name']=d[1]
        request.session['email']=d[2]
        return render(request, 'FarmerApp/FarmerHome.html')
    else:
        context={'msg':'Login Failed...!!'}
        return render(request, 'FarmerApp/Login.html',context)

def FarmerHome(request):
    return render(request,'FarmerApp/FarmerHome.html')


def AddProducts(request):
    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from price_details")
    data=cur.fetchall()
    table="<table><tr><th>ProductName</th><th>Market Value/KG</th><th>Dealer Purchase/KG</th><th>Dealer Sale/KG</th></tr>"
    for d in data:
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    table+="</table>"

    table2="<tr><th>Select Product</th><td><select name='product' required>"
    for d1 in data:
        table2+="<option value="+str(d1[1])+">"+str(d1[1])+"</option>"
    table2+="</td></tr>"


    context={'data':table,'data2':table2}
    return render(request,'FarmerApp/AddProducts.html',context)


def addPAction(request):
    product=request.POST['product']
    dprice=request.POST['dprice']
    location=request.POST['location']
    email=request.session['email']
    uid=request.session['userid']
    uuid=str(uid)
    name=request.session['name']

    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from products where  product='"+product+"' and email='"+email+"'")
    d=cur.fetchone()
    if d is not None:
         #Getting product Details
        cur1=con.cursor()
        cur1.execute("select * from price_details")
        data=cur1.fetchall()
        table="<table><tr><th>ProductName</th><th>Market Value/KG</th><th>Dealer Purchase/KG</th><th>Dealer Sale/KG</th></tr>"
        for d in data:
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
        table+="</table>"

        table2="<tr><th>Select Product</th><td><select name='product' required>"
        for d1 in data:
            table2+="<option value="+str(d1[1])+">"+str(d1[1])+"</option>"
        table2+="</td></tr>"
        context={'data':table,'data2':table2,'msg':'Product Details Already Added...!!'}
        return render(request,'FarmerApp/AddProducts.html', context)
    else:

        cur=con.cursor()
        cur.execute("insert into products values(null,'"+product+"','"+dprice+"','"+location+"','"+uuid+"','"+name+"','"+email+"')")
        con.commit()

        #Getting product Details
        cur1=con.cursor()
        cur1.execute("select * from price_details")
        data=cur1.fetchall()
        table="<table><tr><th>ProductName</th><th>Market Value/KG</th><th>Dealer Purchase/KG</th><th>Dealer Sale/KG</th></tr>"
        for d in data:
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
        table+="</table>"

        table2="<tr><th>Select Product</th><td><select name='product' required>"
        for d1 in data:
            table2+="<option value="+str(d1[1])+">"+str(d1[1])+"</option>"
        table2+="</td></tr>"
        context={'data':table,'data2':table2,'msg':'Successfully Product Details added...!!'}
        return render(request,'FarmerApp/AddProducts.html', context)


def viewproducts(request):
    email=request.session['email']
    con=Database.DBConnection()
    cur1=con.cursor()
    cur1.execute("select * from products where email='"+email+"'")
    data=cur1.fetchall()
    table="<table><tr><th>ProductName</th><th>Direct Sale Price</th><th>Location</th></tr>"
    for d in data:
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'FarmerApp/ViewProducts.html', context)



def BookingRequest(request):
    userid=request.session['userid']
    uuid=str(userid)
    con=Database.DBConnection()
    cur1=con.cursor()
    #cur1.execute("select * from booking b,customer c where b.fid='"+uuid+"' and c.id=b.cid")
    cur1.execute("select * from booking b,customer c,price_details pd where b.fid='"+uuid+"' and c.id=b.cid and b.pname=pd.pname")
    data=cur1.fetchall()
    table="<table><tr><th>Customer Name</th><th>Customer Email</th><th>Customer Location</th><th>Product Name</th><th>Quantity</th><th>Total Profit</th><th>Delivery Status</th></tr>"
    for d in data:
        status=str(d[9])
        cprice=int(d[6])

        dprice=int(d[22])
        fp=cprice-dprice
        q=int(d[8])
        tp=fp*q

        if status=='waiting':
            table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>Rs."+str(tp)+"</td><td><a href='/farmerapp/AssignDeliver?id="+str(d[0])+"&clocation="+str(d[16])+"'><font color='red'>Send To Deliver</font></a></td></tr>"
        else:
            table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>Rs."+str(tp)+"</td><td>"+str(d[9])+"</td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'FarmerApp/ViewBookedProducts.html', context)

def AssignDeliver(request):
    id=request.GET['id']
    clocation=request.GET['clocation']
    con=Database.DBConnection()
    cur1=con.cursor()

    cur1.execute("select * from delivery  where address='"+clocation+"'")
    data=cur1.fetchone()
    if data is not None:
        did=str(data[0])
        cur2=con.cursor()
        cur2.execute("update booking set status='Order sent to delivery person',dp_id='"+did+"' where id='"+id+"'")
        con.commit()

        #VIEW BOOKED PRODUCTS
        userid=request.session['userid']
        uuid=str(userid)
        con=Database.DBConnection()
        cur=con.cursor()
        cur.execute("select * from booking b,customer c,price_details pd where b.fid='"+uuid+"' and c.id=b.cid and c.id=b.cid and b.pname=pd.pname")
        data=cur.fetchall()
        table="<table><tr><th>Customer Name</th><th>Customer Email</th><th>Customer Location</th><th>Product Name</th><th>Quantity</th><th>Total Profit</th><th>Delivery Status</th></tr>"
        for d in data:
            status=str(d[9])
            cprice=int(d[6])

            dprice=int(d[22])
            fp=cprice-dprice
            q=int(d[8])
            tp=fp*q

            if status=='waiting':
                table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>Rs."+str(tp)+"</td><td><a href='/farmerapp/AssignDeliver?id="+str(d[0])+"&clocation="+str(d[16])+"'><font color='red'>Send To Deliver</font></a></td></tr>"
            else:
                table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>Rs."+str(tp)+" Kg</td><td>"+str(d[9])+"</td></tr>"
        table+="</table>"
        context={'data':table,'msg':'Order Details Sent To Delivery Person'}
        return render(request,'FarmerApp/ViewBookedProducts.html',context)
    else:
        #VIEW BOOKED PRODUCTS
        userid=request.session['userid']
        uuid=str(userid)
        con=Database.DBConnection()
        cur=con.cursor()
        cur.execute("select * from booking b,customer c,price_details pd where b.fid='"+uuid+"' and c.id=b.cid and b.pname=pd.pname")
        data=cur.fetchall()
        table="<table><tr><th>Customer Name</th><th>Customer Email</th><th>Customer Location</th><th>Product Name</th><th>Quantity</th><th>Profit</th><th>Delivery Status</th></tr>"
        for d in data:
            status=str(d[9])
            cprice=int(d[6])
            dprice=int(d[22])
            fp=cprice-dprice
            q=int(d[8])
            tp=fp*q
            if status=='waiting':
                table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>Rs."+str(tp)+"</td><td><a href='/farmerapp/AssignDeliver?id="+str(d[0])+"&clocation="+str(d[16])+"'><font color='red'>Send To Deliver</font></a></td></tr>"
            else:
                table+="<tr><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[16])+"</td><td>"+str(d[5])+"</td><td>"+str(d[8])+" Kg</td><td>Rs."+str(tp)+"</td><td>"+str(d[9])+"</td></tr>"
        table+="</table>"
        context={'data':table,'msg':'Delivery is not available for this location'}
        return render(request,'FarmerApp/ViewBookedProducts.html',context)













