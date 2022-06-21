#Lucía Delgado Blanco
#TFG - Análisis de costes y comparación de tecnologías fotovoltaicas

import matplotlib.pyplot as plt # Importar el módulo pyplot con el alias plt
import numpy as np

print("Bienvenido, este programa calcula el LCOE de una instalación fotovoltaica")

#print("¿Quiere hacer una comparación o un único cálculo? \n Comparación = c \n único cálculo = u")
#operacion = input("")

print("¿Qué datos va a utilizar? \n Defecto = d \n Específicos = e")
datos = input("")

if datos == "e": # Elección valores específicos

    print('Recuerde que en Python los números decimales se indican con el separador "." en vez de ","')


############# TIPO DE TECNOLOGÍA Y CARACTERÍSTICAS DE LOS MÓDULOS ##############################################################################

    G_STC = 1000 #Irradiancia en CEM [W/m^2]
        
    nombre_tec = input("¿Qué tecnología se utiliza en los módulos? (PERC, PERT, SHJ, IBC...): ")
    nombre_proceso = input("¿Con qué tipo de oblea? (monocristalino, multicristalino): ")

    A = float(input("Área de un módulo [m2]: "))
    cost_mod = float(input("Coste del módulo en [$/W]: "))
    Pmod = float(input("Potencia nominal de cada módulo en [W]: "))

    n = Pmod/(A*G_STC) #eficiencia del módulo
     
############# COSTES DE INSTALACIÓN Y SUPOSICIONES ########################################################################################

    nombre_inst = input("Se consideran cuatro tipos de instalaciones: Residencial, Comercial, Gran instalación fija o con seguimiento: ")
    BOS_area = float(input("Coste del BOS area [$/W]: "))
    BOS_pot = float(input("Coste del BOS potencia [$/W]: "))
    labor = float(input("Coste de la mano de obra (labor) [$/W]: "))
    otros = float(input("Otros costes (otros) [$/W]: "))
    inv = float(input("Coste del inversor [$/W]: "))
    a = float(input("Costes de operación y manteniemiento del año inicial (OyM) [$/W]: "))

    P_STC = float(input("Potencia nominal del sistema en [kW]: "))
    Psys = P_STC*1000

    ILR = float(input("Inverter loading ratio (ILR): "))
    WACCnominal = float(input("WACC nominal [%]: "))
    WACCnom = WACCnominal/100

    Degradacion = float(input("Degradación [%]: "))
    Degr = Degradacion/100
    
    c_A = cost_mod + BOS_area

############# DATOS DEL MÓDULO (área, número, potencia) ########################################################################################
   
    num_mod = round(Psys/Pmod) #Número de módulos, número entero más cercano
    print("Número de módulos: ", num_mod)

    CTM = 1

    cost_area = c_A*Psys/(n*CTM*A*num_mod*G_STC) #Costes totales relacionados con el área [$]
    
    c_P = (inv/ILR) + BOS_pot
    
    cost_pot = c_P*Psys/(n*CTM*A*num_mod*G_STC) #Costes totales relacionados con la potencia [$]
    
    CoO = cost_area + cost_pot #Cost of Ownership [$]

############# ASUNTOS FINANCIEROS: WACC ########################################################################################
    
    Inflacion = float(input("Inflación [%]: "))
    Infl = Inflacion/100
    
    WACCreal = ((1+WACCnom)/(1+Infl))-1
    
############# COSTES OyM ########################################################################################

    años = int(input("Años de vida del sistema (nº entero): "))

    cost_oym = 0 #Costes totales operación y mantenimiento
    for t in range(1, años+1):
        cost_oym = cost_oym + a/((1+WACCreal)**t)

############# ENERGÍA ########################################################################################

    G_t = float(input("Irradiación anual [kWh/m^2]: "))
    PR = float(input("Performance ratio [%]: "))

    m = (PR * G_t)/(ILR * G_STC)
        
    energ = 0 #Cantidad total de energía producida
    for t in range(1, años+1):
        energ = energ + (m*((1-Degr)**t))/((1+WACCreal)**t)

    print ('¿Utiliza tecnología bifacial? Conteste "si" o "no": ')
    bifacialidad = input("")
    if bifacialidad == "si": #bifacial
        energ = energ * 1.05
    elif bifacialidad == "no": #no bifacial
        energ = energ
    else:
        print('Lo introducido no es correcto. Debe escribir "si" o "no"')
            

############# INFO POR CONSOLA ########################################################################################

    print ("--------    --------    --------    --------    --------    --------")
    print ("DESGLOSE DE PARÁMETROS ESCOGIDOS")
    print ("--------    --------    --------    --------    --------    --------")

    print("Eficiencia del módulo: ", n*100,"%")
    print("Coste total del módulo: ", cost_mod, "$/W")
    print("BOS estructural: ", BOS_area, "$/W")
    print("BOS eléctrico: ", BOS_pot, "$/W")
    print("Coste del inversor: ", inv, "$/W")
    print("Costes de operación y mantenimiento anuales: ", a, "$/W al año")
    print("P* = ", P_STC, "KWp")
    print("WACCnom = ", WACCnom, "%")
    print("Degradación = ", round(Degr*100, 3), "%")
    print("Coste de mano de obra: ", labor, "$")
    print("Área del módulo: ", A, "m^2")
    print("Costes totales relacionados con el área: ", cost_area, "$")
    print("Costes totales relacionados con la potencia: ", cost_pot, "$")    
    print ("Inflación anual: ", Infl*100, "%")
    print ("Años útiles del sistema fotovoltaico a implantar: ", años, "años")
    print("Costes totales de operación y mantenimiento teniendo en cuenta el WACCreal: ", cost_oym, "$/W")
    print("Irradiación anual: ", G_t, "KWh/m^2")
    print("PR: ", PR)
    print("Cantidad de electricidad producida anual: ", m, "KWh/año")
    print("Cantidad total de energía producida teniendo en cuenta la degradación anual y el WACCreal: ", energ, "KWh/año")

############# LCOE ########################################################################################

    print ("----  --------  --------  --------  --------  --------  --------  ----")
    lcoe = (labor + otros + CoO + cost_oym)/energ
    print ("labor + otros + CoO + cost_oym:", labor, "+", otros,"+", CoO,"+ (", cost_area, "+", cost_pot ,") =", labor + otros + CoO + cost_oym)
    print ("SEGUN EL EXCEL cost_area:", cost_area +labor + otros)
    print ("c_A, c_P:", c_A, c_P)

    print ("#######################################################################")
    print("###################### Valor del LCOE:", lcoe, "$/KWh")
    print ("#######################################################################")

############################################################################################################################################

elif datos == "d": # Elección valores por defecto
    
############# TIPO DE TECNOLOGÍA Y POTENCIA NOMINAL DEL MÓDULO ##############################################################################

    G_STC = 1000 #Irradiancia en CEM [W/m^2]
    A = 1.6368 # Área [m^2] de 1 módulo

    print("¿Qué tecnología se utiliza en los módulos? \n 1) Al-BSF estándar (mono) \n 2) Mono PERC \n 3) Multi PERC \n 4) PERT bifacial (mono) \n 5) SHJ bifacial (mono) \n 6) IBC (mono)")
    conv_cel_pais = input("")
    if conv_cel_pais == "1": # elección Al-BSF estándar mono
        nombre_tec = "Al-BSF"
        nombre_proceso = "Monocristalino"
        cost_mod = 0.338 # 2018 NREL pg 118 

        print ("Elija la potencia nominal de cada módulo \n 1) 285 W \n 2) Introducir valor numérico")
        pot_nom = input("")
        if pot_nom == "1": # 285 W
            Pmod = 285
        elif pot_nom == "2": # poner valor W
            Pmod = float(input("Introduzca el valor de la potencia nominal de cada módulo en W: "))
        else:
            print("Lo introducido no es correcto.")
        n = Pmod/(A*G_STC) #eficiencia del módulo

    elif conv_cel_pais == "2": # elección Mono PERC
        nombre_tec = "PERC"
        nombre_proceso = "Monocristalino"
        cost_mod = 0.32

        print ("Elija la potencia nominal de cada módulo \n 1) 310 W \n 2) Introducir valor numérico")
        pot_nom = input("")
        if pot_nom == "1": # 310 W
            Pmod = 310
        elif pot_nom == "2": # poner valor W
            Pmod = float(input("Introduzca el valor de la potencia nominal de cada módulo en W: "))
        else:
            print("Lo introducido no es correcto.")
        n = Pmod/(A*G_STC)

    elif conv_cel_pais == "3": # elección multi PERC
        nombre_tec = "Multi PERC"
        nombre_proceso = "Multicristalino"
        cost_mod = 0.317

        print ("Elija la potencia nominal de cada módulo \n 1) 295 W \n 2) Introducir valor numérico")
        pot_nom = input("")
        if pot_nom == "1": # 295 W
            Pmod = 295
        elif pot_nom == "2": # poner valor W
            Pmod = float(input("Introduzca el valor de la potencia nominal de cada módulo en W: "))
        else:
            print("Lo introducido no es correcto.")
        n = Pmod/(A*G_STC)
        
    elif conv_cel_pais == "4": # elección PERT bifacial mono
        nombre_tec = "PERT bifacial"
        nombre_proceso = "Monocristalino"
        cost_mod = 0.355

        print ("Elija la potencia nominal de cada módulo \n 1) 295 W \n 2) Introducir valor numérico")
        pot_nom = input("")
        if pot_nom == "1": # 295 W
            Pmod = 295
        elif pot_nom == "2": # poner valor W
            Pmod = float(input("Introduzca el valor de la potencia nominal de cada módulo en W: "))
        else:
            print("Lo introducido no es correcto.")
        n = Pmod/(A*G_STC)
        
    elif conv_cel_pais == "5": # elección SHJ bifacial mono
        nombre_tec = "SHJ bifacial"
        nombre_proceso = "Monocristalino"
        cost_mod = 0.345

        print ("Elija la potencia nominal de cada módulo \n 1) 325 W \n 2) Introducir valor numérico")
        pot_nom = input("")
        if pot_nom == "1": # 325 W
            Pmod = 325
        elif pot_nom == "2": # poner valor W
            Pmod = float(input("Introduzca el valor de la potencia nominal de cada módulo en W: "))
        else:
            print("Lo introducido no es correcto.")
        n = Pmod/(A*G_STC)
        
    elif conv_cel_pais == "6": # elección IBC mono
        nombre_tec = "IBC"
        nombre_proceso = "Monocristalino"
        cost_mod = 0.359

        print ("Elija la potencia nominal de cada módulo \n 1) 330 W \n 2) Introducir valor numérico")
        pot_nom = input("")
        if pot_nom == "1": #330 W
            Pmod = 330
        elif pot_nom == "2": # introducir valor en vatios
            Pmod = float(input("Introduzca el valor de la potencia nominal de cada módulo en W: "))
        else:
            print("Lo introducido no es correcto.")
        n = Pmod/(A*G_STC)
    else:
        print("Lo introducido no es correcto. Debe elegir una tecnología de la lista mencionada")
     
############# TAMAÑO DE LA INSTALACIÓN ########################################################################################

    print("Indique el tipo de instalación que se va a realizar \n 1) Residencial \n 2) Comercial \n 3) Gran instalación")
    tipo_inst_bos = input("")
    if tipo_inst_bos == "1": # residencial, datos de 2018 NREL pg 118 
        nombre_inst = "Residencial"
        BOS_area = 0.084 
        BOS_pot = 0.19
        labor = 0.242
        otros = 1.068
        inv = 0.217 #Coste del inversor
        a = 0.022 #Costes O&M 2018 NREL pg 45 

        Psys = 6900 #Potencia nominal del sistema residencial 6.9kW
        P_STC = 6.9 #Potencia nominal del sistema residencial 6.9kW

        ILR = 1.15 # Inverter loading ratio 2018 NREL pg 45
        
        WACCnom = 0.054 # Fraunhofer pg 34 
                
    elif tipo_inst_bos == "2": # comercial, datos de 2018 NREL pg 118 
        nombre_inst = "Comercial"
        BOS_area = 0.112
        BOS_pot = 0.133
        labor = 0.159
        otros = 0.711
        
        Psys = 200000
        P_STC = 200
        ILR = 1.15 # Inverter loading ratio 2018 NREL pg 56
        a = 0.018 # O&M 2018 NREL pg 56
        WACCnom = 0.057 # Fraunhofer pg 34
        inv = 0.045

    elif tipo_inst_bos == "3": # gran instalación, datos de 2018 NREL pg 118 
        nombre_inst = "Gran instalación"
        BOS_pot = 0.088
        Psys = 100000000 # gran ins 100MW
        P_STC = 100000 # gran ins 100MW
        WACCnom = 0.057 # Fraunhofer pg 34 
        inv = 0.022
        print ("¿De qué forma? \n 1) Con inclinación fija \n 2) Con seguimiento")
        tipo_instal = input("")
        if tipo_instal == "1": # con incliación fija
            BOS_area = 0.087         
            labor = 0.094
            otros = 0.182
            a = 0.013 # O&M 2018 NREL pg 66
            ILR = 1.36
        elif tipo_instal == "2": # con seguimiento
            BOS_area = 0.13
            labor = 0.102
            otros = 0.196
            a = 0.015 # O&M 2018 NREL pg 66
            ILR = 1.3
        else:
            print("Lo introducido no es correcto.")
    else:
        print("Lo introducido no es correcto. Debe elegir una instalación de la lista mencionada")
    
    Degr = 0.007 #Degradación

    c_A = cost_mod + BOS_area

############# DATOS DEL MÓDULO (área, número, potencia) ########################################################################################
   
    num_mod = round(Psys/Pmod) #Número de módulos, número entero más cercano
    print("número de módulos: ", num_mod, "Psys:", Psys, "Pmod:", Pmod)

    CTM = 1

    cost_area = c_A*Psys/(n*CTM*A*num_mod*G_STC) #Costes totales relacionados con el área [$]
    
    c_P = (inv/ILR) + BOS_pot
    
    cost_pot = c_P*Psys/(n*CTM*A*num_mod*G_STC) #Costes totales relacionados con la potencia [$]
    
    CoO = cost_area + cost_pot #Cost of Ownership [$]

############# WACC ########################################################################################

    Infl = 0.025 #Inflación

    WACCreal = ((1+WACCnom)/(1+Infl))-1
    
############# ENERGÍA ########################################################################################

    años = 30 #Años de vida del sistema
    cost_oym = 0 #Costes totales operación y mantenimiento
    for t in range(1, años+1):
        cost_oym = cost_oym + a/((1+WACCreal)**t)

    print("¿En qué ciudad se calculan los costes? \n 1) High solar resource (Phoenix, AZ) \n 2) Medium solar resource (Kansas City, MO) \n 3) Low solar resource (New York, NY)")
    pot_max_pais = input("")
    if pot_max_pais == "1": #High solar resource (Phoenix, AZ)
        if tipo_inst_bos == "1" or tipo_inst_bos == "2" or tipo_instal == "1": # residencial o comercial o gran inst. fijo
            G_t = 2448.09 # irradiación anual [kWh/m^2] PVGIS ángulo óptimo montaje fijo
        elif tipo_instal == "2": # con seguimiento
            G_t = 3317.78 # irradiación anual [kWh/m^2] PVGIS ángulo óptimo montaje seguim
        PR = 0.8
    elif pot_max_pais == "2": #Medium solar resource (Kansas City, MO)
        if tipo_inst_bos == "1" or tipo_inst_bos == "2" or tipo_instal == "1": # residencial o comercial o gran inst. fijo
            G_t = 1828.38 # irradiación anual [kWh/m^2] PVGIS ángulo óptimo montaje fijo
        elif tipo_instal == "2": # con seguimiento
            G_t = 2371.18 # irradiación anual [kWh/m^2] PVGIS ángulo óptimo montaje seguim
        PR = 0.8
    elif pot_max_pais == "3": #Low solar resource (New York, NY)
        if tipo_inst_bos == "1" or tipo_inst_bos == "2" or tipo_instal == "1": # residencial o comercial o gran inst. fijo
            G_t = 1513.98 # irradiación anual [kWh/m^2] PVGIS ángulo óptimo montaje fijo
        elif tipo_instal == "2": # con seguimiento
            G_t = 1969.72 # irradiación anual [kWh/m^2] PVGIS ángulo óptimo montaje seguim
        PR = 0.8

    else:
        print("Lo introducido no es correcto. Debe elegir un país de la lista mencionada")

    m = (PR * G_t)/(ILR * G_STC)
        
    energ = 0 #Cantidad total de energía producida
    for t in range(1, años+1):
        energ = energ + (m*((1-Degr)**t))/((1+WACCreal)**t)

    if nombre_tec== "PERT bifacial" or nombre_tec== "SHJ bifacial":
        energ = energ * 1.05


############# INFO POR CONSOLA ########################################################################################

    print ("--------    --------    --------    --------    --------    --------")
    print ("DESGLOSE DE PARÁMETROS ESCOGIDOS")
    print ("--------    --------    --------    --------    --------    --------")

    print("Eficiencia del módulo: ", n*100,"%")
    print("Coste total del módulo: ", cost_mod, "$/W")
    print("BOS estructural: ", BOS_area, "$/W")
    print("BOS eléctrico: ", BOS_pot, "$/W")
    print("Coste del inversor: ", inv, "$/W")
    print("Costes de operación y mantenimiento anuales: ", a, "$/W al año")
    print("P* = ", P_STC, "KWp")
    print("WACCnom = ", WACCnom*100, "%")
    print("Degradación = ", round(Degr*100, 3), "%")
    print("Coste de mano de obra: ", labor, "$")
    print("Área del módulo: ", A, "m^2")
    print("Costes totales relacionados con el área: ", cost_area, "$")
    print("Costes totales relacionados con la potencia: ", cost_pot, "$")    
    print ("Inflación anual: ", Infl*100, "%")
    print ("Años útiles del sistema fotovoltaico a implantar: ", años, "años")
    print("Costes totales de operación y mantenimiento teniendo en cuenta el WACCreal: ", cost_oym, "$/W")
    print("Irradiación anual: ", G_t, "KWh/m^2")
    print("PR: ", PR, "%")
    print("Cantidad de electricidad producida anual: ", m, "KWh/año")
    print("Cantidad total de energía producida teniendo en cuenta la degradación anual y el WACCreal: ", energ, "KWh/año")

############# LCOE ########################################################################################

    print ("----  --------  --------  --------  --------  --------  --------  ----")
    lcoe = (labor + otros + CoO + cost_oym)/energ
    print ("labor + otros + CoO + cost_oym:", labor, "+", otros,"+", CoO,"+ (", cost_area, "+", cost_pot ,") =", labor + otros + CoO + cost_oym)
    print ("SEGUN EL EXCEL cost_area:", cost_area +labor + otros)
    print ("c_A, c_P:", c_A, c_P)

    print ("#######################################################################")
    print("###################### Valor del LCOE:", lcoe, "$/KWh")
    print ("#######################################################################")

else:
    print("Comando incorrecto")

########## Gráfica barras apiladas - Coste instalado ##############################################################

BOS = BOS_area + BOS_pot
CoO_cost_mod = ((cost_mod)*Psys)/(n*A*num_mod*G_STC)
CoO_BOS = (BOS*Psys)/(n*A*num_mod*G_STC)
CoO_inv = (inv*Psys)/(n*A*num_mod*G_STC)

print ("---datos de la grafica-----------------------------------------------------------------")
print ("modulo =", CoO_cost_mod, "inversor =", CoO_inv, "BOS = ", CoO_BOS,"mano_obra =",labor, "otros =",otros)
print("suma=", CoO_cost_mod + CoO_inv + CoO_BOS + labor + otros)

grupos=[nombre_inst]

plt.figure(figsize=(4,5))
plt.bar(grupos,cost_mod,label="CoO Módulo")
plt.bar(grupos,inv,bottom=np.array(cost_mod),label="CoO Inversor")
plt.bar(grupos,BOS,bottom=np.array(cost_mod)+np.array(inv),label="CoO BOS")
plt.bar(grupos,labor,bottom=np.array(cost_mod)+np.array(inv)+np.array(BOS),label="Mano de obra")
plt.bar(grupos,otros,bottom=np.array(cost_mod)+np.array(inv)+np.array(BOS)+np.array(labor),label="Otros")

plt.ylabel("$/W")
plt.xlabel(nombre_proceso)
#plt.text(-0.4,0.5, (nombre_tec, round(n, 3)),  color='yellow') # gran inst    
plt.title('Coste de inversión')
plt.legend()
plt.show()
