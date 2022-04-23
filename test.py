from cgi import print_arguments
import datetime
import string
from parsi_io.modules.time_extractions import TimeExtraction
import utility
from datetime import date
import re

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
string = "از ساعت دو تا پنج باید این کار انجام شود"
print(extractor.run(string))
date_sample = extractor.run(string)['values']['date']
for x in date_sample.keys():
    print(utility.date_decod(date_sample[x]))
