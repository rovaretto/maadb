def createSetI(patient):
    setI = "set I :=\n"
    for pat in patient:
        pat = pat.split(" ")
        setI += pat[2] + "\n"
    setI += ";\n"
    return setI


def createParamO(patients):
    result = "param o :=\n"
    for pat in patients:
        pat = pat.split(" ")
        sala = pat[1]
        opcode = pat[2]
        result += opcode + " " + sala + "\n"
    result += ";\n"
    return result


def createParamS(patient):
    result = "param s :=\n"
    for pat in patient:
        pat = pat.split(" ")
        opcode = pat[2]
        result += opcode + " 0\n"
    result += ";\n"
    return result


def createParamE(patient):
    result = "param e :=\n"
    for pat in patient:
        pat = pat.split(" ")
        opcode = pat[2]
        result += opcode + " 480\n"
    result += ";\n"
    return result


def createParamP(patient):
    result = "param p :=\n"
    for pat in patient:
        pat = pat.split(" ")
        opcode = pat[2]
        durata = pat[3]
        result += opcode + " " + durata + "\n"
    result += ";\n"
    return result


def createParamIo(patient):
    result = "param Io :=\n"
    for pat1 in patient:
        pat1 = pat1.split(" ")
        sala1 = pat1[1]
        opcode1 = pat1[2]
        itsFirst = True
        result += opcode1 + " ["
        for pat2 in patient:
            pat2 = pat2.split(" ")
            sala2 = pat2[1]
            opcode2 = pat2[2]
            if sala1 == sala2:
                result += opcode2 + ","
        result = result[:-1]
        result += "]\n"
    result += ";\n"
    print(result)
    return result


def createFilePatient():
    file = open('data_patient_input_from_advanced.dat', 'r')
    patient = file.read()
    patient = patient.split('\n')
    file.close()

    setI = createSetI(patient)

    paramO = createParamO(patient)
    paramS = createParamS(patient)
    paramE = createParamE(patient)
    paramP = createParamP(patient)
    paramQ = createParamIo(patient)

    file = open('data_patient.dat', 'w')
    file.write(setI)

    file.write(paramO)
    file.write(paramS)
    file.write(paramE)
    file.write(paramP)
    file.write(paramQ)


createFilePatient()
