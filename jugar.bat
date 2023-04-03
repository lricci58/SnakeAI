@echo Instalando librerias necesarias...
pip install numpy==1.19.1
pip install matplotlib==3.3.0
pip install pygame==1.9.6
cls

@echo El juego comenzara en breves...
@echo Debe saber que la IA aprende con el tiempo.
@echo Tardara unas 4 o 5 generaciones en jugar decentemente. Disfrute!

@echo off

> where python.exe "juego.py"
