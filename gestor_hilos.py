import logging

import threading

import time

from typing import Callable, Any, Dict, Optional

# Para poder implementar este código investigué del siguiente link y varios videos de youtube:
# https://stackoverflow.com/questions/10525185/python-threading-how-do-i-lock-a-thread
# https://docs.python.org/es/3.9/library/threading.html

# Configuración basica de los logging.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(name)s - %(levelname)s]: [%(pathname)s] %(message)s'
)

# Definimos la clase Gestor
class Gestor:

    # Inicializamos la clase
    def __init__(self, cantidad_hilos: int):
        self.cantidad_hilos = cantidad_hilos
        self.hilos_registrados: dict =  {}
        self.callbacks_asignados: dict = {}
        self.hilos_activos: int = 0
        self.thread_lock = threading.Lock()

    # Método para la asignación del hilo.
    def Thread_Allocate(self, name_thread: str, function: Callable, *args, **kwargs):

        hilo = threading.Thread(target=self.Thread_execute, name=name_thread, args=(name_thread,))

        self.hilos_registrados[name_thread] = {
            "hilo" : hilo,
            "funcion ejecutada" : function,
            "args" : args,
            "kwargs" : kwargs
        }

        self.callbacks_asignados[name_thread] = {
            'Callback_Start': None,
            'Callback_End': None
        }

    # Creamos este método para que sea llamado por otro método en cuanto a la gestión de los hilos.
    # Aqui es donde se ejecutará la función principal, el hilo no comenzará hasta que se llamé al metodo Thread_Start 
    # el cual es donde se inicia los correspondientes hilos con .start() y empieza con el Callback_start en caso de 
    # que haya.
    def Thread_execute(self, name_thread: str):

        # Tomamos la información del hilo 
        datos_hilo = self.hilos_registrados[name_thread]
        main_funcion = datos_hilo["funcion ejecutada"]
        args = datos_hilo["args"]
        kwargs = datos_hilo["kwargs"]

        # Ejecutamos la función pricipal
        main_funcion(*args, **kwargs)

        # Ejecutamos el callback_End
        if self.callbacks_asignados[name_thread]['Callback_End']:
            self.callbacks_asignados[name_thread]['Callback_End']()

        # A medida que cada hilo ejecute su tarea va quedando espacio en hilos activos para la ejecución de otros hilos.
        with self.thread_lock:
            self.hilos_activos -= 1

    # Metodo para registrar Callback
    def Thread_Callback_Register(self, name_thread: str, callback_start: Callable = None, callback_end: Callable = None):
        if name_thread in self.hilos_registrados:
            
            # Si el hilo pasado como argumento esta ocupado retornará un mensaje de información.
            if self.hilos_registrados[name_thread]["hilo"].is_alive():
                logging.info("El hilo esta ocupado, elija otro")

            # Si no le asignamos los Callback al hilo ingresado.
            else:
                if callback_start:
                    self.callbacks_asignados[name_thread]['Callback_Start'] = callback_start
                if callback_end:    
                    self.callbacks_asignados[name_thread]['Callback_End'] = callback_end
                logging.info(f"Callback registrado en '{name_thread}'")
                
        else:
            logging.warning("El hilo ingresado no existe")
    
    # Clase para arrancar el hilo 
    def Thread_Start(self, name_thread: str):
        if name_thread in self.hilos_registrados:
            
            # Bucle infinito
            while True:
                # Con el hilo puesto el candado
                with self.thread_lock:
                    if self.hilos_activos < self.cantidad_hilos:
                        self.hilos_activos += 1
                        # Sale del while
                        break
                # Espera hasta que haya un hilo activo disponible
                time.sleep(1)

            try:
                # Si hay callback de inicio, se ejecuta
                if self.callbacks_asignados[name_thread]['Callback_Start']:
                    self.callbacks_asignados[name_thread]['Callback_Start']()
                
                # Se arranca el hilo
                self.hilos_registrados[name_thread]['hilo'].start()  
            except:
                logging.error("Algo falló al ejecutar el Callback_Start")
                
        else:
            logging.error("No se pudo iniciar. El hilo ingresado no existe.")

    #Funciones a utilizar
def program(program_name: str, duration: int):
    logging.info(f"Iniciando {program_name}...")
    # Se simula el tiempo que tarda la tarea.
    time.sleep(duration)
    logging.info(f"Finalizando {program_name} con un tiempo de {duration}seg ")

def callback_inicio():
    logging.info("CALLBACK INICIO")

def callback_fin():
    logging.info("CALLBACK FINAL")

# Main
if __name__ == "__main__":
    gestor = Gestor(2)

    logging.info("Empezamos Test")

    # Asignamos 3 hilos
    gestor.Thread_Allocate("hilo_1", program, "GTA.exe", 4)
    gestor.Thread_Allocate("hilo_2", program, "Proteus.exe", 5)
    gestor.Thread_Allocate("hilo_3", program, "Youtube", 6)

    # Asignamos Callback solo a un hilo
    gestor.Thread_Callback_Register("hilo_1", callback_start=callback_inicio, callback_end=callback_fin)

    #Iniciamos los hilos
    gestor.Thread_Start("hilo_1")
    gestor.Thread_Start("hilo_2")
    gestor.Thread_Start("hilo_3")
