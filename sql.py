import mysql.connector


db = mysql.connector.connect(
host='localhost',
user='root',
password='T3ntramitr0z0n',
database='crudbd',
port = 3307,
)
cursor =db.cursor()
print(db)
#sql= "select * from crud1 where id=%s"
#par=(3,)
#cursor.execute(sql,par)
#resultado =cursor.fetchall()[0]
#print(resultado)

#sql= "insert into crud1 (name,email,phone) values (%s,%s,%s)"
#values=[
#     ("Liam","liam18@gmail.com",6554545),
#     ("Lucas","lucas23@gmail.com",6554545),

#]
#cursor.executemany(sql,values)
#db.commit()
