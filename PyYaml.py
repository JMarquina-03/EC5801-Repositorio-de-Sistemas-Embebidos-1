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
           
    def write_file(self, file_path : Path,  data : Any, modo : str) -> None:
        
            if not file_path.parent.exists():
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

class YAML_ARCHIVOS(MANEJADOR_ARCHIVOS):


    def __init__(self):
        super().__init__()
        self.__dictionary : dict = {}

    # Metodo de sintetización de archivo a .YAML
    def sintetizar_YAML(self, file_path : Path):

        # Guardamos el stream leído en una varible tipo diccionario
        datos = self.read_file(file_path, "r")
        # Me interesa el nombre del archivo de la PATH colocada
        name = file_path.name

        # Diccionario dentro de otro diccionario
        self.__dictionary[name] = {
            "path": str(file_path),
            "data": datos
        }

        # Devolvemos el diccionario privado por si hace falta utilizarlo
        return self.__dictionary
     
    # Getter para que permita obtener los diccionarios correspondientes basados en el nombre asignado
    def get_dictionary(self):
        return self.__dictionary

    # Método para modificar un archivo
    def modification(self, identificador: str, datos_actualizados : dict):

        # Verificamos si el nombre del archivo a pasar ya fue sintetizado a .YAML
        if identificador in self.__dictionary:

            print(f"Los datos anteriores son : '{self.__dictionary[identificador]["data"]}'")

            self.__dictionary[identificador]["data"] = datos_actualizados

            print(f"Los datos actualizados son: '{self.__dictionary[identificador]["data"]}")

        else:
            
            print("El archivo a modificar no existe")

    # Método para guardar el archivo        
    def save(self, name : str):
        if name in self.__dictionary:
            self.write_file(Path(self.__dictionary[name]["path"]), self.__dictionary[name]["data"], "w")        
        else:
            print("No se guardaron los datos")    

# main
if __name__ == "__main__":
    # Creamos el objeto
    yaml_archivo = YAML_ARCHIVOS()

    # Definimos las rutas
    path_prueba = Path("./prueba.yaml")
    path_prueba1 = Path("./prueba_1.yaml")
    
    # Guardamos los datos de un archivo para escribirlos en otr archivo, verificando el correcto funcionamiento.
    data_1 = yaml_archivo.read_file(path_prueba, "r")
    yaml_archivo.write_file(path_prueba1, data_1, "w")

    # Sintetizamos
    yaml_archivo.sintetizar_YAML(path_prueba)
    yaml_archivo.sintetizar_YAML(path_prueba1)

    # Modificamos uno de los archivos
    nuevos_datos = {"Trabajador": "Pedro", "Cedula": 123456789}
    yaml_archivo.modification("prueba.yaml", nuevos_datos)

    # Guardamos el archivo ya modificado.
    yaml_archivo.save("prueba.yaml")