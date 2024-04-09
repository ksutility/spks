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
    '''
    goal:
        make a new smart_num_list by add new_num to in_smart_num_list
    test unit:
        Usage examples:
        >>>x=SMART_NUM_LIST("1-5,6-10,12-14")
        >>>str(x)
        1-10,12-14
        >>>str(x.add('11'))
        '1-14'
        >>>str(x.add('16'))
        '1-14,16'
        >>>str(SMART_NUM_LIST("1-5,6-10,12-14").add("11"))
        '1-14'
        >>>str(SMART_NUM_LIST("1-5,6-10001,12-14").add("15"))
        '1-10001'
        >>>str(SMART_NUM_LIST("1-5,8,1-12").add("20"))
        '1-12,20'
'''	
    num_list=[] #smart_num_list
    def __init__(self,smart_num_list=''): 
        '''
        inputs:
        ------
            smart_num_list:str
                smart num list in text
        '''
        if smart_num_list:self.add(smart_num_list)
    def add(self,new_smart_num_list):
        '''
        inputs:
        ------
            smart_num_list:str
                new smart num list in text
        '''
        def combine(l1,l2):
            if l2[0]>l1[1]+1:
                return l1,l2	
            else:
                return [l1[0],max(l1[-1],l2[-1])],None
        #------------------------------------------------		 
        sn=self.num_list+[[int(y) for y in x.split("-")] for x in new_smart_num_list.split(",")]
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
        self.num_list=sn
        return self
    def __str__(self):
        #list=>smart_num_list_txt
        r1=""
        for x in self.num_list:
            r1+= f",{x[0]}"
            if len(x)>1 : 
                r1+= f"-{x[1]}"
        return r1[1:]
    def max(self):
        return max(self.num_list)
    def len(self):
        return len(self.num_list)
        
#-------------------------------------------------
#====================================================== not used ===========================================================================
def limit_x (x_father,x,x_min,x_max):
	if x > x_max :
		x_father=x_father+1
		x=x-x_max
	if x < x_min :
		x_father=x_father-1
		x=x+x_max

x=SMART_NUM_LIST("1-5,6-10,12-14")
print(str(x))#.str__())
