import pymysql
def DBConnection():
    con=pymysql.connect(host='localhost', user='root', password='root', database='green_basket', charset='utf8')
    return con
