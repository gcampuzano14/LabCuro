import datetime



def date_serial(year, month, day, hour, minute, second):
    date_items = [str(year), str(month), str(day), str(hour), str(minute), str(second)]
    print date_items
    for i in range(0,len(date_items)):
        if len(date_items[i]) == 1:
            date_items[i] = '0' + date_items[i]
    date_serial =  "".join(date_items)
    return date_serial
    
            

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#year = now.year
#month = now.month
#day = now.day
#hour = now.hour
#minute = now.minute
#second = now.second

#ff = datetime.datetime.strptime(str(now), "%d-%b-%Y-%H:%M:%S")

print now
#print year
#print date_serial(year, month, day, hour, minute, second)


