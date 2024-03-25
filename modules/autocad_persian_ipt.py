#!/usr/bin/env python
#acp=autocad_persian
#01/06/10  cen,end,start,single  = -x-, x-,-x , x 
inf={       'لا':{'b': 10  ,'join':'10','kateb': [227, 227, 227, 227]},
            'آ':{'b': 1570,'join':'00','kateb': [69,68,68,69]},
            'ا':{'b': 1575,'join':'01','kateb': [67,67,66,66]},
            'ب':{'b': 1576,'join':'11','kateb': [71,72,73,70]}, 
            'پ':{'b': 1662,'join':'11','kateb': [75,76,77,74]}, 
            'ت':{'b': 1578,'join':'11','kateb': [79,80,81,78]}, 
            'ث':{'b': 1579,'join':'11','kateb': [83,84,85,82]},
            'ج':{'b': 1580,'join':'11','kateb': [87,88,89,86]}, 
            'چ':{'b': 1670,'join':'11','kateb': [91,92,93,90]}, 
            'ح':{'b': 1581,'join':'11','kateb': [95,96,97,94]}, 
            'خ':{'b': 1582,'join':'11','kateb': [99,100,101,98]},
            'د':{'b': 1583,'join':'01','kateb': [103, 103, 102, 102]},
            'ذ':{'b': 1584,'join':'01','kateb': [105, 105, 104, 104]},
            'ر':{'b': 1585,'join':'01','kateb': [107, 107, 106, 106]},
            'ز':{'b': 1586,'join':'01','kateb': [109, 109, 108, 108]},
            'ژ':{'b': 1688,'join':'01','kateb': [111, 111, 110, 110]},            
            'س':{'b': 1587,'join':'11','kateb': [113, 114, 115, 112]},  
            'ش':{'b': 1588,'join':'11','kateb': [117, 118, 119, 116]},
            'ص':{'b': 1589,'join':'11','kateb': [121, 122, 123, 120]}, #ok
            'ض':{'b': 1590,'join':'11','kateb': [125, 126, 161, 124]}, #ok
            'ط':{'b': 1591,'join':'11','kateb': [163, 164, 165, 162]}, #ok
            'ظ':{'b': 1592,'join':'11','kateb': [167, 168, 169, 166]}, #ok
            'ع':{'b': 1593,'join':'11','kateb': [171, 172, 174, 170]}, #ok
            'غ':{'b': 1594,'join':'11','kateb': [177, 178, 179, 176]}, #ok
            'ف':{'b': 1601,'join':'11','kateb': [181, 182, 184, 180]}, #ok
            'ق':{'b': 1602,'join':'11','kateb': [186, 187, 188, 185]}, #ok
            'ک':{'b': 1705,'join':'11','kateb': [190, 191, 192, 189]},
            'گ':{'b': 1711,'join':'11','kateb': [194, 195, 196, 193]},
            'ل':{'b': 1604,'join':'11','kateb': [198, 199, 200, 197]},
            'م':{'b': 1605,'join':'11','kateb': [202, 203, 204, 201]},
            'ن':{'b': 1606,'join':'11','kateb': [206, 207, 208, 205]}, #ok
            'و':{'b': 1608,'join':'01','kateb': [212, 212, 211, 211]},
            'ه':{'b': 1607,'join':'11','kateb': [216, 217, 218, 215]},
            'ی':{'b': 1740,'join':'11','kateb': [224, 225, 226, 223]},
            'ئ':{'b': 1574,'join':'11','kateb': [220, 221,222,219]},
            ',':{'b': 44,'join':'11','kateb': [44,44,44,44]},
            
            
            
            }            
'''
'ن':{'b': 1606,'join':'11','kateb': [107, ['%%160',160], 161, 162]},
for x in inf:
    print(f"{x}:{{'b': {ord(x)}")
'''    
## convert not list (1 item) in each kateb_font_case to list
for x in inf:
    y_list=inf[x]['kateb']
    for i,yi in enumerate(y_list ):
        if type(yi)!=list:
            y_list[i]=[yi]
#print(inf)
##---   
'''
inf={'xp_font_n':{'join':'11','kateb':['kateb_font_1_case_first','kateb_font_1_case_mid','kateb_font_1_case_joined_end','32','kateb_font_1_case_singel_end','32']}
    'join':show can join to befor and after char
        2 char , each char =0 /1
            1:can join
            0:can not join
        exam:
            '11' = can join to befor and after
            '10' = can join to befor and can not join to after chr 
'''
def _report(xx,lable):
    #return
    print("\n"+'+'*50+lable+'\n'+xx)
    ttx="\n\t".join(f'{x} => {ord(x)}' for x in xx)
    print("\n"+'-'*50+'\n\t'+ttx+'\n')

def kateb_2_win(cad_t):
    if not cad_t:
        return ''
    #global inf
    '''
    t1=[ord(x) for x in cad_t]
    o1=''
    for t in cad_t:
        t_ord=ord(t)
        for x_c in inf:
            if t_ord in inf[x_c]:
                o1+=x_c
        else:
            o1+=t
    '''
    #print(cad_t)
    t1=cad_t
    _report(t1,'--:--')
    def x_prepare_1(xx):
        return f'%%{xx}' if type(xx)==int else xx #else=> type str  
    if t1:
        for x_chr in inf:
            for x_ktb_case in inf[x_chr]['kateb']:
                for xa in x_ktb_case : 
                    t1=t1.replace(x_prepare_1(xa),x_chr)
        #ttx="\n".join(f'{x} => {ord(x)}' for x in t1)
        #print(t1+ttx)
        def trans_1(i_chr):
            for x_chr in inf:
                for x_ktb_case in inf[x_chr]['kateb']:
                    if ord(i_chr) in x_ktb_case:
                        return x_chr
            return i_chr
        t2=''.join([trans_1(x) for x in t1])
    else:
        t2=''
    # for xa in x_ktb_case:
        # if type(xa)==int:
        # t1=t1.replace(chr(xa),x_chr)
    #print(t1)        
    return _nums_revers(_prntz_revers(t2))
def win_2_kateb(txt):

     #global inf
    
    _report(txt,'1')
    t0=f' {_nums_revers(txt)} '
    t1=_prntz_revers(t0,xcase='w2k')
    _report(t1,'2')
    t2=''
    for i in range(1,len(t1)-1):
        t=t1[i]
        if t in inf:
            p=kateb_pos(t1[i-1],t1[i+1])
            xx=inf[t]['kateb'][p][0]
            if type(xx)==int:
                t2 += chr(xx)
            elif type(xx)==str:
                t2 += xx
        else:
            t2 += t
    t2=t2.replace('،',',')      
    #t2="a"
    _report(t2,'3')
    return t2
    
def kateb_pos(chr_befor,chr_after):
    t1='0' if not chr_befor in inf else inf[chr_befor]['join'][1]                
    t2='0' if not chr_after in inf else inf[chr_after]['join'][0]
    t3=t1+t2
    cc={'01':0,'11':1,'10':2,'00':3}
    return cc[t3]        
def _nums_revers(t_num):
    import re
    return re.sub('([0-9]+)', lambda m:m.group(0)[::-1], t_num)
#print (_nums_revers('ab12cd3ef4-'))
def _prntz_revers(in_txt,xcase='k2w'):
    '''
    xcase
        w2k =>win 2 kateb
        k2w =>kateb 2 win 
    '''
    xx={'(':')',
        ')':'('
        }    #k2w :kateb 2 win
    if xcase!='k2w':
        xx={y:x for x,y in xx.items()}
    t2=''    
    for t in in_txt:
        if t in xx:
            t2=xx[t]+t2
        else:
            t2=t+t2
    return t2
#print(_prntz_revers('a(bc)'))
