'''
Created on 2012-11-20

@author: xizhao
'''
import  web 

render = web.template.render('../templates/')
  
urls = (  
    '/', 'index'  ,
    '/result','result'
)  


elements = []
pronto_list = []
pac_list = []
pac_version = []

class element():
    def __init__(self,id,pronid,title,state,target,cn,modification):
        self.id = id
        self.pronid = pronid
        self.title = title
        self.state = state
        self.target = target
        self.cn = cn
        self.modification = modification
 
class index:  
  
    def GET(self):
        tempelement = element('','','','','','','')
        templist = []
        templist.append(tempelement)
        return render.index(templist)  
      
    def POST(self):
        line = ""
        line_count = 0
#        y = web.input(prontlist={})
        x = web.input(colfile={})
        y = web.input(prontlist={})
        reader = y['prontlist'].file.read().strip().split('\r\n')
        reader_col = x['colfile'].file.read()
        pac_version.append(reader_col)
#        print pac_version
        
        for line in reader:
            line_count += 1
            if (line_count < 9):
                continue
            else:
                id = (line_count - 9)
                pronid = line.split('","')[0][1:]
                title = line.split('","')[4]
                state = line.split('","')[9]
                target = line.split('","')[11]
                cn = line.split('","')[13]
                modification = line.split('","')[14]
                pronto = element(id,pronid,title,state,target,cn,modification)
                pronto_list.append(pronto)
#        for ii in pronto_list:
#            print ii.id
        return render.index(pronto_list)

class result:
    def GET(self):
        pass

    def POST(self):
        selectlist = web.input(releasea=[])
        print selectlist
        targetselected = selectlist["releasea"]        
        filename = selectlist["resultfile"]
        checkselected = selectlist["releasea"]
#       print pac_version
        f = open(filename,'w+')
        print filename
        for line in targetselected:   
            modification_list = pronto_list[int(line)].modification              
            output = "PR" + str(pronto_list[int(line)].id) + pronto_list[int(line)].pronid + pronto_list[int(line)].title + pronto_list[int(line)].modification
            if selectlist.has_key('checkbox4'):
                output += pronto_list[int(line)].cn
            print output
            f.write(output)        
            f.write('\n') 
        f.close()
        
if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run() 
    
    