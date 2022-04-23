#!/usr/bin/env python
# coding: utf-8

# In[177]:


from parstdex import Parstdex
import re
from datetime import datetime, timedelta


# In[6]:


get_ipython().system(' pip install parstdex')
get_ipython().system(' pip install re')


# In[8]:



class TimeExtraction(object):
    def __init__(self):
        # model initialization
        self.model = Parstdex()

    def run(self, text):
        result = {}

        spans = self.model.extract_span(text)
        result['spans'] = spans

        markers = self.model.extract_marker(text)
        result['markers'] = markers

        values = self.model.extract_value(text)
        result['values'] = values

        ners = self.model.extract_ner(text)
        result['ner'] = ners

        return result


# In[185]:


extractor = TimeExtraction()
out = extractor.run("   بعد ساعت دو تنبانتیابتا و  ده  دقیقه ونیتابنیتانت  دو ساعت و از  ساعت  دو تا ساعت پنج بعد لبالبب   تا بعد ساعت پنجس  ")
out


# In[184]:


def sum_time(sign,h,m,s):
    now = datetime.now() + sign* timedelta(hours = h, minutes = m, seconds = s )
    return now.timestamp()

def handle_time(time_str):
    hour = 0
    minute =0 
    second = 0
    x = re.search('بعد',time_str) 
    y = re.search('قبل', time_str)
    if x != None :
        if x.end()+1 == len(time_str) :
            
            a = time_str.split()
            
            if a[1] == 'ساعت' :
                hour = int(a[0])
            elif a[1] == 'دقیقه':
                 minute = int(a[0])
            elif a[1] == 'ثانیه':
                    second = int(a[0])
            if len(a) > 4  :    
                if a[3] == 'دقیقه'  :
                    minute = int(a[2])
                elif a[3] == 'ثانیه':
                    second = int(a[2])
            if len(a) > 6 :
                if a[5] == 'ثانیه':
                    second = int(a[4])
                    
            if re.search('یک ربع',time_str)  != None :
                minute = 15
            return sum_time(+1,hour,minute,second)
                
     
                
    elif y != None :
        if y.end()+1 == len(time_str):
            a = time_str.split()
            
            if a[1] == 'ساعت' :
                hour = int(a[0])
            elif a[1] == 'دقیقه':
                 minute = int(a[0])
            elif a[1] == 'ثانیه':
                    second = int(a[0])
            if len(a) > 4  :    
                if a[3] == 'دقیقه'  :
                    minute = int(a[2])
                elif a[3] == 'ثانیه':
                    second = int(a[2])
            if len(a) > 6 :
                if a[5] == 'ثانیه':
                    second = int(a[4])
                    
            if re.search('یک ربع',time_str)  != None :
                minute = 15
            return sum_time(-1,hour,minute,second)
        
    else :
        return self.model.extract_value(time_str)['time']
        
        
    


# In[183]:





# In[93]:


string  ="شنبه این هفته درست در ساعت پنج و چهل و یک دقیقه صدایی بعد "


# In[96]:


x = re.search('بعد',string)


# In[97]:


x ==None


# In[99]:


x.end()


# In[100]:


len(string)


# In[135]:


a =string.split(' ')


# In[136]:


a[1]+a[0]


# In[157]:


'2 ساعت و 5 ثانیه بعد'.split(' ')


# In[ ]:




