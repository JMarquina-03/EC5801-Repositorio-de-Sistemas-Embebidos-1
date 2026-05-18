import time

# Creamos la clase Disco_duro
class disco_duro:
    delay_lectura: float = 0.1
    delay_escritura: float = 0.2

    # Inicializamos
    def __init__(self, tamaño: int):
        self.tamaño = tamaño
        espacio_vacio: list = [None]
        self.ssd = espacio_vacio * tamaño

    # Definimos el método para la lectura de esta clase
    def lectura(self, posicion: int):

        # Añadimos el retraso 
        time.sleep(self.delay_lectura)

        if posicion >= self.tamaño:
             print("Error al leer")
             return None
        else:
            self.posicion = posicion
        return self.ssd[posicion]
    
    # Definimos el método para la escritura de esta clase
    def escritura(self, posicion: int, data: str):

        # Añadimos el retraso
        time.sleep(self.delay_escritura)

        if posicion >= self.tamaño:
             print("Error al escribir. la posición de memoria es inválida")
             return None
        else:
            self.posicion = posicion
            self.data = data
            self.ssd[posicion] = data

# Creamos la clase memoria_ram
class memoria_ram:
    delay_lectura: float = 0.05
    delay_escritura: float = 0.1
    # Inicializamos
    def __init__(self, tamaño: int):
        self.tamaño = tamaño
        espacio_vacio: list = [None]
        self.ram = espacio_vacio * tamaño

    # Definimos el método para la lectura de esta clase
    def lectura(self, posicion: int):

        # Añadimos el retraso 
        time.sleep(self.delay_lectura)

        if posicion >= self.tamaño:
             print("Error al leer")
             return None
        else:
            self.posicion = posicion
            
        return self.ram[posicion]
    
    # Definimos el método para la escritura de esta clase
    def escritura(self, posicion: int, data: str):

        # Añadimos el retraso
        time.sleep(self.delay_escritura)

        if posicion >= self.tamaño:
             print("Error al escribir. la posición de memoria es inválida")
             return None
        else:
            self.posicion = posicion
            self.data = data
            self.ram[posicion] = data
        

class memoria_sram:
    delay_lectura: float = 0.001
    delay_escritura: float = 0.005

    # Inicializamos
    def __init__(self, tamaño:int):
        self.tamaño = tamaño
        espacio_vacio: list = [None]
        self.sram = espacio_vacio * tamaño

    # Definimos el método para la lectura de esta clase
    def lectura(self, posicion: int):

        # Añadimos el retraso 
        time.sleep(self.delay_lectura)

        if posicion >= self.tamaño:
             print("Error al leer")
             return None
        else:
            self.posicion = posicion
        return self.sram[posicion]
    
    # Definimos el método para la escritura de esta clase
    def escritura(self, posicion: int, data: str):

        # Añadimos el retraso 
        time.sleep(self.delay_escritura)

        if posicion >= self.tamaño:
             print("Error al escribir. la posición de memoria es inválida")
             return None
        else:
            self.posicion = posicion
            self.data = data
            self.sram[posicion] = data

# función para escribir en la memoria específica (Polimorfismo)
def escribir(tipo_memoria, posicion: int, data: str):
    return tipo_memoria.escritura(posicion,data)

# función para leer la memoria específica (polimorfismo)
def leer(tipo_memoria, posicion: int):
    return tipo_memoria.lectura(posicion)

# Ejemplo

ssd = disco_duro(100)
ram = memoria_ram(10)
sram = memoria_sram(10)

escribir(ssd, 99, "20000000")
escribir(ssd, 2, "buenas tardes")
escribir(ram, 1, "Jose")
escribir(sram, 3, "Zapatos")

print(leer(ssd, 99))
print(leer(ssd, 2))
print(leer(ram, 1))
print(leer(sram, 3))
