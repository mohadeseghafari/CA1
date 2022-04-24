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
    print(run("من و علی از فردا ساعت دو تا یکشنبه دو هفته بعد ساعت سه باید بازی کنیم"))

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
    #TODO: find ta
    regex_pattern = '(' + 'از' +'\s)' "?(([ا-ی]*\s)*)\s" + '(تا' ")(\s([ا-ی])*)"
    date_sample = extractor.run(string)['values']['date']
    interval_time = False
    for x in result.keys():
        interval_check = re.search(regex_pattern, result[x])
        if not interval_check:
            continue
        interval_time = True
        output['span'] = x
        ta_index = result[x].find('تا')
        az_index = result[x].find('از')
        if az_index >= 0:
            az_index += 3
        else:
            az_index = 0
        first_time = result[x][az_index:ta_index - 1]
        second_time = result[x][ta_index + 3:]
        # print(first_time, second_time)
        #TODO change it to get time and date

        tmp = extractor.run(first_time)['values']['date']
        for span, string in tmp.items():
            d1 = utility.date_decod(string)
            first_span = interval_decoder(span)
            first_span[0] += az_index + interval_decoder(x)[0]
            first_span[1] += az_index + interval_decoder(x)[0]
            
        
        tmp = extractor.run(second_time)['values']['date']
        for span, string in tmp.items():
            d2 = utility.date_decod(string)
            second_span = interval_decoder(span)
            second_span[0] += ta_index + 3 + interval_decoder(x)[0]
            second_span[1] += ta_index + 3 + interval_decoder(x)[0]
        output['value'] = [d1, d2]
        return output

def crontime_handler(string):
    pass

def exact_handler(string):
    pass

test()  
