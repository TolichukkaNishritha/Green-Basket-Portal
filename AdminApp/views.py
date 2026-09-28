from django.shortcuts import render
from CustomerApp import Database
# Create your views here.
def login(request):
    return render(request,'AdminApp/Login.html')


def logAction(request):
    uname=request.POST['username']
    pwd=request.POST['password']

    if uname=='Admin' and pwd =='Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        return render(request,'AdminApp/Login.html')

def Home(request):
    return render(request,'AdminApp/AdminHome.html')


def pricedetails(request):
    return render(request,'AdminApp/AddrPriceDetails.html')


def priceAction(request):
    name=request.POST['pname']
    mprice=request.POST['mprice']
    dpprice=request.POST['dpprice']
    dsprice=request.POST['dsprice']

    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from price_details where  pname='"+name+"'")
    d=cur.fetchone()
    if d is not None:

     context={'msg':'Product Details Already Added...!!'}
     return render(request,'AdminApp/AddrPriceDetails.html', context)
    else:
        cur=con.cursor()
        cur.execute("insert into price_details values(null,'"+name+"','"+mprice+"','"+dpprice+"','"+dsprice+"')")
        con.commit()
        context={'msg':'Price Details added Successfully...!!'}
        return render(request,'AdminApp/AddrPriceDetails.html', context)

def Viewpricedetails(request):
    con=Database.DBConnection()
    cur=con.cursor()
    cur.execute("select * from price_details")
    data=cur.fetchall()
    table="<table><tr><th>ProductName</th><th>Market Value/KG</th><th>Dealer Purchase/KG</th><th>Dealer Sale/KG</th></tr>"
    for d in data:
        table+="<tr><td>"+str(d[1])+"</td><td>Rs."+str(d[2])+"</td><td>Rs."+str(d[3])+"</td><td>Rs."+str(d[4])+"</td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'AdminApp/ViewPriceDetails.html', context)



