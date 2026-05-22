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

# Typing Import #
from typing import Any

# Schema validator function import
from schema_validator import schema_validator

# Validate this schema
schema_persona : dict = [{
    "nombre" : str,
    "altura" : float,
    "peso" : float,
    "edad" : int,
    "lista de habilidades" : list,
    "descripcion" : str
}]

# fabric
@schema_validator(schema_persona)
# function to decorate
def verificador_datos(data: Any):
    return data

# generic_t type generic 
generic_t = TypeVar("generic_t")

class MANEJADOR_ARCHIVOS(Generic[generic_t]):
    __dict : generic_t

    def __init__(self):
        ...

    def read_file(self, file_path : Path, modo : str) -> Any:

            if not file_path.exists() or not file_path.is_file():
                print("La ruta suministrada no es válida")
                return None
        
        # if the path is valid, read file
            if modo == "r":
                with file_path.open(mode=modo) as file:
                    file_data = load(file, Loader=Loader)
                    return file_data
       
            # for other modes
            else:
                with file_path.open(mode=modo) as file:
                    file_data = file.read()
                    return file_data
           
    def write_file(self, file_path : Path,  data : Any, modo : str) -> None:
        
            if not file_path.parent.exists():
                print("La ruta suministrada no es válida")
                return None
            
            # if the path is valid, write file
            if modo == "w":
                with file_path.open(mode=modo) as file:
                    dump(data, file, Dumper = Dumper)
                    print(f"Archivo guardado en: {file_path}")
            # for other modes
            else:
                with file_path.open(mode=modo) as file:
                    file.write(data)
                    print(f"Archivo guardado en: {file_path}" ) 

class YAML_ARCHIVOS(MANEJADOR_ARCHIVOS):


    def __init__(self):
        super().__init__()
        self.__dictionary : dict = {}

    # Synthesis of file to .YAML
    def sintetizar_YAML(self, file_path : Path):

        # We store the read stream in a dictionary type variable
        datos = self.read_file(file_path, "r")
        # I'm interested in the filename of the PATH
        name = file_path.name

        # Dictionary within another dictionary
        self.__dictionary[name] = {
            "path": str(file_path),
            "data": datos
        }

        # Returning the private dictionary in case it is needed.
        return self.__dictionary
     
        # Getter to allow obtaining the corresponding dictionaries based on the assigned name
    def get_dictionary(self):
        return self.__dictionary

    # Method to modify a file
    def modification(self, identificador : str, datos_actualizados : dict):
        
        # We check if the filename to be passed has already been synthesized to .YAML
        if identificador in self.__dictionary:
            
            # Verify if the new data complies with the scheme
            if verificador_datos(datos_actualizados) is None:
                print("Los nuevos datos no cumplen con el schema")
                return 
            
            print(f"Los datos anteriores son : '{self.__dictionary[identificador]["data"]}'")

            self.__dictionary[identificador]["data"] = datos_actualizados

            print(f"Los datos actualizados son: '{self.__dictionary[identificador]["data"]}")

        else:
            
            print("El archivo a modificar no existe")

    # Method for saving the file        
    def save(self, name : str):
        if name in self.__dictionary:

            data_new = self.__dictionary[name]["data"]

            if verificador_datos(data_new) is not None:
                self.write_file(Path(self.__dictionary[name]["path"]), data_new, "w")
           
            else:
                 print(f"Los datos de '{name}' estan errados")    
        
        else:
            print("No se guardaron los datos")

# Main
if __name__ == "__main__":
    # Create the object
    yaml_archivos = YAML_ARCHIVOS()

    # TEST
    path_prueba1 = Path("./prueba_1.yaml")
    path_prueba2 = Path("./newdata.yaml")
    
    data_correcta = [{
        "nombre" : "Jose",
        "altura" : 1.80,
        "peso" : 70.0,
        "edad" : 22,
        "lista de habilidades" : ["Agil", "Entendedor"],
        "descripcion" : "Estudiante de la USB"
    }]

    data_incorrecta = {  
        "nombre" : "Cheo",
        "altura" : 10,
        "peso" : 70.0,
        "edad" : 12.5,
        "lista de habilidades" : "Agil",
        "descripcion" : "Estudiante de la USB"
    }
    # Write in test file the data_correcta
    yaml_archivos.write_file(path_prueba1, data_correcta, "w")

    yaml_archivos.sintetizar_YAML(path_prueba1)
    yaml_archivos.sintetizar_YAML(path_prueba2)

    newdata = yaml_archivos.read_file(path_prueba2, "r")

    # You can test this by modifying the file with "data_incorrect" or "new_data"
    yaml_archivos.modification("prueba_1.yaml", newdata) 

    # Nota: Se guarda el archivos con los datos anteriormente correctos, cuando se intenta modificar con una data incorrecta.
    yaml_archivos.save("prueba_1.yaml")