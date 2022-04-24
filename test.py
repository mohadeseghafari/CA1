from cgi import print_arguments
import datetime
import string
from time_extractions import TimeExtraction
import utility
from datetime import date
import re

def interval_decoder(span):
    span = span[1:-1].split(', ')
    return [int(span[0]), int(span[1])]

def gregorian_to_jalali(gy, gm, gd):
 g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
 if (gm > 2):
  gy2 = gy + 1
 else:
  gy2 = gy
 days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
 jy = -1595 + (33 * (days // 12053))
 days %= 12053
 jy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  jy += (days - 1) // 365
  days = (days - 1) % 365
 if (days < 186):
  jm = 1 + (days // 31)
  jd = 1 + (days % 31)
 else:
  jm = 7 + ((days - 186) // 30)
  jd = 1 + ((days - 186) % 30)
 return [jy, jm, jd]


extractor = TimeExtraction()
string = "من و علی از فردا تا یکشنبه دو هفته بعد باید بازی کنیم"
result = extractor.run(string)['markers']['datetime']
print (result)
regex_pattern = '(' + 'از' +'\s)' "?(([ا-ی]*\s)*)\s" + '(تا' ")(\s([ا-ی])*)"
date_sample = extractor.run(string)['values']['date']
interval_time = False
for x in result.keys():
    interval_check = re.search(regex_pattern, result[x])
    if not interval_check:
        continue
    interval_time = True
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
        print(utility.date_decod(string))
        first_span = interval_decoder(span)
        first_span[0] += az_index + interval_decoder(x)[0]
        first_span[1] += az_index + interval_decoder(x)[0]
        print(first_span)
    
    tmp = extractor.run(second_time)['values']['date']
    for span, string in tmp.items():
        print(utility.date_decod(string))
        second_span = interval_decoder(span)
        second_span[0] += ta_index + 3 + interval_decoder(x)[0]
        second_span[1] += ta_index + 3 + interval_decoder(x)[0]
        print(second_span)
if not interval_time:
    print(None)