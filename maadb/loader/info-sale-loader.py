import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dbOspedale = myclient["ospedale"]

infoSale = dbOspedale["info-sale"]

salaA = {"nome":"A",
        "giorniApertura": ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"],
         "specialita":{"Lunedi": "General", "Martedi":"General", "Mercoledi":"General", "Giovedi":"General", "Venerdi":"General"},
         "orarioApertura": {"Lunedi":"08:00", "Martedi":"08:00", "Mercoledi":"08:00", "Giovedi":"08:00", "Venerdi":"08:00"},
         "orarioChiusura": {"Lunedi":"16:00", "Martedi":"16:00", "Mercoledi":"16:00", "Giovedi":"16:00", "Venerdi":"16:00"},
        "equipeForToday" : {"Lunedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Martedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Mercoledi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Giovedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Venerdi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]}
                            }
        }

salaB = {"nome":"B",
        "giorniApertura": ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"],
        "specialita":{"Lunedi": "Gyn_Obstetrics", "Martedi":"Gyn_Obstetrics", "Mercoledi":"Gyn_Obstetrics", "Giovedi":"Gyn_Obstetrics", "Venerdi":"Gyn_Obstetrics"},
         "orarioApertura": {"Lunedi":"08:00", "Martedi":"08:00", "Mercoledi":"08:00", "Giovedi":"08:00", "Venerdi":"08:00"},
         "orarioChiusura": {"Lunedi":"16:00", "Martedi":"16:00", "Mercoledi":"16:00", "Giovedi":"16:00", "Venerdi":"16:00"},
        "equipeForToday" : {"Lunedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Martedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Mercoledi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Giovedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Venerdi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]}
                            }
        }

salaC = {"nome":"C",
        "giorniApertura": ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"],
        "specialita":{"Lunedi": "Otolaryngology", "Martedi":"Otolaryngology", "Mercoledi":"Otolaryngology", "Giovedi":"Otolaryngology", "Venerdi":"Otolaryngology"},
         "orarioApertura": {"Lunedi":"08:00", "Martedi":"08:00", "Mercoledi":"08:00", "Giovedi":"08:00", "Venerdi":"08:00"},
         "orarioChiusura": {"Lunedi":"16:00", "Martedi":"16:00", "Mercoledi":"16:00", "Giovedi":"16:00", "Venerdi":"16:00"},
        "equipeForToday" : {"Lunedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Martedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Mercoledi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Giovedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Venerdi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]}
                            }
        }

salaD = {"nome":"D",
        "giorniApertura": ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi"],
        "specialita":{"Lunedi": "Trauma", "Martedi":"Trauma", "Mercoledi":"Trauma", "Giovedi":"Trauma", "Venerdi":"Trauma"},
         "orarioApertura": {"Lunedi":"08:00", "Martedi":"08:00", "Mercoledi":"08:00", "Giovedi":"08:00", "Venerdi":"08:00"},
         "orarioChiusura": {"Lunedi":"16:00", "Martedi":"16:00", "Mercoledi":"16:00", "Giovedi":"16:00", "Venerdi":"16:00"},
        "equipeForToday" : {"Lunedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Martedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Mercoledi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Giovedi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]},
                            "Venerdi": {"Surgeons": [12], "Anesthesist":[9], "Nurse":[10,21]}
                            }
        }
infoSale.drop()

infoSale.insert_many([salaA, salaB, salaC,salaD])

