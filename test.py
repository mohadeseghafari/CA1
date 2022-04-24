import datetime
import string
from time_extractions import TimeExtraction
import utility
from datetime import date
import re

def interval_decoder(span):
    span = span[1:-1].split(', ')
    return [int(span[0]), int(span[1])]

def test():
    print(run("من و علی از دوشنبه تا یکشنبه دو هفته بعد ساعت سه باید بازی کنیم"))

def run(string: str):
    functions = [crontime_handler, time_interval_handler, exact_handler]
    for f in functions:
        result = f(string)
        if result: 
            return result
    return None

def time_interval_handler(string):
    output = {'type': 'duration', 'text': 'token'}
    extractor = TimeExtraction()
    
    result = extractor.run(string)['markers']['datetime']
    print(result)
    #TODO: find ta

    date_sample = extractor.run(string)['values']['date']
    interval_time = False
    for x in result.keys():
        if result[x][0:3] == 'تا ':
            ta_index = 0
        elif result[x].find(' تا ') >= 0:
            ta_index = result[x].find(' تا ') + 1
        else:
            continue
        interval_time = True
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
        for span, string in tmp.items():
            d1 = utility.date_decod(string)
            first_span = interval_decoder(span)
            first_span[0] += az_index + interval_decoder(x)[0]
            first_span[1] += az_index + interval_decoder(x)[0]
        tmp2 = extractor.run(first_time)['values']['time']

        t1 = datetime.time(0, 0, 0, 0)
        for span, string in tmp2.items():
            t1 = datetime.time(int(string[0:2]), int(string[3:5]))
        
        d1 = datetime.datetime.combine(d1, t1)
        d2 = date.today()
                               
        tmp = extractor.run(second_time)['values']['date']
        for span, string in tmp.items():
            d2 = utility.date_decod(string)
            second_span = interval_decoder(span)
            second_span[0] += ta_index + 3 + interval_decoder(x)[0]
            second_span[1] += ta_index + 3 + interval_decoder(x)[0]
        tmp2 = extractor.run(second_time)['values']['time']

        t2 = datetime.time(0, 0, 0, 0)
        for span, string in tmp2.items():
            t2 = datetime.time(int(string[0:2]), int(string[3:5]))

        d2 = datetime.datetime.combine(d2, t2)
        output['value'] = [int(d1.timestamp()), int(d2.timestamp())]
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
                               
        tmp2 = extractor.run(result[x])['values']['date2']
        time ='' 
        for span, string in tmp.items():
            time = string                     
        time = ctime(time)
        tmp = extractor.run(result[x])['values']['date']
        for span, string in tmp.items():
            array = string.split(' ')
            for i in range(len(array) ) :
                if array[i] == 'هر' :
                    break
            if array[i+1] == 'روز' :
                return time + ' * 0 0'
            elif array[i+1] == 'شنبه' :
                return time + ' * 0 6'
            elif array[i+1] == 'یکشنبه' :
                return time + ' * 0 7'
            elif array[i+1] == 'دوشنبه' :
                return time + ' * 0 1'
            elif array[i+1] == 'سه شنبه' :
                return time + ' * 0 2'
            elif array[i+1] == 'چهارشنبه' :
                return time + ' * 0 3'
            elif array[i+1] == 'پنج شنبه' :
                return time + ' * 0 4'
            elif array[i+1] == 'جمعه' :
                return time + ' * 0 5'
            elif array[i+1] == 'ماه' :
                x = re.findall('[0-9]+', date_str)
                return time + ' * ' + x[0] + ' *'

def exact_handler(string):
    pass

test()  
