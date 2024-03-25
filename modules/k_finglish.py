# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 10:15:55 2021

@author: ks
"""
ef2={
'uH':'ح',
'uQ':'غ',
'uT':'ط',
'uZ':'ظ',
'wS':'ث',
'wZ':'ذ',
'yH':'ه',
'yS':'ص',
'yZ':'ض',
'Ch':'چ',
'Kh':'خ',
'Sh':'ش'
   }
ef1={
'0':'۰',
'1':'۱',
'2':'۲',
'3':'۳',
'4':'۴',
'5':'۵',
'6':'۶',
'7':'۷',
'8':'۸',
'9':'۹',
'A':'ا',
'B':'ب',
'D':'د',
'E':'ع',
'F':'ف',
'G':'گ',
'I':'ی',
'J':'ج',
'K':'ک',
'L':'ل',
'M':'م',
'N':'ن',
'P':'پ',
'Q':'ق',
'R':'ر',
'S':'س',
'T':'ت',
'V':'و',
'X':'ژ',
'Z':'ز',
'_':' '
    }
ef1_a={
       'A':'آ',
       'K':'ك',
       'I':'ي'
       }
fe1={ef1[x]:x for x in ef1}
fe2={ef2[x]:x for x in ef2}
fe1_a={ef1_a[x]:x for x in ef1_a}
def fa_to_fin(fa_txt):
	#020801
    if not fa_txt:return ''
    r1=''
    for t in fa_txt:
        if t in fe1:
            r1+=fe1[t]
        elif t in fe2:
            r1+=fe2[t]
        elif t in fe1_a:
            r1+=fe1_a[t]
        else:
            r1+=t
    return r1
def fin_to_fa(fin_txt):
    if not fin_txt:return ''
    r1=fin_txt
    for t in ef2:
        r1=r1.replace(t,ef2[t])
    for t in ef1:
        r1=r1.replace(t,ef1[t])     
    return r1
#print(fin_to_fa(fa_to_fin('سلام صبح بخیر')))
#print(ord(ef1_a['I']))
#print(ord(ef1['I']))