# Definimos la clase Matriz
class Matriz:
    #Variale para almacenar la matriz
    data: list = []

    # Inicializamos la clase Matriz
    def __init__(self, data):
        self.data  = data

        # Definimos el numero de filas
        self.filas = len(data)

        #Definimos el numero de columnas
        total_elementos = 0
        for fila in data:
            total_elementos += len(fila)
        self.columnas = total_elementos//self.filas

    # Definimos la operación de suma 
    def __add__(self,nueva):
        resultado_suma = []
        for i in range(self.filas):
            fila_temp = []
            for j in range(self.columnas):
                suma_elementos = self.data[i][j] + nueva.data[i][j]
                fila_temp.append(suma_elementos)
            resultado_suma.append(fila_temp)
        return Matriz(resultado_suma)
    
    # Definimos la operacion resta
    def __sub__(self,nueva):
        resultado_resta = []
        for i in range(self.filas):
            fila_temp = []
            for j in range(self.columnas):
                resta_elementos = self.data[i][j] - nueva.data[i][j]
                fila_temp.append(resta_elementos)
            resultado_resta.append(fila_temp)
        return Matriz(resultado_resta)
    
    # Definimos la multiplicación
    def __mul__(self,nueva):
        # Si el numero de columnas de la primera es igual al numero de filas de la segunda, se define la multiplicación.
        if self.columnas == nueva.filas:
            resultado_mul = []
            for i in range(self.filas):
                fila_temp = []
                for j in range(nueva.columnas):
                    suma_producto = 0
                    for k in range(self.columnas):
                        mul_elementos = self.data[i][k] * nueva.data[k][j]
                        suma_producto += mul_elementos
                    fila_temp.append(suma_producto)
                resultado_mul.append(fila_temp)
            return Matriz(resultado_mul)
        # Si no concuerda la regla anterior, entonces no se puede llevar a cabo la operación
        else:
            print("No se puede llevar a cabo la operación debido a sus dimensiones")

    # Se deshabilita la operación de división
    def __truediv__(self, nueva):
         return print("La división de matrices no está definida")
         

    # Definimos cómo se debe representar la matriz como texto
    def __str__(self):
        resultado = ""
        for fila in self.data:
            # Se convierte cada fila a texto y agregamos un salto de línea
            resultado += str(fila) + "\n"
        return resultado
    
# Probamos 

matriz_A = Matriz([ [1, 2, 3],
                    [4, 5, 6], 
                    [1, 2, 3]])

print(matriz_A)

matriz_B = Matriz([ [10, 10, 3],
                    [20, 20, 4],
                    [30, 30, 5]])

print(matriz_B)

resultado_1 = matriz_A + matriz_B
resultado_2 = matriz_A - matriz_B
resultado_3 = matriz_A * matriz_B

print("Resultado de Matriz A + Matriz B")
print(resultado_1)

print("Resultado de Matriz A - Matriz B")
print(resultado_2)        

print("Resultado de Matriz A * Matriz B")
print(resultado_3)

# Aparecerá un mensaje que menciona que no está definida la división
resultado_4 = matriz_A / matriz_B
