
dic = {'B-Ge-i-5-897.0': 327.0, 'B-Ge-o-5-534.1': 135.0, 'M-Ge-o-5-530.00': 199.0, 'S-Ge-i-5-932.12': 0.0, 'S-Ge-o-5-534.1': 400.0, 'S-Ge-o-5-534.35': 265.0}

file = open('data_patient_OUTPUT.data','w')
for row in dic:
    file.write(row+'\n')