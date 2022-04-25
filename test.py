import datetime
from time_extractions import TimeExtraction
from datetime import timedelta
import utility
from datetime import date
import re

def interval_decoder(span):
    span = span[1:-1].split(', ')
    return [int(span[0]), int(span[1])]

def test():
    print(run("من و تو از سه شنبه هفته قبل تا شنبه هفته بعد ساعت دو  به فوتبال میرویم"))

def run(string: str):
    functions = [crontime_handler, time_interval_handler, exact_handler]
    for f in functions:
        result = f(string)
        if result: 
            return result
    return None
def sum_time(sign,h,m,s):
    now = datetime.now() + sign*  timedelta(hours = h, minutes = m, seconds = s )
    return now.time()

def handle_time(time_str):
    hour = 0
    minute =0 
    second = 0
    x = re.search('بعد',time_str) 
    y = re.search('قبل', time_str)
    if x != None :
        if x.end() == len(time_str) :
            
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
        if y.end() == len(time_str):
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
        return datetime.time(int(time_str[0:2]) , int(time_str[3:5]) , int(time_str[6:8]) )
 
def time_interval_handler(string):
    output = {'type': 'duration', 'text': 'token'}
    extractor = TimeExtraction()
    
    result = extractor.run(string)['markers']['datetime']
#     print(result)
    #TODO: find ta

    for x in result.keys():
        if result[x][0:3] == 'تا ':
            ta_index = 0
        elif result[x].find(' تا ') >= 0:
            ta_index = result[x].find(' تا ') + 1
        else:
            continue
        output['span'] = x
        if result[x][0: 3] == 'از ':
            az_index = 3
        else:
            az_index = 0
        first_time = result[x][az_index:ta_index]
        second_time = result[x][ta_index + 3:]
        # print(first_time, second_time)
        #TODO change it to get time and date

        tmp = extractor.run(first_time)['values']['date']
        d1 = date.today()
        for span, datestring in tmp.items():
            d1 = utility.date_decod(datestring)
            first_span = interval_decoder(span)
            first_span[0] += az_index + interval_decoder(x)[0]
            first_span[1] += az_index + interval_decoder(x)[0]
        tmp2 = extractor.run(first_time)['values']['time']

        t1 = datetime.time(0, 0, 0, 0)
        for span, timestring in tmp2.items():
            t1 = handle_time(timestring)
        
        d1 = datetime.datetime.combine(d1, t1)
        d2 = date.today()
                               
        tmp = extractor.run(second_time)['values']['date']
        for span, datestring in tmp.items():
            d2 = utility.date_decod(datestring)
            second_span = interval_decoder(span)
            second_span[0] += ta_index + 3 + interval_decoder(x)[0]
            second_span[1] += ta_index + 3 + interval_decoder(x)[0]
        tmp2 = extractor.run(second_time)['values']['time']

        t2 = datetime.time(0, 0, 0, 0)
        for span, timestring in tmp2.items():
            t2 = handle_time(timestring)

        d2 = datetime.datetime.combine(d2, t2)
        output['value'] = [d1.timestamp(), d2.timestamp()]
        return output

def ctime(time_str) :
    if time_str == '' :
        return '* *'                  
    return time_str[0:2] + ' ' + time_str[3:5]
                               
                               
def crontime_handler(string):
    output = {'type': 'crontime', 'text': 'token'}
    extractor = TimeExtraction()
    result = extractor.run(string)['markers']['datetime']
    
    for x in result.keys():
        crontime_check = re.search('هر', result[x])
        if crontime_check == None :
            return None
        output['span'] = x
                               
        time ='' 
        tmp2 = extractor.run(result[x])['values']['time']
        for span, timestring in tmp2.items():
            time = timestring                     
        time = ctime(time)
        tmp = extractor.run(result[x])['values']['date']
        for span, datestring in tmp.items():
            array = datestring.split(' ')
            for i in range(len(array) ) :
                if array[i] == 'هر' :
                    break
            if array[i+1] == 'روز' :
                output['value'] = time + ' * 0 0'
                return output
            elif array[i+1] == 'شنبه' :
                output['value'] =time + ' * 0 6'
                return output
            elif array[i+1] == 'یکشنبه' :
                output['value'] =time + ' * 0 7'
                return output
            elif array[i+1] == 'دوشنبه' :
                output['value'] = time + ' * 0 1'
                return  output
            elif array[i+1] == 'سه شنبه' :
                output['value'] = time + ' * 0 2'
                return output
            elif array[i+1] == 'چهارشنبه' :
                output['value'] = time + ' * 0 3'
                return output
            elif array[i+1] == 'پنج شنبه' :
                output['value'] = time + ' * 0 4'
                return output
            elif array[i+1] == 'جمعه' :
                output['value'] = time + ' * 0 5'
                return output
            elif array[i+1] == 'ماه' :
                
                x = re.findall('[0-9]+', datestring)
                output['value'] =  time + ' * ' + x[0] + ' *'
                return output
            elif array[i+1] == 'هفته' :
                output['value'] = time + ' * 0 0'
                return output
    return None

def exact_handler(string):
    output = {'type': 'exact', 'text': 'token'}

    extractor = TimeExtraction()

#     print(extractor.run(string))
    result = extractor.run(string)['markers']['datetime']
    for x, y in result.items():
        output['span'] = x

    tmp = extractor.run(string)['values']['date']
    d1 = date.today()

    for span, date_string in tmp.items():
        d1 = utility.date_decod(date_string)
#         print(date_string)    
    tmp2 = extractor.run(string)['values']['time']
#     print(tmp2)
    t1 = datetime.time(0, 0, 0, 0)
    for span, timestring in tmp2.items():
        t1 = handle_time(timestring)
        
    
    d1 = datetime.datetime.combine(d1, t1)
    output['value'] = d1.timestamp()
    return output
    

test()      
