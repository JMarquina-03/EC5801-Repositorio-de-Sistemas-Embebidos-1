# from PYYAML 
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except:
    from yaml import Loader, Dumper

# OS import
from pathlib import Path

# Typing import
from typing import Any, Generic, TypeVar

# generic_t Tipo genérico 
generic_t = TypeVar("generic_t")

class MANEJADOR_ARCHIVOS(Generic[generic_t]):
    __dict : generic_t

    def __init__(self):
        ...
  
    # Creamos el método para leer archivo
    def read_file(self, file_path : Path, modo : str) -> Any:

            if not file_path.exists() or not file_path.is_file():
                print("La ruta suministrada no es válida")
                return None
        
        # Sí la ruta es válida, lee el archivo
            if modo == "r":
                with file_path.open(mode=modo) as file:
                    file_data = load(file, Loader=Loader)
                    return file_data
       

            else:
                with file_path.open(mode=modo) as file:
                    file_data = file.read()
                    return file_data
                
    # Creamos el método para escribir en un archivo     
    def write_file(self, file_path : Path,  data : Any, modo : str) -> None:
        
            if not file_path.parent.exists() or not file_path.is_file():
                print("La ruta suministrada no es válida")
                return None
            
            # Sí la ruta es válida, lee el archivo
            if modo == "w":
                with file_path.open(mode=modo) as file:
                    dump(data, file, Dumper = Dumper)
                    print(f"Archivo guardado en: {file_path}")
    
            else:
                with file_path.open(mode=modo) as file:
                    file.write(data)
                    print(f"Archivo guardado en: {file_path}" )    
# main
if __name__ == "__main__":

    manejador_archivos = MANEJADOR_ARCHIVOS()

    # Prueba
    text_path = Path("./archivo_texto.txt")

    # Datos a escribir:
    datos = {
    'nombre': 'Jose Marquina',
    'edad': 22,
    'universidad': "USB"
    }
    
    # Escribimos 
    manejador_archivos.write_file(text_path, datos, "w")
    
    # Leemos 
    read_text: dict = manejador_archivos.read_file(text_path, "r")
    print("Lectura de texto:", read_text)

    # Parte binaria
    bin_path = Path("./archivo_binario.bin")
    
    # Escribimos binario 
    manejador_archivos.write_file(bin_path, b"\x24\x24\x24\x23\x23\x23\x22\x22\x22\x21\x21\x21" , "wb")
    
    # Leemos binario 
    read_bin: bytes = manejador_archivos.read_file(bin_path, "rb")
    print("Lectura binaria:", read_bin)

               

