# proyecto_seguridad
implementación de ataque de diccionario y fuerza bruta usando Python

# Variables disponibles en archivo .env
* CARPETA_RESULTADOS: carpeta donde serán guardadas las salidas de cada uno de los algoritmos
* CARPETA_CONTRAS: Carpeta donde se hará el indexado del archivo "rockyou.txt" por letra inicial
* PREFIJO_CONTRA: Prefijo que se usara para la creación de los archivos de indexado dentro del programa bash
* CANTIDAD_MAXIMA_FUERZA_BRUTA: longitud teórica máxima de la cadena a revisar por el método de fuerza bruta, tome en cuenta que solo revisara letras minúsculas
* VALOR_MD5_FUERZA_BRUTA: Contraseña a crackear usando el método de fuerza bruta
* VALOR_MD5_DICT: Contraseña a crackear usando el método de diccionario
* VALORES_CONTRAS_BASE: Cantidad máxima de contraseñas a usar por archivo de indexado del archivo "rockyou.txt"
* RESETEO_CONTRAS: hágase "true" para eliminar todo el proceso de indexado y los resultados de los algoritmos y empezar desde 0
