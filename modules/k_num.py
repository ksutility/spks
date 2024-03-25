#smart_num_list = a text that show list of numbers :	(example= 1-5,8,1-12,20)
		#syntax	:	number "-" ","
			#","	:	splite the sections in smart_num_list
			#each section in smart_num_list is 2 case
				#case 1: a single number (example= 5 )
				#case 2: a range of serial Numbers that shows like ("n1-n2")
						#n1: start / small number in serial numbers
						#n2: end / big number in serial numbers
						#- : const character for show serial numbers 
class SMART_NUM_LIST():
    #snl=smart_num_list
    #make a new smart_num_list by add new_num to in_smart_num_list
    snl=[]
    def __init__(self,snl_txt=''): 
        '''
        inputs:
        ------
            snl_txt:str
                smart num list in text
        '''
        if snl_txt:self.add(snl_txt)
    def add(self,new_snl_txt):
        def combine(l1,l2):
            if l2[0]>l1[1]+1:
                return l1,l2	
            else:
                return [l1[0],max(l1[-1],l2[-1])],None
        #------------------------------------------------		 
        sn=self.snl+[[int(y) for y in x.split("-")] for x in new_snl_txt.split(",")]
        #sort
        sn.sort(key=lambda x: x[0])
        #compine
        i=0
        while i<len(sn)-1:
            c1,c2=combine(sn[i],sn[i+1])
            if c2==None :
                del sn[i+1]
                sn[i]=c1
                continue
            elif c1==sn[i] and c2==sn[i+1]:
                i+=1
                continue
            else:
                print (f"error i={i}\n sn[i]={sn[i]},sn[i+1]={sn[i+1]} \n c1={c1},c2={c2}")
        self.snl=sn
        return self
    def __str__(self):
        #list=>smart_num_list_txt
        r1=""
        for x in self.snl:
            r1+= f",{x[0]}"
            if len(x)>1 : 
                r1+= f"-{x[1]}"
        return r1[1:]
#-------------------------------------------------
#====================================================== not used ===========================================================================
def limit_x (x_father,x,x_min,x_max):
	if x > x_max :
		x_father=x_father+1
		x=x-x_max
	if x < x_min :
		x_father=x_father-1
		x=x+x_max
'''
test unit:
    Usage examples:
    >>>x=SMART_NUM_LIST("1-5,6-10,12-14")
    >>>str(x)
    1-10,12-14
    >>>x.add('11')

    x.add('11')
    x.add('16').str()='1-16'
	SMART_NUM_LIST("1-5,6-10,12-14").add("11").str())='1-14'
	SMART_NUM_LIST("1-5,6-10001,12-14").add("15").str()='1-10001'
	SMART_NUM_LIST("1-5,8,1-12").add("20").str()='1-12,20'
'''	
x=SMART_NUM_LIST("1-5,6-10,12-14")
print(str(x))#.str__())
