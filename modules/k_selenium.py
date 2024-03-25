from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
debug=[False,True][1]#True
import tk_ui as ui
#driver = webdriver.Firefox()
import time
import json
import k_err
from k_err import xxprint,xprint,xxxprint
chrome_options = webdriver.ChromeOptions()
if 1==1:#chorome
    settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "isGcpPromoDismissed":False,
            "selectedDestinationId": "Save as PDF",
            "version": 2,

        }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
             "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome}
        "savefile.default_directory":"C:\\Users\\k.saadati\\Downloads\\"} 
      
    chrome_options.add_experimental_option('prefs', prefs)
    for tt in ["--kiosk-printing" , "--window-size=800,850", "--window-position=810,0","--disable-infobars"]:# ,--headless-for-tests"]:# ,--kiosk
        chrome_options.add_argument(tt)
    chrome_options.add_experimental_option('prefs', {
    #"download.default_directory": "C:/Users/XXXX/Desktop", #Change default directory for downloads
       "download.prompt_for_download": False, #To auto download the file
       "download.directory_upgrade": True,
       "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
     })
    #driver = webdriver.Chrome(executable_path=r"C:\webdriver\chromedriver.exe",options=chrome_options)
    #chrome_options.binary_location =r'C:\webdriver\chromedriver.exe'
    driver = webdriver.Chrome(options=chrome_options)
else:
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    #options.add_argument("download.default_directory=C:\\temp")
    driver = webdriver.Firefox(options=options)#,executable_path="C:\\temp\\geckodriver.exe")
actions = ActionChains(driver)
class Kselenium():
    xx="xx"
    #driver.get("http://93.115.149.30/RAVAN/UI/index.php") # automation 
    def __init__(self,url):
        driver.get(url)
    def find_element_trace(self,_xpath):
        from selenium.common.exceptions import NoSuchElementException
        from selenium.webdriver.common.by import By
        xp=_xpath
        while True:
            try:
                elm=driver.find_element(By.XPATH,xp)
                xprint("xpath search \n {} \n founded".format(xp))
                break
            except NoSuchElementException:
                xp1=xp.rpartition("/")[0]
                ui.msg("xpath search \n  {} \n not founded \n ------------ \n search for: \n {}".format(xp,xp1)) 
                xp=xp1
        return elm  
    def find_element(self,_id,_xpath):
        from selenium.webdriver.common.by import By
        #try:
        if 1==1:
            if _xpath=='':
                x=driver.find_element(By.ID,_id)
                
            else:
                x= driver.find_element(By.XPATH,_xpath)
        return x
        #except:
        #    return False
    def wait_click(self,_id='',msg='',_xpath='',click=True,retry=True):
        el,_id,_xpath=self.wait_for(_id=_id,msg=msg,_xpath=_xpath)
        xxxprint(msg=['start',msg,''],vals={'xpath':_xpath,'id':_id})
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        t=0
        while True:
            t+=1
            try:
                if _xpath=='':
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, _id)))
                else:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, _xpath)))
                element = self.find_element(_id,_xpath)
                if element:
                    #self.element_screen_shot(element)
                    break   
                else:
                    if t<5:
                        ui.msg('wait_click : find_element => false\n' + str(t)+"\n"+str([_id,_xpath,msg]))
                    else:
                        html_el=driver.find_element(By.TAG_NAME,"html")
                        html_t = html_el.get_attribute('innerHTML')
                        res,_id,_xpath=err_handel(_id,_xpath,msg,html_t)    
            except Exception as err:
                # if debug : breakpoint()
                if not retry:
                    xxprint ('','wait_click : not reply')
                    return False
                if t<5 : 
                    time.sleep(1)
                else:
                    html_el=driver.find_element(By.TAG_NAME,"html")
                    html_t = html_el.get_attribute('innerHTML')
                    res,_id,_xpath=err_handel(_id,_xpath,msg,html_t)
                    if not res:return False
                #element = self.find_element(_id,_xpath)
        xxxprint(msg=['element','find_element - step1',''],
                         vals={'id':_id,'xpath':_xpath},vals2=self.report_element(element))
        time.sleep(1)       
        if click:
            i=0
            while True:
                i+=1
                try: 
                    element.click() # - By.XPATH
                    break
                except Exception as err:
                    #if debug : breakpoint()
                    if i==1:
                        element = self.find_element(_id,_xpath)
                    else:
                        html_el=driver.find_element(By.TAG_NAME,"html")
                        html_t = html_el.get_attribute('innerHTML')
                        res,_id,_xpath=err_handel(_id,_xpath,msg,html_t)                        

                        if not res:return False
                        element = self.find_element(_id,_xpath)
                
                xxxprint(msg=['element','find_element - step2',''],
                         vals={'id':_id,'xpath':_xpath},vals2=self.report_element(element))
        xxxprint(msg=['end','clicked ok',''],vals={'_xpath':_xpath,'_id':_id,'msg':msg})
        return element
    def wait_for(self,_id='',msg='',_xpath='',user_prompt=True):
        '''
            input
            -----
                _xpath:str or list
            output
            ------
                result:boolean
                    True/False
                xp:str
                    finded xpath
                    
                
        '''
        xxxprint(msg=['start',msg,''],vals={'xpath':_xpath,'id':_id})
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        t=0
        while True:
            t+=1
            try:
                #element = self.find_element(_id,_xpath)
                if not _xpath:
                    el=driver.find_element(By.ID,_id)
                    xxxprint(msg=['element','find_element_by_id:',_id],vals=self.report_element(el))
                    return el,_id,_xpath
                else:
                    if type(_xpath)==str:
                        el=driver.find_element(By.XPATH,_xpath)
                        xxxprint(msg=['element','find_element_by_xpath:',_xpath],vals=self.report_element(el))
                        return el,_id,_xpath
                    else: #type(_xpath)=list
                        for xp in _xpath:
                            try:
                                xprint('-123-'+xp)
                                el=driver.find_element(By.XPATH,xp)
                                if el:
                                    
                                    xxxprint(msg=['element','find_element_by_xpath:',xp],vals=self.report_element(el))
                                    return el,_id,xp
                            except:
                                pass
                    
                    
                '''
                if _xpath=='':
                    element = WebDriverWait(driver, 1).until(EC.element_to_be_selected((By.ID, _id)))
                else:
                    element = WebDriverWait(driver, 1).until(EC.element_to_be_selected((By.XPATH, _xpath)))
                ''' 
                break
            except Exception as err:
                #if debug : breakpoint()
                if t<3 : 
                    xxxprint(cat=['driver titel','',''],msg=['err-'+str(t),'t<3',str(err)],
                             args=self.titles())
                    self.titles('err-'+str(t),str(err))# xxxprint
                    time.sleep(1)
                else:
                    if True: #user_prompt:
                        xxxprint(cat=['driver titel','',''],msg=['err-'+str(t),'else',str(err)],
                                 args=self.titles())
                        #k_err.show()
                        html_el=driver.find_element(By.TAG_NAME, "html")
                        html_t = html_el.get_attribute('innerHTML')
                        res,_id,_xpath=err_handel(_id,_xpath,msg,html_t)
                        if not res:return False
                        #-------------------------------------
                        '''
                        t=0
                        if not ui.msg('kselenium-wait_for:\n_id={}\nmsg={}\n_xpath={}\n wait for selected \n click me when it is shown '.format(_id,msg,_xpath) ,'yesno'):
                            return False
                        xx=ui.input([['_id',_id],['_xpath',_xpath]])
                        _id=xx["_id"]
                        _xpath=xx["_xpath"]
                        '''
                    else:
                        return False,_id,_xpath
                    #element = self.find_element(_id,_xpath)
        return True,_id,_xpath
    
    def send_keys(self,keys_text_list):
        from selenium.webdriver.common.keys import Keys
        t=""
        actions.reset_actions()
        for k in keys_text_list.split(","):
            t+=f".send_keys({k})"
        t=f"actions{t}"
        exec(t)
        actions.perform()
        #actions.send_keys(un).send_keys(Keys.TAB).send_keys(ps).send_keys(Keys.RETURN).perform()
        #k_slnm.send_keys(f'"{un}",Keys.TAB,"{ps}",Keys.RETURN')
    def print(self):
        ui.msg("kselenium print function is delete")
        #driver.execute_script('window.print();')
    def close(self):
        driver.close()
    def title(self):
        try:
            return driver.title
        except Exception as err:
            if debug : breakpoint()
            return ''
    def cur_win():
        '''
            detect Current Window ID in selenium browser
            output:
                [cur_win_id,cur_win_title]
                cur_win_id : Current Window ID
                cur_win_title : Current Window Title
        '''
        while True:
            try:
                cur_win_id = driver.current_window_handle
                break  
            except Exception as err:
                tx1='err on cuurent window access:'
                tx2="""
                    ÔäÇÓÇíí äÌÑå ÝÚÇá ÈÇ ãÔ˜á ãæÇÌå ÔÏå ÇÓÊ
                    --
                    áØÝÇ Ó ÇÒ ÔäÇÓÇíí æ Íá ãÔ˜á Ï˜ãå ok ÑÇ ÈÒäíÏ 
                    """
                xxxprint(msg=['err',tx1,tx2],err=err)
                xc=ui.ask(tx1+'\n',tx2,['cancel & next','breakpoint','play - go'])
                if xc=='breakpoint':breakpoint()
                elif xc=='cancel & next':return ''
                if debug : breakpoint()
        '''              
        titles=self.titles()
        if cur_win_id not in titles: # cur_win_id in ids of titels
            ui.msg("
                äÌÑå ãæÌæÏ ÏÑ áíÓÊ äÌÑå åÇí ÔäÇÓÇíí ÔÏå äãí ÈÇÔÏ
                ÈÑÇí ÈÑÑÓí ÈíÔÊÑ ÈÑäÇãå ÏÑ ÍÇáÊ breakpoint ÇÏÇãå ãí íÇÈÏ
            ")
            breakpoint()
            self.cur_win()
        '''    
        return [cur_win_id,self.title()]#titles[cur_win_id]]
        
    def titles(self,msg1='',msg2=''):#report_titles
        '''report titels'''
        while True:
            try:
                chwnd = driver.window_handles
                o1={}
                i=0
                for w in chwnd:
                    i+=1
                    driver.switch_to.window(w)
                    o1[w]=self.title()
                break
            except Exception as err:
                tx1='err in switch win:'
                tx2="""
                    ÏÑ ÔäÇÓÇíí ÊÇíÊá ÊÈ åÇí ÈÇÒ ãÔ˜á æÌæÏ ÏÇÑÏ
                    ÇÍÊãÇáÇ í˜ ãÔ˜á ãËá í˜ ÑíäÊ ÏÑ ÍÇá ÇäÌÇã æÌæÏ ÏÇÑÏ
                    áØÝÇ Ó ÇÒ ÔäÇÓÇíí æ Íá ãÔ˜á Ï˜ãå ok ÑÇ ÈÒäíÏ 
                    """
                xxxprint(msg=['err',tx1,tx2],err=err)
                xc=ui.ask(tx1+'\n'+tx2,['play - go','cancel & next','breakpoint',])
                if xc=='breakpoint':breakpoint()
                elif xc=='cancel & next':break
        return o1
    def switch_by_title(self,title):
        p = driver.current_window_handle
        chwnd = driver.window_handles
        for w in chwnd:
                #switch focus to child window
                if(w!=p):
                    driver.switch_to.window(w)
                    xprint(driver.title)
                    if driver.title==title:
                        return
    def switch_window(self,close_cur_win=False,title=''):
        p = driver.current_window_handle
        
        find=False
        i=0
        while not find: # retry 5 time by delay 1 secend
            chwnd = driver.window_handles
            xprint(f'switch_window-num of win ={len(chwnd)}')
            i+=1        
            for w in chwnd:
                #switch focus to child window
                if(w!=p):
                    if title!='':
                        if self.title()==title:
                            find=True
                    else:
                        find=True
                    if find:    
                        if close_cur_win:driver.close()
                        driver.switch_to.window(w)
                        tit=self.title()
                        xprint(f'window titel={tit}')
                        break
            if not find:
                if i<6:
                    time.sleep(1)
                else:
                    x=ui.ask('Error: func(switch_window) can not do switch the window',['retry','countiue','end'])
                    if x=='retry':i=0
                    elif x=='countiue':break
                    elif x=='end':quit()
    #@k_err.check_err               
    def print_v_close_by_title(self,title='',do_print=True):
        import k_file
        @k_err.until_result(True,"1 page print")
        def print_master():
            n,f=k_file.file_count(k_file.downloads_path())
            if n==1:return True
            chwnd = driver.window_handles
            xxxprint(msg=['n ','switch_to.window'],args=chwnd)
            for w in chwnd:
                #switch focus to child window
                if(w!=p):
                    
                    driver.switch_to.window(w)
                    xxxprint(msg=['do ','switch_to.window'],args=[w,p],vals={'title':title,'driver.title':driver.title})
                    if title=='' or driver.title==title:
                        n,f=k_file.file_count(k_file.downloads_path()) 
                        xxxprint(msg=['do - print_win-#',n,k_file.downloads_path()],args=f)
                        if n==0: # do_print:
                            xxxprint(msg=['do - print_win--',n,k_file.downloads_path()],args=f)
                            print_win()
                            return True
            return False
        @k_err.until_result(True,"1 file print and exist on download_path")
        def print_win():
            n,f=k_file.file_count(k_file.downloads_path()) 
            if n>0:return True
            try:
                time.sleep(1)
                driver.execute_script('window.print();')
                #driver.execute_script("window.document.execCommand('Save')")
                time.sleep(1)
            except Exception as err:
                if debug : breakpoint()
                pass
                #k_err.show()
            n,f=k_file.file_count(k_file.downloads_path()) 
            xxxprint(msg=['print_win--',n,k_file.downloads_path()],args=f)
            return True if n>0 else False
        def print_win1():
            pdf = driver.execute_cdp_cmd("Page.printToPDF", {
                  "printBackground": True
                    })
            import base64
            with open("c://temp//print.pdf", "wb") as f:
                f.write(base64.b64decode(pdf['data']))
        def close_win1():
            #driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + 'w')
            #self.send_keys(Keys.CONTROL + 'w')
            # print ('driver.title=' + driver.title)        
            # driver.close()
            pass
         
        def close_win(p):
            chwnd = driver.window_handles
            for w in chwnd:
                if(w!=p):
                    try:
                        driver.switch_to.window(w) 
                        driver.close()
                    except Exception as err:
                        if debug : breakpoint()
                        xprint('==error:1 window can not  switch or close (in kselenium.print_v_close_by_title.colse_win)')
        p = driver.current_window_handle
        xxxprint(msg=['titles','print : start'],vals=self.titles())
        print_master()
        #                           try:
        #                               time.sleep(1)
        #                               driver.execute_script('window.print();')
        #                               time.sleep(1)
        #                               
        #                           except:
        #                               ui.msg(f"error : can not => print_v_close_by_title ({title})\n Please Manually do it")
        xxxprint(msg=['titles','close_win : start'],vals=self.titles())
        close_win(p)
        xxxprint(msg=['titles','close_win : end'],vals=self.titles())
        driver.switch_to.window(p)
        x=ui.ask('print_v close - countinue:',['a','b'])
    @k_err.check_err
    def element_screen_shot(self,element,el_file_name_suffix=''):
        ##try:
        from datetime import datetime
        now = datetime.now().strftime("%H%M%S")
        from PIL import Image
        import k_pic
        # take screenshot
        location = element.location
        size = element.size
        driver.save_screenshot("c:\\temp\\pageImage.png")
        # calc region
        x1 = location['x'];
        y1 = location['y'];
        x2 = location['x']+size['width'];
        y2 = location['y']+size['height'];
        region=(int(x1), int(y1), int(x2), int(y2))
        #ui.msg(f"x1={x1},y1={y1}\n x2={x2},y2={y2}")
        if 0==1:
            im = Image.open("c:\\temp\\pageImage.png")
            #im = im.crop(region)
            im=k_pic.highlight_area(im, region, factor=2.5, outline_color='red', outline_width=1)
            im.save(f"c:\\temp\\element-{now}-{el_file_name_suffix}.png")
        ##except:
        #    import k_err
        #    k_err.show()
    def html(self,element):
        return element.get_attribute('innerHTML')
    def exist(self,xpath):
        from selenium.webdriver.common.by import By
        els=driver.find_elements(By.XPATH,xpath)
        return False if len(els)==0 else els[0]
    def input_write(self,_xpath,msg,write_text,_id='',sleep=0,send_enter=False):
        el=self.wait_click(_id=_id,msg=msg,_xpath=_xpath)
        el.clear()
        ent=u'\ue007' if send_enter else ''
        el.send_keys(f"{write_text}"+ ent)
        xxxprint(msg=['send_keys',write_text,msg])
        if sleep>0:time.sleep(sleep)
    def report_element(self,el): #,msg1,msg2='',vals={}):
        #report inf of selenium find element
        try:
            r1={'att_innerHTML':el.get_attribute("innerHTML"),
                'att_textContent':el.get_attribute("textContent"),
                'text':el.text}
        except Exception as err:
            if debug : breakpoint()
            r1={'err':str(err)}
        return r1    
        #r1.update(vals)
        #xxxprint(msg=['result',msg1,msg2],vals=r1)
    def make_pdf():
        response = browser.execute_cdp_cmd('Page.printToPDF', self.template)
        self.log = self.get_log(browser)
        if not response:
            return

        with open(os.path.abspath(os.path.join(self.dir, 'output.pdf')), 'wb') as f:
            f.write(base64.b64decode(response['data']))

        self.success = True 
    #---------------------------------------------------------    
#driver.quit()  
def err_handel(_id,_xpath,msg,html_x):
    x_do={ "retry":{"help":"retry to select element"},
           "correct":{"help":"correct(id ,xpath) then retry"},
           "end":{"help":"end program"},
           "cancel & countinu":{"help":"no need to pro click element - i do it"},
           "debug":{"help":"trace error"}}
    #if debug : breakpoint()
    tx='kselenium-wait_click <error> :\n error=can not select element \n'+'-'*40
    tx+='\n _id='+_id
    tx+='\n _xpath='+str(_xpath)
    tx+='\n msg='+msg
    tx+='\n'+'-'*40+'\n please click => \n'
    tx+='\n'.join([f"{x}:{x_do[x]['help']}" for x in x_do]) 
    b=[x for x in x_do]
    x=ui.ask(tx,b)
    a=x
    print('html','html='+html_x,'',tx)
    xxxprint(msg=['ask','ask='+a,tx])
    if a=="retry":
        return True,_id,_xpath
    elif a=="cancel & countinu":
        return False,'',''
    elif a=="debug":
        k_err._show()
    elif a=="correct":
        _id,_xpath=ui.input([['_id',_id],['_xpath',_xpath]],'tuple')
        return True,_id,_xpath
    elif a=="end":
        k_err.quit()

