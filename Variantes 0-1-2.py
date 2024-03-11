import random
from tabulate import tabulate
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
class Componente:
    # esta clase almacena los tiempos de cada producto
    def __init__(self, espera):
        # al crear solo se  tiene los tiempos random´s
        self.tEnsamblaje = round(random.uniform(25, 35))
        self.tHorno = round(random.uniform(6, 10) + espera)
        self.tipo = ""
        self.tiempo = 0
        self.tLlegadaE = 0
        self.tSalidaE = 0
        self.tLlegadaH = 0
        self.tSalidaH = 0
        self.Ensambladora = -1
        self.Horno = -1

        # al entrar a una ensambladora se actualiza las variables correspondientes
    def setE(self, Llegada, Ensambladora):
        self.tipo = "L"
        self.tLlegadaE = Llegada
        self.tSalidaE = Llegada + self.tEnsamblaje
        self.tiempo = Llegada + self.tEnsamblaje
        self.Ensambladora = Ensambladora

    def setH(self, Llegada, Horno):
        self.tLlegadaH = Llegada
        self.tSalidaH = Llegada + self.tHorno
        self.tiempo = Llegada + self.tHorno
        self.tipo = "S"
        self.Horno  = Horno
    def MostrarEvento (self):
        if self.tipo == "S":return (str(self.Horno) + self.tipo) 
        return (str(self.Ensambladora) + self.tipo)

LEF = []

def mostrarLEF():
    list = []
    for i in LEF:
        list.append(i.MostrarEvento() + str(i.tiempo))
    return list


def addSalida (componente , tiempo, estadoHorno):
    for i,estado in enumerate(estadoHorno):
        if estado:
            componente.setH(tiempo, i)
            estadoHorno[i]= False
            break
    for i,evento in enumerate(LEF):
        if evento.tiempo>componente.tiempo:
            LEF.insert(i,componente)
            return estadoHorno
    LEF.append(componente)
    return estadoHorno
            
def addComponente(tiempo, Ensambladora, tiempoFinal, espera):
    aux = Componente(espera)  
    aux.setE(tiempo,Ensambladora)
    if aux.tiempo < tiempoFinal:
        for i,evento in enumerate(LEF):
            if evento.tiempo>aux.tiempo:
                LEF.insert(i,aux)
                return
        LEF.append(aux)

# aquí esta todo :)
def main(numEnsambladoras, numHornos, tiempoFinal, espera):
    colaHorno = []
    listaComponentes = [] #almacena componentes terminados
    tamMaxCola = 0
    estadoHorno = []
    for i in range(numHornos):
        estadoHorno.append(True)
    tiempoAct = 0
    componente = Componente(espera)
    for i in range(numEnsambladoras):
        addComponente(0, i,tiempoFinal,espera)
    tipoEvento = componente.MostrarEvento()
    while (LEF): 
        tamMaxCola = max(tamMaxCola, len(colaHorno))
        print (tiempoAct ,"-", tipoEvento,"-" , estadoHorno , "-",tamMaxCola ,"-", mostrarLEF())
        componente = LEF.pop(0)
        tipoEvento = componente.MostrarEvento()
        tiempoAct = componente.tiempo

        if componente.tipo == "L" :
            addComponente(tiempoAct , componente.Ensambladora,tiempoFinal, espera)
            if any(estadoHorno) :
                estadoHorno = addSalida(componente, tiempoAct, estadoHorno) 
            else:
                colaHorno.append(componente)
        else:
            listaComponentes.append(componente)
            aux = componente.Horno
            estadoHorno[aux] = True
           ## print("horno" , estadoHorno)
            if colaHorno:
                estadoHorno = addSalida(colaHorno.pop(0), tiempoAct , estadoHorno)
                
    print (tiempoAct ,"-", tipoEvento,"-" , estadoHorno , "-",tamMaxCola ,"-", mostrarLEF())
    return(referentes(listaComponentes,numHornos,tamMaxCola,tiempoAct))

def referentes(listaDeComponentes, numHornos, colaMax, tfinal):
    CantidadTerminados = len(listaDeComponentes)
    tiempoTotal = tfinal
    PorcentajeHorno = 0  # porcentaje de tiempo
    esperaPromedio = 0  # espera promedio para entrar a horno
    for i in listaDeComponentes:
        PorcentajeHorno += i.tHorno  # suma pero NO es respuesta
        esperaPromedio += i.tLlegadaH - i.tSalidaE

    PorcentajeHorno =round((PorcentajeHorno/(tiempoTotal*numHornos)) * 100,3)  # calcula porcentaje
    esperaPromedio = round(esperaPromedio/len(listaDeComponentes),3)
    return(tiempoTotal, PorcentajeHorno, esperaPromedio, colaMax, CantidadTerminados)   

def promedio(lista):
    prom = 0
    for i in lista:
        prom+=i
    return round(prom/len(lista),3)

def repetir (numRepe , numEmsables, numHornos, tiempo, esperaHorno):
    tiempoTotal, PorcentajeHorno,esperaPromedio,colaMax,cantidadTerminados = [],[],[],[],[]
    for _ in range(numRepe):
        datos = main(numEmsables,numHornos, tiempo,esperaHorno)
        tiempoTotal.append(datos[0])
        PorcentajeHorno.append(datos[1])
        esperaPromedio.append(datos[2])
        colaMax.append(datos[3])
        cantidadTerminados.append(datos[4])
    # Crear una lista con los datos de la tabla
    data = [
        ["tiempo Total", tiempoTotal, promedio(tiempoTotal)],
        ["Porcentaje Horno", PorcentajeHorno, promedio(PorcentajeHorno)],
        ["espera Promedio", esperaPromedio, promedio(esperaPromedio)],
        ["cola Maxima", colaMax, promedio(colaMax)],
        ["cantidad Terminados", cantidadTerminados, promedio(cantidadTerminados)]
    ]

    # Imprimir la tabla con formato
    headers = ["Variable", "Datos", "Promedio"]
    print("------------------------------------------------------------------------")
    print("\033[1mVariables de Desempeño:\033[0m")
    print(f"{numEmsables} Ensambladoras y {numHornos} Hornos, espera {esperaHorno}")
    print(tabulate(data, headers, tablefmt="fancy_grid"))


def buscarMejorOpcion(rangoI,rangoF,numHornos,esperaHorno):
    for numEnsambladoras in range(rangoI,rangoF+1):
        repetir(1,numEnsambladoras,numHornos,960,esperaHorno)

buscarMejorOpcion(6,6,1,0)#primer variante
##buscarMejorOpcion(1,6,1,5)#segunda variante
##buscarMejorOpcion(3,9,2,0)#tercer variante