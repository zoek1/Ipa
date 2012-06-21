#!/usr/bin/env python
# encoding: utf-8
# -*- mode: python; indent-tab-mode: nil; tab-width: 4 -*-

# Traduce un archivo con extension plymouth a las necesidades del sistema
# actual.
# Copyright (C) 2012  Miguel Angel Gordian <os.aioria@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

# import pdb

# Colores de salida
MORADO   = '\033[95m'
AZUL     = '\033[94m'
VERDE    = '\033[92m'
AMARILLO = '\033[93m'
ROJO     = '\033[91m'
NINGUNO  = '\033[0m'

COLOR = True

# Atributos del tema necesarios
Tema = {"Esquema"     : "Plymouth Theme",
        "Name"        : "",
        "Description" : "",
        "ModuleName"  : ""}

# Lista de Esquemas 
Esquema = []
ListaEsquemas = []

# El esquema por default es "Plymouth Theme"
EsquemaActual = Tema["Esquema"]


def ObtenerAtributos(NombreArchivo):
    """
    Obtener los atributos de un archivo con extensión '.plymouth'
    y codificarlos

    Arguments:
    - `NombreArchivo`: Nombre del Archivo a ser escrito
    """
    bytes = 0
    try:
        ArchivoPlymouth = open(NombreArchivo)
    except IOError:
        print("Error en apertura de Archivo: " , NombreArchivo)
    else:
        for Cadena in ArchivoPlymouth:
            bytes += len(Cadena)
            
            if Cadena == "\n":
                continue
            if (Cadena.count("[") + Cadena.count("]") == 2):
                
                Cadena = Cadena.strip("[")
                Cadena = Cadena.strip("\n")
                Cadena = Cadena.strip("]")
                print("Esquema encontrado",Cadena)
                
                ListaEsquemas.append(Cadena)
                diccionario = {"Esquema" : Cadena}
                
                for atributo in ArchivoPlymouth:
                    bytes += len(atributo)
                    if atributo == "\n":
                        continue
                    elif atributo.count("=") == 1:
                        atributo = atributo.split("=")
                        atributo[0] = atributo[0].strip()
                        atributo[1] = atributo[1].strip("\n")
                        
                        if EsquemaActual == "Plymouth Theme]":
                            Tema[atributo[0]] = atributo[1]
                            diccionario = Tema
                        else:
                            diccionario[atributo[0]]=atributo[1]
                           
                        if COLOR:
                            print("\t|--->",MORADO, "Asociacion", AZUL,
                                  atributo[0],NINGUNO, " - ", VERDE,
                                  atributo[1], NINGUNO)
                        else:
                            print("\t|--->", "Asociacion", atributo[0],
                                  " - ", atributo[1])
                    else:
                        bytes -= len(atributo)

                        # try:
                        #     ArchivoPlymouth.seek(ArchivoPlymouth.tell() -
                        #                          len(atributo))
                        # except IOError:
                        #     print("Reasignacion de puntero en fichero")

                        break
                ArchivoPlymouth.seek(bytes)
                Esquema.append(diccionario)
                
        ArchivoPlymouth.close()



def EscribirPlymouth(NombreArchivo):
    """Escribir al archivo los campos del diccionario
    dando las rutas correctas y el posicionamiento de imagenes
    adecuado para tratar de evitar conflictos
    
    Arguments:
    - `NombreArchivo`: Nombre del Archivo a ser escrito
    """
    try:
        ArchivoPlymouth = open(NombreArchivo,"w")
    except:
        print("no se pudo escribir el archivo")
    else:
#        pdb.set_trace()        
        for Esquemas in Esquema:

            for Atributos in Esquemas:
                if Atributos == "Esquema":
                    ArchivoPlymouth.write("[" + Esquemas["Esquema"] +"]\n")
                else:
                    ArchivoPlymouth.write(Atributos+"=")
                    ArchivoPlymouth.write(Esquemas[Atributos]+"\n")

            ArchivoPlymouth.write("\n")

        ArchivoPlymouth.close()


#if __name__ == "__main":
ObtenerAtributos("Aztli/aztli-os.plymouth")
EscribirPlymouth("salida.plymouth")
