#!/bin/bash

if [ ! -d "${CARPETA_RESULTADOS}" ]; then
    echo "Carpeta '${CARPETA_RESULTADOS}' no existe en imagen"
    exit 1;
fi

archivo_zip="${CARPETA_RESULTADOS}/rockyou.txt.tar.gz"
if [ ! -f $(realpath "${archivo_zip}") ]; then
    wget \
        --verbose \
        --output-document=${archivo_zip} \
        https://github.com/zacheller/rockyou/raw/master/rockyou.txt.tar.gz
fi

if [ ! -d "${CARPETA_CONTRAS}" ]; then
    mkdir "${CARPETA_CONTRAS}"
    tar -xvf "${archivo_zip}" -C "${CARPETA_CONTRAS}"
    abc="abcdefghijklmnñopqrstuvwxyz"
    for (( i=0; i<${#abc}; i++ )); do
        letra_actual="${abc:$i:1}"
        nuevo_archivo="${CARPETA_CONTRAS}/${PREFIJO_CONTRA}_${letra_actual}.txt"
        archivo_original="${CARPETA_CONTRAS}/rockyou.txt"
        touch ${nuevo_archivo}
        cat "${archivo_original}" | grep ^${letra_actual} > ${nuevo_archivo} &
    done
fi