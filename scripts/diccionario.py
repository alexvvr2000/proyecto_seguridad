from pathlib import Path
from typing import Optional, Iterator, Awaitable
from string import ascii_lowercase
from aiofiles import open
from hashlib import md5
from os import getenv
from asyncio import Lock, as_completed, run


class ContadorIteraciones:
    valor: int
    lock: Lock

    def __init__(self):
        self.valor = 0
        self.lock = Lock()

    async def incrementar(self):
        async with self.lock:
            self.valor += 1
            return self.valor


async def revisar_archivo(
    direccion_contra: Path, valor_md5: str, contador: ContadorIteraciones
) -> Optional[str]:
    async with open(direccion_contra, "r") as archivo_actual:
        async for contra_actual in archivo_actual:
            contra_limpia = contra_actual.rstrip("\r\n")
            md5_contra_actual = md5(contra_limpia.encode("utf-8")).hexdigest()
            await contador.incrementar()
            if md5_contra_actual == valor_md5:
                return contra_limpia
            print(
                f"{contra_limpia} -> {valor_md5} en {direccion_contra.name} == {valor_md5}"
            )
    return None


def crear_tareas_lectura(
    valor_md5: str, contador: ContadorIteraciones
) -> Iterator[Awaitable[Optional[str]]]:
    carpeta_archivos_texto = getenv("CARPETA_CONTRAS")
    if carpeta_archivos_texto is None:
        raise EnvironmentError(
            "La carpeta con los archivos de texto base no se definio"
        )
    prefijo_contra = getenv("PREFIJO_CONTRA")
    for letra_archivo in ascii_lowercase:
        archivo_contra = Path(
            carpeta_archivos_texto, f"{prefijo_contra}_{letra_archivo}.txt"
        )
        yield revisar_archivo(archivo_contra, valor_md5, contador)


async def main(valor_md5: str) -> None:
    contador_iteraciones = ContadorIteraciones()
    tareas_contras = crear_tareas_lectura(valor_md5, contador_iteraciones)
    carpeta_resultados = getenv("CARPETA_RESULTADOS")
    mensaje_final: str
    if carpeta_resultados is None:
        raise FileNotFoundError("La carpeta de resultados no existe")
    for tarea_terminada in as_completed(tareas_contras):
        resultado_tarea = await tarea_terminada
        if resultado_tarea is None:
            mensaje_final = "No se encontro la contraseña despues de" \
                f"{contador_iteraciones.valor} iteraciones\n\n"
        else:
            mensaje_final = (
                f"Contraseña encriptada: {valor_md5}\n"
                f"Contraseña desencriptada: {resultado_tarea}\n"
                f"Cantidad de iteraciones: {contador_iteraciones.valor}\n\n"
            )
            break
    async with open(
        Path(carpeta_resultados, "resultados.txt"), "a+"
    ) as archivo_resultados:
        await archivo_resultados.write(mensaje_final)


if __name__ == "__main__":
    valor_md5 = getenv("VALOR_MD5_DICT")
    if valor_md5 is None:
        raise EnvironmentError("El valor md5 no fue introducido en .env")
    run(main(valor_md5))
