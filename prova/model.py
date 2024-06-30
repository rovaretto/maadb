import datetime
import locale

# Imposta la lingua italiana
locale.setlocale(locale.LC_TIME, 'it_IT.utf8')

# Ottieni la data di oggi
oggi = datetime.datetime.today()


# Aggiungi un giorno
one_day_later = oggi + datetime.timedelta(days=1)

# Ottieni il giorno della settimana in italiano
giorno_settimana = one_day_later.strftime('%A')

print(giorno_settimana)