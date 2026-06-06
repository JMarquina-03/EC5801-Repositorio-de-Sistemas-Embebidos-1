import logging

# Definimos una función para probar logging
def Test_logging():

    # Configuración básica
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s - %(levelname)s]: [%(pathname)s] %(message)s'
    )   

    # Creamos el registrador
    logger: logging.Logger = logging.getLogger(__name__)

    # DEBUG
    logger.debug("Revisando el valor de la variable X")

    # INFO
    logger.info("Copias de seguridad realizadas en este momento")

    # WARNING
    logger.warning("Queda poco espacio en el disco")

    # ERROR
    logger.error("No se pudo hacer cierto cálculo")

    # CRITICAL
    logger.critical("Fuente de alimentación caída")

# Main
if __name__ == "__main__":

    Test_logging()
