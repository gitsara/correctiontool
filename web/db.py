'''
Created on 2012-11-23

@author: xizhao
'''
import sqlite3

con = sqlite3.connect("test.db") 
cur = con.cursor() 
cur.execute("create table tabel1 (date, number, name)") 
tt1 = ('2007-10-11', '1', 'aaa')
cur.execute("""insert into tabel1 (date, number, name) values(?,?,?)""", tt1)
con.commit()
cur.close()
con.close()