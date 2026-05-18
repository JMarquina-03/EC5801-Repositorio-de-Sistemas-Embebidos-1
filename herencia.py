# Creamos la clase Punto
class Punto:

    # Definimos las coordenadas
    __x:int
    __y:int
    __z:int

    # Inicializamos 
    def __init__(self,x,y,z):
        self.__x = x
        self.__y = y
        self.__z = z
        self.point = [x , y, z]

    # Getters    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_z(self):
        return self.__z
    
    # Definimos la suma con un escalar
    def __add__(self, escalar):
        suma_x = self.point[0] + escalar
        suma_y = self.point[1] + escalar
        suma_z = self.point[2] + escalar
        return (suma_x, suma_y, suma_z)
    
    # Definimos la multiplicacion o producto punto como extra
    def __mul__(self, nuevo):

        # Si el otro vector es un objeto Punto hace la multiplicación.
        if isinstance(nuevo, Punto):
            mul_x = self.point[0] * nuevo.point[0]
            mul_y = self.point[1] * nuevo.point[1]
            mul_z = self.point[2] * nuevo.point[2]
        
        # Si el otro vector es una tupla o una lista, tambien ahace la multiplicaión sin dar errores.
        elif isinstance(nuevo, (tuple, list)):
            mul_x = self.point[0] * nuevo[0]
            mul_y = self.point[1] * nuevo[1]
            mul_z = self.point[2] * nuevo[2]

        else:
            print("No se puede hacer la multiplicación")

        return (mul_x, mul_y, mul_z)
    
    # Multiplicar por un escalar en cualquiera de las componentes multi(escalar = 10 , [1,3] (multiplica el escalar en la componente 1 y 3))
    def multi(self, escalar:int , eje:list =[]):
        
        mul_esc = list(self.point)

        for i in eje:

            i_eje =  i-1
            
            if i_eje < 3 and i_eje  >= 0:
                mul_esc[i_eje] = mul_esc[i_eje] * escalar
                resultado = mul_esc[0], mul_esc[1], mul_esc[2]
            
            else:
                resultado = print("Solo hay los ejes: 1, 2 y 3")
            
        return(resultado)

# Definimos la clase Vector
class Vector(Punto):

    # Inicializamos
    def __init__(self, x, y, z ):      
        super().__init__(x, y, z)

    # Definimos un método para calcular la magnitud de dicho vector.
    def magnitud(self):
        origen = [0, 0, 0]
        x = self.get_x() - origen[0]
        y = self.get_y() - origen[1]
        z = self.get_z() - origen[2]
    
        modulo_cuadrado = x*x + y*y + z*z

        modulo = modulo_cuadrado**(1/2)
        return modulo
    
# Ejemplo Calculo Magnitud del vector
vector_1=Vector(3,4,5) 
print(vector_1.magnitud())

# Ejemplo operaciones con el objeto Punto
# Producto punto
punto_A = Punto(1 ,2 ,3)
punto_B = Punto(4 ,5 ,6)
valor_1= punto_A * punto_B
print(valor_1)

# Multiplicación por un escalar en cualquiera de sus ejes. 1=eje x. 2=eje y. 3=eje z
resultado = punto_A.multi(10, eje=[1,3])
print(resultado)
    
        
