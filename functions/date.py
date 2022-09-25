from datetime import datetime, timezone, timedelta

#Definir el time zone de Argentina.
dif = timedelta(hours=-3)
tz = timezone(dif)

#Modificar el datetime para que se guarde con el horario de Argentina.
def setToLocalTime(dt):
    dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(tz)
    local_datetime = dt.strftime('%Y-%m-%d %H:%M')
    return local_datetime