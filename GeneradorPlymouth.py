#!/usr/bin/env python3

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

import os

import pdb
import EsquemaT

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


def ObtenerAtributos(NombreArchivo,COLOR=False):
    """
    Obtener los atributos de un archivo con extension .plymouth
    y codificarlos.

    Arguments:
    - `NombreArchivo`: Nombre del Archivo a ser escrito.
    """
    # pdb.set_trace()
    ListaEsquemas = []

    # El esquema por default es "Plymouth Theme"

    bytes = 0
    try:
        ArchivoPlymouth = open(NombreArchivo)
    except IOError:
        print("Error en apertura de Archivo: ", NombreArchivo)
    else:
        for Cadena in ArchivoPlymouth:
            bytes += len(Cadena)

            if Cadena == "\n":
                continue
            if (Cadena.count("[") + Cadena.count("]") == 2):

                Cadena = Cadena.strip("[")
                Cadena = Cadena.strip("\n")
                Cadena = Cadena.strip("]")
                print("Esquema encontrado", Cadena)

                EsquemaActual = EsquemaT.Esquema(Cadena)

                for atributo in ArchivoPlymouth:
                    bytes += len(atributo)
                    if atributo == "\n":
                        continue
                    elif atributo.count("=") == 1:
                        atributo = atributo.split("=")
                        atributo[0] = atributo[0].strip()
                        atributo[1] = atributo[1].strip("\n")

                        EsquemaActual.setElemento(atributo[0],atributo[1])
                        # if EsquemaActual == "Plymouth Theme]":
                        #     Tema[atributo[0]] = atributo[1]
                        #     diccionario = Tema
                        # else:
                        #     diccionario[atributo[0]]=atributo[1]

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
                ListaEsquemas.append(EsquemaActual)

        ArchivoPlymouth.close()

        return ListaEsquemas

def EscribirEsquema(Archivo,Esquema,Modo="a+"):
    """Escribir al archivo los campos del diccionario
    dando las rutas correctas y el posicionamiento de imagenes
    adecuado para tratar de evitar conflictos.

    Arguments:
    - `NombreArchivo`: Nombre del Archivo a ser escrito
    - `ListaEsquemas`: Lista que contiene elementos tipo Esquema
    - `Modo`:  Modo de escritura sobresescribir o al final de archivo
    """
    try:
        Plymouth = open(Archivo,Modo)
    except IOError:
        print("No se pudo escibir el archivo")
    else:
        Plymouth.write("[" + Esquema.getTitle() + "]" + "\n")
        for Atributos in Esquema.listAtributo():
            print("Atributo: " + Atributos
                  + " Valor: " + Esquema.getElemento(Atributos))
            Plymouth.write(Atributos + " = " +
                           Esquema.getElemento(Atributos) +"\n")

        Plymouth.close()


def EscribirPlymouth(NombreArchivo,ListEsquemas, Modo="a+"):
    """Escribir al archivo los campos del diccionario
    dando las rutas correctas y el posicionamiento de imagenes
    adecuado para tratar de evitar conflictos.

    Arguments:
    - `NombreArchivo`: Nombre del Archivo a ser escrito
    - `ListaEsquemas`: Lista que contiene elementos tipo Esquema
    - `Modo`:  Modo de escritura sobresescribir o al final de archivo
    """
    # pdb.set_trace()
    try:
        os.remove(NombreArchivo)
    except:
        pass

    for Esquemas in ListEsquemas:
        print("Escribiendo Esquema: %s " % Esquemas.getTitle())
        EscribirEsquema(NombreArchivo, Esquemas, Modo)




def setTitulo(Titulo = None, Esquema = None):
    """Si un titulo es dado se asignara un esquema con el mismo valor
    de titulo, si no es dado el titulo se tomara un modo interactivo
    que preguntara por el valor de titulo del esquema.

    Arguments:
    - `Titulo`: Nombre del titulo del nuevo esquema por defecto es None
    """
    if Esquema is None:
        Esquema = EsquemaT.Esquema()

    while not Titulo:
        Titulo = raw_input("Introduce el Nombre del plymouth")
    print("Nombre del esquema: " + Titulo)
    Esquema.setTitle(Titulo)

    return Esquema


def LeerEsquema(Titulo = None, Esquema = None):
    """Establece un metodo para introducir el identificador del esquema,
    y sus respectivos elementos como son los atributo y su valor.

    Devolvera un objeto de tipo Esquema.
    """

    opcion   = "s"

    esquema = setTitulo(Titulo = Titulo, Esquema=Esquema)

    while opcion == "s" or opcion == "S":
        atributo = None
        valor    = None

        while not atributo:
            atributo = raw_input("Introduce el identificador atributo: ")

        while not valor:
            valor = raw_input("Introduce el valor del atributo: ")

        # Establecer elemento del esquema
        esquema.setElemento(atributo,valor)

        opcion = raw_input("Desea ingresar otro campo para el esquema s/n")

    return esquema


def IPlymouth():
    """Metodo interectivo para crear un archivo con extension ".plymouth"
    """
    ListEsquema = []
    Name = Description = ModuleName = False
    ImageDir = ScriptFile = False

    Cabecera = EsquemaT.Esquema()
    Modulo = EsquemaT.Esquema()

    # Lectura de cabecera de plymouth
    Cabecera.setTitle("Plymouth Theme")

    while not Name:
        Name = raw_input("Introduce el nombre del tema: ")

    while not Description:
        Description = raw_input("Introduce una descripcion del tema: ")

    while not ModuleName:
        ModuleName = raw_input("Introduce el nombre del modulo del plymouth: ")

    Cabecera.setElemento("Name", Name)
    Cabecera.setElemento("Description", Description)
    Cabecera.setElemento("ModuleName", ModuleName)

    if ModuleName == "script":
        while not ImageDir:
            ImageDir = raw_input("Directorio de Imagenes para el plymouth: ")

        while not ScriptFile:
            ScriptFile = raw_input("Direccion del archivo script del plymouth: ")

        Modulo.setTitle(ModuleName )
        Modulo.setElemento("ImageDir", ImageDir)
        Modulo.setElemento("ScriptFile", ScriptFile)
    else:
        Modulo = LeerEsquema(Titulo = ModuleName)

    ListEsquema.append(Cabecera)
    ListEsquema.append(Modulo)

    EscribirPlymouth(Name + ".plymouth",ListEsquema)




#if __name__ == "__main":
#Esquema = ObtenerAtributos("Walking.plymouth")
#LeerEsquema
#EscribirPlymouth("salida.plymouth",Esquema)
#IPlymouth()
