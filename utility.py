
import datetime
import re


def date_decod(string):
#     print('\"' + string + '\"')
    functions = [relative_simple_phase_date, absolute_date, relative_day_week, relative_day, relative_week]
    for f in functions:
        if f(string):
            return f(string)
    return None

def relative_simple_phase_date(string):
    date_simple_phase = {'پریروز': -2, 'دیروز': -1, 'امروز': 0, 'فردا': 1, 'پس فردا': 2}
    for phase, shift_num in date_simple_phase.items():
        if string == phase:
            return day_shift(shift_num, datetime.date.today())
    return None

# def absolute_date(string):
#     j_months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
#     regex_pattern ="(\d+)\s(" + '|'.join(j_months)+")\s(\d+)"
#     status = re.search(regex_pattern, string)
#     if not status:
#         return None
#     string = string.split(' ')
#     day = int(string[0])
#     month = j_months.index(string[1])
#     year = int(string[2])

def absolute_date(string):
    regex_pattern ="\d+/\d+/\d+"
    status = re.search(regex_pattern, string)
    if not status:
        return None
    string = string.split('/')
    day = int(string[2])
    month = int(string[1])
    year = int(string[0])
    res = jalali_to_gregorian(year, month, day)
    return datetime.date(res[0], res[1], res[2])
    
def day_shift(k, date):
    if k >= 0:
        return date + datetime.timedelta(days=k)
    else:
        return date - datetime.timedelta(days=-k)
    
def jalali_to_gregorian(jy, jm, jd):
 jy += 1595
 days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
 if (jm < 7):
  days += (jm - 1) * 31
 else:
  days += ((jm - 7) * 30) + 186
 gy = 400 * (days // 146097)
 days %= 146097
 if (days > 36524):
  days -= 1
  gy += 100 * (days // 36524)
  days %= 36524
  if (days >= 365):
   days += 1
 gy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  gy += ((days - 1) // 365)
  days = (days - 1) % 365
 gd = days + 1
 if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
  kab = 29
 else:
  kab = 28
 sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
 gm = 0
 while (gm < 13 and gd > sal_a[gm]):
  gd -= sal_a[gm]
  gm += 1
 return [gy, gm, gd]

def relative_day(string):
    past = {'گذشته', 'پیش', 'قبل'}
    future = {'بعد', 'آینده', 'دیگر'}
    regex_pattern_past = "(\d+)\s(روز)\s(" + '|'.join(past) + ")"
    regex_pattern_future = "(\d+)\s(روز)\s(" + '|'.join(future) + ")"
    status_future = re.search(regex_pattern_future, string)
    status_past = re.search(regex_pattern_past, string)
    if status_future:
        day_number = re.split("\s", string)
        shift_num = int(day_number[0])
        return day_shift(shift_num, datetime.date.today())
    if status_past:
        day_number = re.split("\s", string)
        shift_num = -int(day_number[0])
        return day_shift(shift_num, datetime.date.today())
    return None

def relative_week(string):
    past = {'گذشته', 'پیش', 'قبل'}
    future = {'بعد', 'آینده', 'دیگر'}
    regex_pattern_past = "(\d+)\s(هفته)\s(" + '|'.join(past) + ")"
    regex_pattern_future = "(\d+)\s(هفته)\s(" + '|'.join(future) + ")"
    regex_pattern_past1 = "(هفته)\s(" + '|'.join(past) + ")"
    regex_pattern_future1 = "(هفته)\s(" + '|'.join(future) + ")"
    status_future = re.search(regex_pattern_future, string)
    status_past = re.search(regex_pattern_past, string)
    status_future1 = re.search(regex_pattern_future1, string)
    status_past1 = re.search(regex_pattern_past1, string)
    if status_future:
        day_number = re.split("\s", string)
        shift_num = int(day_number[0]) * 7
        return day_shift(shift_num, datetime.date.today())
    if status_past:
        day_number = re.split("\s", string)
        shift_num = -(int(day_number[0]) * 7)
        return day_shift(shift_num, datetime.date.today())
    if status_future1:
        shift_num = 7
        return day_shift(shift_num, datetime.date.today())
    if status_past1:
        shift_num = -7
        return day_shift(shift_num, datetime.date.today())
    return None

def relative_day_week(string):
    weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنج شنبه', 'جمعه']
    past = {'گذشته', 'پیش', 'قبل'}
    future = {'بعد', 'آینده'}
    regex_pattern_past = '(' + '|'.join(weekdays) + ')'  + "\s(\d+)\s(هفته)\s(" + '|'.join(past) + ")"
    regex_pattern_future ='(' + '|'.join(weekdays) + ')' + '\s' + "(\d+)\s(هفته)\s(" + '|'.join(future) + ")"
    regex_pattern_past1 ='(' + '|'.join(weekdays) + ')' + '\s' + "(هفته)\s(" + '|'.join(past) + ")"
    regex_pattern_future1 = '(' + '|'.join(weekdays) + ')'+ '\s'  + "(هفته)\s(" + '|'.join(future) + ")"
    regex_pattern_past2 = '(' + '|'.join(weekdays) + ')' + '\s' +'('+ '|'.join(future) + ")"
    regex_pattern_future2 = '(' + '|'.join(weekdays) + ')' + '\s' + '(' + '|'.join(future) + ")"
    regex_pattern_this_week = '(' + '|'.join(weekdays) + ')'+ '\s'  + "این" + '\s' + 'هفته'
    regex_pattern_day_week = '(' + '|'.join(weekdays) + ')'

    status_future = re.search(regex_pattern_future, string)
    status_past = re.search(regex_pattern_past, string)
    status_future1 = re.search(regex_pattern_future1, string)
    status_past1 = re.search(regex_pattern_past1, string)
    status_past2 = re.search(regex_pattern_past2, string)
    status_future2 = re.search(regex_pattern_future2, string)
    status_this_week = re.search(regex_pattern_this_week, string)
    status_day_week = re.search(regex_pattern_day_week, string)

    if status_future:
        day_number = re.split("\s", string)
        weekday = (datetime.date.today().weekday() + 2) % 7
        targetweekday = weekdays.index(day_number[0])
        shift_num = int(day_number[1]) * 7 - weekday + targetweekday
        return day_shift(shift_num, datetime.date.today())
    if status_past:
        day_number = re.split("\s", string)
        weekday = (datetime.date.today().weekday() + 2) % 7
        targetweekday = weekdays.index(day_number[0])
        shift_num = -(int(day_number[1]) * 7) - weekday + targetweekday
        return day_shift(shift_num, datetime.date.today())
    if status_future1:
        day_number = re.split("\s", string)
        weekday = (datetime.date.today().weekday() + 2) % 7
        targetweekday = weekdays.index(day_number[0])
        shift_num = 7 - weekday + targetweekday
        return day_shift(shift_num, datetime.date.today())
    if status_past1:
        day_number = re.split("\s", string)
        weekday = (datetime.date.today().weekday() + 2) % 7
        targetweekday = weekdays.index(day_number[0])
        shift_num = -7 - weekday + targetweekday
        return day_shift(shift_num, datetime.date.today())
    if status_future2:
        day_number = re.split("\s", string)
        weekday = (datetime.date.today().weekday() + 2) % 7
        targetweekday = weekdays.index(day_number[0])
        shift_num = (6 - weekday + targetweekday ) % 7 + 1
        return day_shift(shift_num, datetime.date.today())
    if status_past2:
        day_number = re.split("\s", string)
        weekday = (datetime.date.today().weekday() + 2) % 7
        targetweekday = weekdays.index(day_number[0])
        shift_num = (-6 - weekday + targetweekday ) % 7 - 1
        return day_shift(shift_num, datetime.date.today())
    if status_this_week or status_day_week :
        day_number = re.split("\s", string)
        weekday = (datetime.date.today().weekday() + 2) % 7
        targetweekday = weekdays.index(day_number[0])
        shift_num = targetweekday - weekday
        return day_shift(shift_num, datetime.date.today())
    return None
