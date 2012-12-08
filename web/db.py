'''
Created on 2012-11-23

@author: xizhao
'''
import sqlite3

con = sqlite3.connect('correction.db') 
cur = con.cursor()
cur.execute("create table pronto_table(ID, Title, Release,State, CN)")

insert_datas = ('1', 'title_1', 'content_1', 'user_1', '2008-01-01') 
cur.execute("insert into pronto_table(ID, Title, Release, State, CN) values (?, ?, ?, ?, ?)",insert_datas)
con.commit() 
cur.close() 
con.close()

