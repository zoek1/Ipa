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
import re
import pdb
import EsquemaT

# Colores de salida
_MORADO   = '\033[95m'
_AZUL     = '\033[94m'
_VERDE    = '\033[92m'
_AMARILLO = '\033[93m'
_ROJO     = '\033[91m'
_NINGUNO  = '\033[0m'

_COLOR = True

# Atributos del tema necesarios
Tema = {"Esquema"     : "Plymouth Theme",
        "Name"        : "",
        "Description" : "",
        "ModuleName"  : ""}


def ObtenerAtributos(NombreArchivo,_COLOR=False):
    """
    Obtener los Cadenas de un archivo con extension .plymouth
    y codificarlos.

    Arguments:
    - `NombreArchivo`: Nombre del Archivo a ser escrito.
    """
    # pdb.set_trace()
    ListaEsquemas = []
    title = re.compile("\[.*\]")
    element = re.compile(".*=.*")
    # El esquema por default es "Plymouth Theme"

    try:
        ArchivoPlymouth = open(NombreArchivo)
    except IOError:
        print("Error en apertura de Archivo: ", NombreArchivo)
    else:
        for Cadena in ArchivoPlymouth:

            if title.match(Cadena):

                Cadena = Cadena.strip("[")
                Cadena = Cadena.strip("\n")
                Cadena = Cadena.strip("]")
                print("Esquema encontrado", Cadena)

                EsquemaActual = EsquemaT.Esquema(Cadena)
                ListaEsquemas.append(EsquemaActual)

            if element.match(Cadena):
                Cadena = Cadena.split("=")
                Cadena[0] = Cadena[0].strip()
                Cadena[1] = Cadena[1].strip("\n")

                ListaEsquemas[-1].setElemento(Cadena[0],Cadena[1])

                if _COLOR:
                    print("\t|--->",_MORADO, "Asociacion", _AZUL,
                          Cadena[0],_NINGUNO, " - ", _VERDE,
                          Cadena[1], _NINGUNO)
                else:
                    print("\t|--->", "Asociacion", Cadena[0],
                          " - ", Cadena[1])

        ArchivoPlymouth.close()

        return ListaEsquemas

def _EscribirEsquema(Archivo,Esquema,Modo="a+"):
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

        Plymouth.write("\n")
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
        _EscribirEsquema(NombreArchivo, Esquemas, Modo)




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
        Titulo = input("Introduce el Nombre del plymouth")
    print("Nombre del esquema: " + Titulo)
    Esquema.setTitle(Titulo)

    return Esquema


def LeerEsquema(Titulo = None, Esquema = None):
    """Establece un metodo para introducir el identificador del esquema,
    y sus respectivos elementos como son los Cadena y su valor.

    Devolvera un objeto de tipo Esquema.
    """

    opcion   = "s"

    esquema = setTitulo(Titulo = Titulo, Esquema=Esquema)

    while opcion == "s" or opcion == "S":
        Cadena = None
        valor    = None

        while not Cadena:
            Cadena = input("Introduce el identificador Cadena: ")

        while not valor:
            valor = input("Introduce el valor del Cadena: ")

        # Establecer elemento del esquema
        esquema.setElemento(Cadena,valor)

        opcion = input("Desea ingresar otro campo para el esquema s/n")

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
        Name = input("Introduce el nombre del tema: ")

    while not Description:
        Description = input("Introduce una descripcion del tema: ")

    while not ModuleName:
        ModuleName = input("Introduce el nombre del modulo del plymouth: ")

    Cabecera.setElemento("Name", Name)
    Cabecera.setElemento("Description", Description)
    Cabecera.setElemento("ModuleName", ModuleName)

    if ModuleName == "script":
        while not ImageDir:
            ImageDir = input("Directorio de Imagenes para el plymouth: ")

        while not ScriptFile:
            ScriptFile = input("Direccion del archivo script del plymouth: ")

        Modulo.setTitle(ModuleName )
        Modulo.setElemento("ImageDir", ImageDir)
        Modulo.setElemento("ScriptFile", ScriptFile)
    else:
        Modulo = LeerEsquema(Titulo = ModuleName)

    ListEsquema.append(Cabecera)
    ListEsquema.append(Modulo)

    EscribirPlymouth(Name + ".plymouth",ListEsquema)




if __name__ == "__main__":
#Esquema = ObtenerAtributos("Walking.plymouth")
#LeerEsquema
#EscribirPlymouth("salida.plymouth",Esquema)
    IPlymouth()
