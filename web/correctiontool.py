'''
Created on 2012-11-20

@author: xizhao
'''
import  web 
import sqlite3

 
render = web.template.render('../templates/')
  
urls = (  
    '/', 'index'  
)  
 
class index:  
  
    def GET(self):

#        print "OK"
        con = sqlite3.connect("test.db") 
        cur = con.cursor() 
        con.commit()
        cur.execute("select * from tabel1")
        tabel_info = cur.fetchall()
#        print(tabel_info)
        return render.index(tabel_info)
        cur.close() 
        con.close()
        return "OK"
    
    def POST(self):
        i = web.input("form1")
        return i.title()

  
if __name__ == "__main__":  
    app = web.application(urls, globals())  
    app.run() 