#!/bin/bash

#convierte los archivos '.webm' a '.mp3' dentro de la carpeta donde se encuentre el script
#el  mp3 convertido se almacena en la misma carpeta con el nombre original

for FILE in *.webm; do
    echo -e "Processing video '\e[32m$FILE\e[0m'";
    ffmpeg -i "${FILE}" -vn -ab 128k -ar 44100 -y "${FILE%.webm}.mp3";
done;
