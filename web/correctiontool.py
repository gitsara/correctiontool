'''
Created on 2012-11-20

@author: xizhao
'''
import  web 
import re

render = web.template.render('../templates/')
  
urls = (  
    '/', 'index'
)

handleRegx = {"C.*":"BLCODE",
              "L.*":"BLCODE",
              "S.*":"BLCODE",
              "A.*":"LFILES",
              "D.*":"LFILES",
              "K.*":"LFILES",
              "M.*":"MMDIRE",
              "Y.*":"LFILES",
              "Z0.*":"LFILES"
              }
ignoreRegx = {".*P.*":"ALL",
              "D$":"LFILES",
              "DO$":"LFILES",
              "DB$":"LFILES",
              "DBO$":"LFILES",
              "DI$":"LFILES",
              "DIO$":"LFILES",
              "DIB$":"LFILES",
              "DIBO$":"LFILES",
              "DF$":"LFILES",
              "DFO$":"LFILES",
              "DFB$":"LFILES",
              "DFBO$":"LFILES",
              "DIT$":"LFILES",
              "DITO$":"LFILES",
              "DFT$":"LFILES",
              "DFTO$":"LFILES",
              
              }

class parameter():
    def __init__(self,colfile,prontofile,elements,results):
        self.colfile = colfile
        self.prontofile = prontofile
        self.elements = elements
        self.results = results
        
class element():
    def __init__(self,id,pronid,title,state,target,cn,modification):
        self.id = id
        self.pronid = pronid
        self.title = title
        self.state = state
        self.target = target
        self.cn = cn
        self.modification = modification
 
class target_branch:
    def __init__(self,reader_pronto,reader_col):
        self.reader_pronto = reader_pronto
        self.reader_col = reader_col
        self.element_list = []
        self.all_element_list = []
        self.modification_list = []

        
    def prontolist_key_reader(self):
        line_count = 0
        for line in self.reader_pronto.strip().split('\r\n'):
            line_count += 1
            if (line_count < 7):
                    continue
            else:
                line = line.split('","')
                return line
    def get_prontoid(self):
        line = self.prontolist_key_reader()
        return line.index("\"Problem ID")
    
    def get_title(self):
        line = self.prontolist_key_reader()
        return line.index("Title")

    def get_state(self):
        line = self.prontolist_key_reader()
        return line.index("Correction State")

    def get_target(self):
        line = self.prontolist_key_reader()
        return line.index("Target Build")    
    
    def get_cn(self):
        line = self.prontolist_key_reader()
        return line.index("Change Notes")    
    
    def get_modification(self):
        line = self.prontolist_key_reader()
        return line.index("Modified Components")

    def prontolist_reader(self):
        line_count = 0
        for line in self.reader_pronto.strip().split('\r\n'):
            line_count += 1
            if (line_count < 9):
                    continue
            else:
                id = (line_count - 9)
                pronid = line.split('","')[int(self.get_prontoid())][1:]
                title = line.split('","')[int(self.get_title())]
                state = line.split('","')[int(self.get_state())]
                target = line.split('","')[int(self.get_target())]
                cn = line.split('","')[int(self.get_cn())]
                modification = line.split('","')[int(self.get_modification())]
                pronto = element(id,pronid,title,state,target,cn,modification)
                self.all_element_list.append(pronto)
                if not self.modification_list.__contains__(modification):
                    self.modification_list.append(modification)                   
                    self.element_list.append(pronto)
            
class result:
    def __init__(self,selectedlist,pronto_list,col_txt):
        
        self.all_selected = selectedlist
        self.selectedlist = selectedlist["releasea"]
        self.pronto_list = pronto_list
        self.col_txt = col_txt
        self.pac_list = []
        self.result_txt = []
        self.temp_txt = []
        self.final_txt = []
        self.need_check_list = []      
    def get_pac_list(self):       
        if self.selectedlist =="":
            print "NO branch selected"       
        else:
            for line in self.selectedlist:
                if not self.pronto_list[int(line)].state == "Tested" and not self.pronto_list[int(line)].state == "Testing Not Needed":
                    continue
                if self.pronto_list[int(line)].modification.__contains__("BOP") or self.pronto_list[int(line)].modification.__contains__("PBO") or self.pronto_list[int(line)].modification.__contains__("FBO") or self.pronto_list[int(line)].modification.__contains__("CBO"):
                    continue
                modifications = self.pronto_list[int(line)].modification
                if modifications.__contains__(","):
                    for pac in modifications.split(","):
                        if not pac.__contains__(".PAC") and not pac.__contains__(".IMG") and not pac.__contains__(".XML") and not pac.__contains__(".BIN"):
                            continue
                        if self.pac_list.__contains__(pac.strip()):
                            continue
                        else:
                            self.pac_list.append(pac.strip())
                else:
                    if modifications.__contains__(".PAC") or pac.contains__(".IMG") or pac.contains(".XML") or pac.contains(".BIN"):
                        if self.pac_list.__contains__(modifications.strip()):
                            continue
                        else:
                            self.pac_list.append(modifications.strip())
        self.uniq_pac_list()
        self.check_pacname_col_file()
        self.check_pacversion_col_file()
        
    def uniq_pac_list(self):
        for pac in self.pac_list:
            self.temp_txt.append(pac)        
        if self.pac_list =="":
            print "No Pac"
        else:
            for el in self.temp_txt:
                pac = pacs(el)
                for al in self.temp_txt:
                    other_pac = pacs(al)
                    if pac.compare_pac(other_pac):
                        if self.pac_list.__contains__(al):
                            self.pac_list.remove(al)
        self.temp_txt=[]                
    
    def check_pacname_col_file(self):
        for pac in self.pac_list:
            self.temp_txt.append(pac)
        for pac in self.temp_txt:
            el = pacs(pac)
            if self.col_txt.__contains__(el.pacname.split(".")[0]):
                pass
            else:
                needcheck = pac + "not in colfile\n"
                self.pac_list.remove(pac)
                self.need_check_list.append(needcheck)
        self.temp_txt=[]
        
    def check_pacversion_col_file(self):
        for pac in self.pac_list:
            self.temp_txt.append(pac)   
        for pac in self.temp_txt:
            el= pacs(pac)
            for col_line in self.col_txt.split("\n"):
                if col_line.__contains__(el.pacname.split(".")[0]):
                    version_in_col = col_line.split("!")[3].strip()
                    otherpac = str((el.pacname + " " + version_in_col)).encode('utf-8')
                    other_pac = pacs(otherpac)            
                    if el.compare_version(other_pac):
                        break
                    else:
                        self.pac_list.remove(pac)                        
                        break 
        self.temp_txt=[] 
    def get_final_list(self):
        for pac in self.pac_list:
            for pronto in self.pronto_list:
                if pronto.modification.__contains__(pac):
                    type_info =  self.get_handle_type(pac) 
                    if self.all_selected.has_key('checkbox4'):
                        info_txt =  pac + "\t" + type_info + "\t" + pronto.pronid + "\t" + pronto.title + "\t" + pronto.cn
                    else:
                        info_txt =  pac + "\t" + type_info + "\t" + pronto.pronid + "\t" + pronto.title
                    self.final_txt.append(info_txt)
                    break
        self.final_txt.append("need to check:\n")
        for check in self.need_check_list:
            self.final_txt.append(check)        
        print self.final_txt
    def get_handle_type(self,pac):   
            el= pacs(pac)
            for col_line in self.col_txt.split("\n"):
                if col_line.__contains__(el.pacname.split(".")[0]):
                    el.handle = col_line.split("!")[0].strip()[1:]
                    el.type = el.get_type()
                    return el.type
                               
class pacs:
    def __init__(self,pac):
        self.pac = pac
        self.pacname = self.pac.split(" ")[0]
        self.pacversion = self.pac.split(" ")[1]
        self.version = int(self.pacversion.strip().split(".")[0])
        self.edition = int(self.pacversion.strip().split(".")[1].split("-")[0])
        self.repair = int(self.pacversion.strip().split(".")[1].split("-")[1])
        self.handle = ""
        self.type = ""
    def compare_pac(self,other_pac):
        if self.pacname == other_pac.pacname:
            if self.compare_version(other_pac):
                return True
            else:
                return False
        else:
            return False
    def compare_version(self,other_pac):
        if self.version > other_pac.version :
            return True
        elif self.version == other_pac.version:
            if self.edition > other_pac.edition:
                return True
            elif self.edition == other_pac.edition:
                if self.repair > other_pac.repair:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False   
             
    def get_type(self):
            shouldIgnore = False
            for regx in handleRegx:
                if re.match(regx,self.handle):
                    for ignRegx in ignoreRegx:
                        if ignoreRegx.get(ignRegx) <> 'ALL' and ignoreRegx.get(ignRegx) <> handleRegx.get(regx):
                            continue
                        if re.match(ignRegx,self.handle):
                            shouldIgnore = True
                    if not shouldIgnore:
                        return handleRegx.get(regx)
                    
            return "Can't find Handle Type."                       
    
class index:  
    def GET(self):
        return render.index(parameter(None,None,None,None))  
      
    def POST(self): 
        param = parameter(None,None,None,None) 
        input_data = web.input()                        
        if (input_data.has_key('loading')):
            col_txt = web.input(colfile={})['colfile'].value
            pronto_txt = web.input(prontlist={})['prontlist'].value
            param.colfile = col_txt.encode('utf-8')
            param.prontofile = pronto_txt.encode('utf-8')            
            get_target = target_branch(pronto_txt,col_txt)
            get_target.prontolist_reader()
            param.elements = get_target.element_list

        else:
            col_txt = input_data.get('colfiletxt')
            pronto_txt = input_data.get('prontofiletxt')
            get_target = target_branch(pronto_txt,col_txt)
            get_target.prontolist_reader()
            pronto_list = get_target.all_element_list
            selectlist = web.input(releasea=[])
            result_list = result(selectlist,pronto_list,col_txt)
            result_list.get_pac_list()
            result_list.get_final_list()
            param.colfile = None
            param.prontofile = None
            param.elements = None
            param.results = result_list.final_txt            
        return render.index(param)

if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run() 
    