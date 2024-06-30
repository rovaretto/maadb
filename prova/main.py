import datetime

# Ottieni la data corrente
week_number = datetime.date.today().isocalendar()[1]

print(f"Oggi e siamo nella settimana numero {week_number} dell'anno.")
