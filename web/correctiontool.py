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
col = []
need_check = []

class index:  
  
    def GET(self):
        return render.index(())  
      
    def POST(self):
        line = ""
        line_count = 0
#        y = web.input(prontlist={})
        x = web.input(colfile={})
        y = web.input(prontlist={})
        reader = y['prontlist'].file.read().strip().split('\r\n')
        reader_col = x['colfile'].file.read()
        col.append(reader_col)
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
            output = " "   
            modification_list = pronto_list[int(line)].modification
            print modification_list
            if modification_list.__contains__(","):                
                for pac in modification_list.split(","):
                    if  checkpac(pac,col):                       
                        output += pac.strip() + " " + pronto_list[int(line)].pronid + " " + pronto_list[int(line)].title                 
            elif checkpac(modification_list,col):               
                output = pronto_list[int(line)].modification.lstrip() +" " +  str(pronto_list[int(line)].id) +" " +  pronto_list[int(line)].pronid + " " + pronto_list[int(line)].title 
                
                
            if selectlist.has_key('checkbox4'):
            output += " " + pronto_list[int(line)].cn
            f.write(output)        
            f.write('\n')
        f.close()
        raise web.seeother('/')
        
class element():
    def __init__(self,id,pronid,title,state,target,cn,modification):
        self.id = id
        self.pronid = pronid
        self.title = title
        self.state = state
        self.target = target
        self.cn = cn
        self.modification = modification
def checkversion(pacname,pacversion,colfile):
    for col_line in colfile.split("\n"):
        if col_line.__contains__(pacname):
            current_version = col_line.split("!")[3]
            print current_version
            return True
            
    return False     
                    
def checkpac(pac,col):
    col_file = " "
    pacname = pac.split(" ")[0][0:8]
    if pacname.__contains__("CBO") or pacname.__contains__("FlashBoot") or pacname.__contains__("BOP"):
        return False
    colfile = col[0]
    if colfile.__contains__(pacname):
        pacversion = pac.split(" ")[1]
        if checkversion(pacname,pacversion,colfile):         
            return True
        else:
            return False
    else:
        info = "%s not in col" %(pacname)
#        need_check.append(info) 
        return False
        
if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run() 
    