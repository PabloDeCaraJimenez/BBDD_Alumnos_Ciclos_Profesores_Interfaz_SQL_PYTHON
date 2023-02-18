import mysql.connector

def conecta():
  miBBDD = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7alohoql7",
    database="CENTRO_DOCENTE"
  )
  return miBBDD

def extraer(miCursor, miConsulta, datos):
  miCursor.execute(miConsulta, datos)
  resp = miCursor.fetchall()
  return resp

def introducir(miConsulta, datos):
  miCursor.execute(miConsulta, datos)
  miBBDD.commit()
  
def esNumero(string):
  numero = True
  if string == "":
    numero = False
  for i in string:
    if i not in "1234567890":
      numero = False
  return numero
  
def esLetra(string):
  numero = True
  if string == "":
    numero = False
  for i in string:
    if i not in "QWERTYUIOPASDFGHJKLÑZXCVBNM":
      numero = False
  return numero

def esDNI(dni):
  resp = True
  if len(dni) != 9:
    resp = False
  elif esNumero(dni[0:8])== False or esLetra(dni[8])== False:
    resp = False
  return resp

def esFecha(fecha):
  resp = True
  if len(fecha) != 10:
    resp = False
  elif esNumero(fecha[0:4]) == False or esNumero(fecha[5:7]) == False or esNumero(fecha[8:]) == False:
    resp = False
  elif int(fecha[0:4]) < 1920 or int(fecha[0:4]) > (int(datetime.today().strftime("%Y")) - 12) or int(fecha[5:7]) < 1 or int(fecha[5:7]) > 12:
    resp = False
  elif fecha[5:7] in ["01","03","05","07","08","10","12"]:
    if int(fecha[8:]) < 1 or int(fecha[8:]) > 31:
      resp = False
  elif fecha[5:7] in ["04","06","09","11"]:
    if int(fecha[8:]) < 1 or int(fecha[8:]) > 30:
      resp = False
  elif fecha[5:7] == "02":
    if int(fecha[8:]) < 1 or int(fecha[8:]) > 28: # LO SIENTO POR LOS "BISITESTOS"
      resp = False
  return resp
    
def imprimeDatos(consulta, indice):
  itera = 0
  print ("------------------------------------")
  for datos in consulta:
    for dato in datos:
      print (indice[itera], end= "")
      print (dato)
      itera += 1
    print ("------------------------------------")
    itera = 0

def cierra(miCursor, miBBDD):
    miCursor.close()
    miBBDD.close()

def compruebaDNI(dni, miCursor):
    resp = False
    miConsulta = "SELECT COMPRUEBA_DNI(%s)"
    datos = [dni]
    miCursor.execute(miConsulta, datos)
    resp = miCursor.fetchall()
    return resp

def compruebaCODIGO(codigo, miCursor):
    resp = False
    miConsulta = "SELECT COMPRUEBA_CODIGO(%s)"
    datos = [codigo]
    miCursor.execute(miConsulta, datos)
    resp = miCursor.fetchall()
    return resp

    

print("\n1: REGISTRAR NUEVO ALUMNO")
print("2: MATRICULAR ALUMNO EN MÓDULO")
print("3: ELIMINAR ALUMNO")
print("4: LISTA DE MÓDULOS CON PROFESOR Y Nº ALUMNOS")
print("5: LISTA DE ALUMNOS DEL CENTRO")
print("6: SALIR")
opcion = input ("\nInserte el número de la opción que desea ejecutar: ")

while opcion != "6":
    if opcion == "1":
        miBBDD = conecta()
        miCursor = miBBDD.cursor()
        nombre = input ("Inserte el NOMBRE del ALUMNO: ")
        apellidos = input ("Inserte los APELLIDOS del ALUMNO: ")
        dni = input ("Inserte el DNI del ALUMNO: ")
        dni = dni.upper()
        while esDNI(dni)==False and dni != "SALIR":
            print("El DNI no es correcto. Inserte un DNI válido o \"salir\" para salir.")
            dni = input ("Inserte el DNI del ALUMNO: ")
            dni = dni.upper()
        if dni != "SALIR":
            if compruebaDNI(dni, miCursor) == [(1,)]:
                print ("\nEl DNI ya está registrado.\n")
            else:
                fecha_nacimiento = input ("Inserte la FECHA de nacimiento (yyyy-mm-dd) del ALUMNO: ")
                while esFecha(fecha_nacimiento) == False and fecha_nacimiento != "salir":
                    print ("La fecha no es válida. Introduce una fecha válida.")
                    fecha_nacimiento = input ("Inserte la FECHA de nacimiento (yyyy-mm-dd) del ALUMNO: ")
                if fecha_nacimiento != "salir":
                    telefono = input ("Inserte el TÉLEFONO del ALUMNO: ")
                    while (esNumero(telefono) == False or len(telefono) != 9) and telefono != "salir":
                        print("El número de teléfono es incorrecto.\nIntroduce un número válido o \"salir\" para salir.")
                        telefono = input ("Inserte el TÉLEFONO del ALUMNO: ")
                    if telefono != "salir":
                        miConsulta = "INSERT INTO ALUMNO (DNI, NOMBRE, APELLIDOS, FECHA_NACIMIENTO, TELEFONO) VALUES (%s, %s, %s, %s, %s)"
                        datos = [dni, nombre, apellidos, fecha_nacimiento, telefono]
                        introducir(miConsulta, datos)
                        print ("\nALUMNO registrado.\n")
        cierra(miCursor, miBBDD)

    elif opcion == "2":
        miBBDD = conecta()
        miCursor = miBBDD.cursor()
        dni = input ("Inserte el DNI del Alumno: ")
        dni = dni.upper()
        if compruebaDNI(dni, miCursor) == [(0,)]:
            print ("\nEl DNI no está registrado, por favor, registre primero al alumno.\n")
        else:
            codigo = input ("Inserte el CODIGO del MODULO que desea cursar: ")
            if compruebaCODIGO(codigo, miCursor) == [(0,)]:
                print ("\nEl MODULO no existe.\n")
            else:
                miConsulta = "CALL MATRICULACION (%s, %s)"
                datos = [dni, codigo]
                introducir(miConsulta, datos)
                print ("\nALUMNO matriculado.\n")
        cierra(miCursor, miBBDD)

    elif opcion == "3":
        miBBDD = conecta()
        miCursor = miBBDD.cursor()
        dni = input ("Introduce el DNI del ALUMNO que quieras eliminar: ")
        dni = dni.upper()
        if esDNI(dni) == False:
            print ("\nDNI incorrecto.\n")
        elif compruebaDNI(dni, miCursor) == [(0,)]:
            print ("\nEl DNI no está registrado.\n")
        else:
            miConsulta = "DELETE FROM ALUMNO WHERE DNI = %s;"
            datos = [dni]
            introducir (miConsulta, datos)
            print ("\nALUMNO eliminado.\n")
        cierra (miCursor, miBBDD)

    elif opcion == "4":
        indice = ["    CÓDIGO: ", "    NOMBRE: ", "     HORAS: ", "   IMPARTE: ", "Nº ALUMNOS: "]
        miBBDD = conecta()
        miCursor = miBBDD.cursor()
        miConsulta = "SELECT * FROM LISTA_DE_MODULOS;"
        miCursor.execute(miConsulta)
        imprimeDatos(miCursor.fetchall(), indice)
        cierra (miCursor, miBBDD)

    if opcion == "5":
      print ("\nUse:\n\"A\" para avanzar\n\"R\" para retroceder\n\"S\" para salir\nO introduzca el Nº de página")
      off = 0
      accion = "-1"
      while accion != "S":
        if accion == "A":
          off = off+5
        elif accion == "R":
          off = off-5
          if off < 0:
            off = 0
        elif esNumero(accion):
          irAPag = int(accion)
          if irAPag > 429496730:
            irAPag = 1
          off = (irAPag-1)*5
          if off <= 0:
            off = 1
        pagina = int((off/5)+1)
        miBBDD = conecta()
        miCursor = miBBDD.cursor()
        indice = ["   APELLIDOS: ", "      NOMBRE: ", "         DNI: ", "   FECHA NAC: ", "        EDAD: ", "TLF CONTACTO: "]
        pag = str(off)
        miConsulta = "CALL PAGINACION(%s)"
        datos = [pag]
        misAlumnos = extraer(miCursor, miConsulta, datos)
        print ("\n                           PAGINA: " + str(pagina))
        imprimeDatos(misAlumnos, indice)
        print ("\n")
        accion = input ("A/R/S/Nº : ").upper()
        cierra(miCursor, miBBDD)

        
    print("\n1: REGISTRAR NUEVO ALUMNO")
    print("2: MATRICULAR ALUMNO EN MÓDULO")
    print("3: ELIMINAR ALUMNO")
    print("4: LISTA DE MÓDULOS CON PROFESOR Y Nº ALUMNOS")
    print("5: LISTA DE ALUMNOS DEL CENTRO")
    print("6: SALIR")
    opcion = input ("\nInserte el número de la opción que desea ejecutar: ")





