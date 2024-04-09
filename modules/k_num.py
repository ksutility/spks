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
    snls=[] #list of smart_num_list_slice in num format :'1,4-7,8 => [[1],[4,7],[8]]
    def __init__(self,smart_num_list=''): 
        '''
        inputs:
        ------
            smart_num_list:str / list
                smart num list in text / list
        '''
        if smart_num_list:self.add(smart_num_list)
            
    def add(self,new_smart_num_list):
        '''
        inputs:
        ------
            new_smart_num_list:str / list
                new smart num list in text / list
        '''
        def combine(l1,l2):
            if l2[0]>l1[-1]+1:
                return l1,l2	
            else:
                return [l1[0],max(l1[-1],l2[-1])],None
        #------------------------------------------------	
        if type(new_smart_num_list) ==str:
            sn=self.snls+[[int(y) for y in x.split("-")] for x in new_smart_num_list.split(",")]
        elif type(new_smart_num_list) == list:
            sn=self.snls+[[int(x)] for x in new_smart_num_list if x not in [None,'None']] 
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
        self.snls=sn
        return self
    def __str__(self):
        #list=>smart_num_list_txt
        r1=""
        for x in self.snls:
            r1+= f",{x[0]}"
            if len(x)>1 : 
                r1+= f"-{x[1]}"
        return r1[1:]
    def max(self):
        if self.snls:
            return self.snls[-1][-1]
        return -1
    def len(self):
        l=0
        for x in self.snls:
            l+=x[-1]-x[0]+1
        return l
#-------------------------------------------------
#====================================================== not used ===========================================================================
def limit_x (x_father,x,x_min,x_max):
	if x > x_max :
		x_father=x_father+1
		x=x-x_max
	if x < x_min :
		x_father=x_father-1
		x=x+x_max
        
if __name__ == "__main__":
    x=SMART_NUM_LIST("1-5,6-10,12-14")
    print(str(x))#.str__())
    print(x.max())
    print(x.len())
    x=SMART_NUM_LIST([1,2,5,6,7,3])
    print(str(x))
    print(x.max())
    print(x.len())
    x=SMART_NUM_LIST(None)
    print(str(x))
    print(x.max())
    print(x.len())

