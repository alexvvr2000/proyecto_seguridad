from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import md5
from itertools import product
from os import getenv
from pathlib import Path
from string import ascii_lowercase
from threading import Lock
from typing import Optional


class ContadorIntentos:
    valor: int

    def __init__(self):
        self.valor = 0
        self._lock = Lock()

    def sumar(self):
        with self._lock:
            self.valor += 1
            return self.valor


def fuerza_bruta(
    md5_introducido: str, longitud_clave: int, contador_intentos: ContadorIntentos
) -> Optional[str]:
    for combinacion in product(ascii_lowercase, repeat=longitud_clave):
        valor_comparado = "".join(combinacion).strip()
        md5_actual = md5(valor_comparado.encode("utf-8")).hexdigest()
        if md5_actual == md5_introducido:
            return valor_comparado
        contador_intentos.sumar()
        print(f"{valor_comparado} -> {md5_actual} == {md5_introducido}")
    return None


if __name__ == "__main__":
    CANTIDAD_LETRAS_ENV = getenv("CANTIDAD_MAXIMA_FUERZA_BRUTA")
    if CANTIDAD_LETRAS_ENV is None or not str.isdigit(CANTIDAD_LETRAS_ENV):
        raise EnvironmentError(
            "Valor introducido de la cantidad de hilos no es numerico"
        )
    MD5_ENV = getenv("VALOR_MD5_FUERZA_BRUTA")
    if MD5_ENV is None:
        raise EnvironmentError("Valor introducido como MD5 no es correcto")
    CANTIDAD_LETRAS = int(CANTIDAD_LETRAS_ENV)
    contador_intentos = ContadorIntentos()
    with ThreadPoolExecutor(max_workers=CANTIDAD_LETRAS) as ejecucion_fuerza_bruta:
        futuros_fuerza_bruta = {
            ejecucion_fuerza_bruta.submit(
                fuerza_bruta, MD5_ENV, longitud, contador_intentos
            ): longitud
            for longitud in range(1, CANTIDAD_LETRAS + 1)
        }
        carpeta_resultados = getenv("CARPETA_RESULTADOS")
        mensaje_final: str
        if carpeta_resultados is None:
            raise FileNotFoundError("La carpeta de resultados no existe")
        for tarea_futuro in as_completed(futuros_fuerza_bruta):
            longitud_intento = futuros_fuerza_bruta[tarea_futuro]
            try:
                valor_retorno = tarea_futuro.result()
            except Exception as error:
                print(
                    f"Se genero una excepcion cuando se empezo con la longitud {longitud_intento}: {error}"
                )
            else:
                if valor_retorno is None:
                    mensaje_final = f"No se encontro la contraseña despues de {contador_intentos.valor} intentos"
                else:
                    mensaje_final = (
                        f"MD5 original: {MD5_ENV}\n"
                        f"Contraseña sin encriptar: {valor_retorno}\n"
                        f"Intentos: {contador_intentos.valor}\n\n"
                    )
                    ejecucion_fuerza_bruta.shutdown(wait=False)
                    break
        with open(
            Path(carpeta_resultados, "resultados_fuerza_bruta.txt"), "a+"
        ) as archivo_resultado:
            archivo_resultado.write(mensaje_final)
