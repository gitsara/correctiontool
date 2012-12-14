'''
Created on 2012-11-20

@author: xizhao
'''
import  web 
import re

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
        x = web.input(colfile={})
        y = web.input(prontlist={})
        reader = y['prontlist'].file.read().strip().split('\r\n')
        reader_col = x['colfile'].file.read()
        col.append(reader_col)
        
        for line in reader:
            line_count += 1
            if (line_count < 9):
                continue
            else:
#                print line
                id = (line_count - 9)
                pronid = line.split('","')[0][1:]
                title = line.split('","')[4]
                state = line.split('","')[9]
                target = line.split('","')[11]
                cn = line.split('","')[13]
                modification = line.split('","')[14]
                pronto = element(id,pronid,title,state,target,cn,modification)
                pronto_list.append(pronto)

        return render.index(pronto_list)

class result:
    def GET(self):
        pass

    def POST(self):

        selectlist = web.input(releasea=[])
        targetselected = selectlist["releasea"]      
        filename = selectlist["resultfile"]
        checkselected = selectlist["releasea"]
        f = open(filename,'w+')
        for line in targetselected:
            output = ""
            if pronto_list[int(line)].state == "Tested" or pronto_list[int(line)].state == "Testing Not Needed":
                type = ""   
                modification_list = pronto_list[int(line)].modification
                if modification_list.__contains__(","):                
                    for pac in modification_list.split(","):
                        if  checkpac(pac.strip(),col):
                            handle = gethandle(pac.strip(),col)[1:]
                            if handle:                                
                                type = gettype(handle)                       
                            output += pac.strip() + "\t" + type + "\t"  + pronto_list[int(line)].pronid + "\t" + pronto_list[int(line)].title 
                            if selectlist.has_key('checkbox4'):
                                output += "\t" + pronto_list[int(line)].cn + "\n"
                            else:
                                output += "\n"
                                               
                elif checkpac(modification_list.strip(),col):  
                    handle = gethandle(pac.strip(),col)[1:] 
                    if handle:
                        type = gettype(handle)            
                    output = pronto_list[int(line)].modification.strip() +"\t" + type + "\t" +  pronto_list[int(line)].pronid + "\t" + pronto_list[int(line)].title  
                    if selectlist.has_key('checkbox4'):
                        output += "\t" + pronto_list[int(line)].cn + "\n"
                    else:
                        output += "\n"         

            f.write(output)  
        f.write("\n")
        f.write("need to confirm:")
        for check in need_check:
            f.write(check)
            f.write("\n")     
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
    pac_v = pacversion.strip().split(".")[0]
    pac_e = pacversion.strip().split(".")[1].split("-")[0]
    pac_r = pacversion.strip().split(".")[1].split("-")[1]
    for col_line in colfile.split("\n"):
        if col_line.__contains__(pacname):
#            print col_line.split("!")
            current_version = col_line.split("!")[3]
            current_v = current_version.strip().split(".")[0]
            current_e = current_version.strip().split(".")[1].split("-")[0]
            current_r = current_version.strip().split(".")[1].split("-")[1]
            if pac_v > current_v:
                return True
            elif pac_v == current_v and pac_e > current_e:
                    return True
            elif pac_v == current_v and pac_e == current_e and pac_r > current_r:
                return True
                
            else:
                return False
                
                    
def checkpac(pac,col):
    if not pac.__contains__(".PAC") and not pac.__contains__(".IMG"):
        return False
#    elif not pac.__contains__(".PAC") and pac.__contains__(".IMG"):
#        pac = pac.replace('IMG','PAC')
    pacname = pac.split(" ")[0].split(".")[0].strip()
    if pacname.__contains__("CBO") or pacname.__contains__("FlashBoot") or pacname.__contains__("BOP"):
        return False
    colfile = col[0]
    if colfile.__contains__(pacname):
        pacversion = pac.split(" ")[1]
        if checkversion(pacname,pacversion,colfile):         
            return True
    else:
        need_check_info = pac + "not in col file"
        need_check.append(need_check_info)
        return False

def gethandle(pac,col):
    handle = ""
    colfile = col[0]
    pacname = pac.split(" ")[0].split(".")[0].strip()
    for col_line in colfile.split("\n"):
        if col_line.__contains__(pacname):
            handle = col_line.split("!")[0].strip()
    return handle

handleRegx = {"C.*":"BLCODE",
              "L.*":"BLCODE",
              "S.*":"BLCODE",
              "A.*":"LFILES",
              "D.*":"LFILES",
              "K.*":"LFILES",
              "M.*":"MMDIRE",
              "Y.*":"EXTRA",
              }
ignoreRegx = {".*P.*":"ALL",
              "D":"LFILES",
              "DO":"LFILES",
              "DB":"LFILES",
              "DBO":"LFILES",
              "DI":"LFILES",
              "DIO":"LFILES",
              "DIB":"LFILES",
              "DIBO":"LFILES",
              "DF":"LFILES",
              "DFO":"LFILES",
              "DFB":"LFILES",
              "DFBO":"LFILES",
              "DIT":"LFILES",
              "DITO":"LFILES",
              "DFT":"LFILES",
              "DFTO":"LFILES",
              
              }

def gettype(handle):
    shouldIgnore = False
    for regx in handleRegx:
        if re.match(regx,handle):
            for ignRegx in ignoreRegx:
                if ignoreRegx.get(ignRegx) <> 'ALL' and ignoreRegx.get(ignRegx) <> handleRegx.get(regx):
                    continue
                if re.match(ignRegx,handle):
                    shouldIgnore = True
            if not shouldIgnore:
                return handleRegx.get(regx)
            
    return "Can't find Handle Type."

        
if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run() 
    