import logging

import threading

import time

from queue import Queue

from typing import Callable, Any, Dict, Optional

# Configuración basica de los logging.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(name)s - %(levelname)s]: [%(pathname)s] %(message)s'
)
# Creamos la clase.
class Messages_Manager:
    
    # Inicializamos 
    def __init__(self):
        self.dictionary_queues: dict = {}
        self.dictionary_callbacks: dict = {}
        self.thread_lock = threading.Lock()

    # Método que crea la cola y le relacionamos un Callback.
    def create(self, name_queue: str, num_max: int, function : Callable) -> None:
        if name_queue in self.dictionary_queues:
            logging.error("Ya la cola fue creada")
        else:
            with self.thread_lock:
                self.dictionary_queues[name_queue] = Queue(maxsize=num_max)
                self.dictionary_callbacks[name_queue] = function

    # Método que elimina la cola 
    def delete(self, name_queue: str) -> None:
        with self.thread_lock:    
            if name_queue in self.dictionary_queues:
                self.dictionary_queues.pop(name_queue)
                self.dictionary_callbacks.pop(name_queue)

            else:
                logging.error("No hay una cola registrada con ese nombre")

    # Método para enviar datos a una cola
    def send(self, datos: Any, name_queue: str) -> None:

        with self.thread_lock:
            if name_queue not in self.dictionary_queues:
                logging.error("La cola no existe")
                return
        # Si los datos son una lista o tupla, los itera.
        if isinstance(datos,(list, tuple)):      
            for i in datos:
                # Block=True bloquea si es necesario hasta que un espacio libre esté disponible.
                self.dictionary_queues[name_queue].put(i, block=True)

        else:
            # En caso de que sea un solo dato como (int, float, str)
            self.dictionary_queues[name_queue].put(datos, block=True)

    # Método para extraer datos de una cola.
    def receive(self, name_queue: str) -> Any:
        
        with self.thread_lock:
            if name_queue not in self.dictionary_queues:
                logging.error("La cola no existe")
                return
            
            # Mientras que la cola tenga datos los sacamos todos
            if (self.dictionary_queues[name_queue].empty() == False):

                data = self.dictionary_queues[name_queue].get(block=False)
                return data
            
            else:
                logging.info("La cola está vacía")
                return None
            
    # Método para asignar los datos que tienen las colas a las funciones correspondientes        
    def poll(self):
        
        for key in self.dictionary_queues.keys():
            if(self.dictionary_queues[key].empty() == True):
                logging.info(f"La cola {key} no se activo porque está vacía")
            
            else:
                while(self.dictionary_queues[key].empty() == False):
                    data = self.receive(key)   

                    with self.thread_lock:
                        function = self.dictionary_callbacks[key]
                
                    function(data)

# Definimos funcion callback
def  funcion_datos(dato: Any):
    print(f"CALLBACK con el siguiente dato: {dato} ")

# Main
if __name__ == '__main__':
    # Creamos un objeto
    gestor = Messages_Manager()

    # Creamos "cola 1" y la relacionamos con un Callback
    gestor.create("cola_1", 3, funcion_datos)

    # Creamos una cola y la eliminamos.
    gestor.create("cola_2", 5, funcion_datos)
    gestor.delete("cola_2")

    # Imprimirá un mensaje que la cola no existe porque fue eliminada.
    gestor.send((22,23,24), "cola_2")

    lista: list = ["José", "Alejandro", 22, 2003, "Marquina", "20-10412"]

    # Creamos un hilo secundario y lo inicializamos
    hilo_secundario = threading.Thread(target=gestor.send, args=(lista, "cola_1"))
    hilo_secundario.start()

    # Extraigo dato de la "cola_1".
    datos_extraidos = gestor.receive("cola_1")
    print(f"El dato extraido es: {datos_extraidos}")

    gestor.poll()
    hilo_secundario.join()