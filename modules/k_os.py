def run_cmd(x_cmd):   
    try:
        import os
        xxx=os.popen(x_cmd).read()
        return {'ok':True,'inf':x_cmd+"<hr>"+"<br>".join(xxx.split("\n"))}
    except:   
        return {'ok':False,'inf':x_cmd+"<hr>"+"<br>".join(x_cmd.split("\\"))}  
