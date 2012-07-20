#!/usr/bin/env python


class Esquema:
    __head = None
    __body = {}

    def __init__(self, namescheme="None"):
        self.__head = namescheme
        self.__body = {}

    def getElemento(self, atributo):
        return self.__body[atributo]

    def getTitle(self):
        return self.__head

    def listAtributo(self):
        return self.__body.keys()

    def listElementos(self):
        return self.__body

    def setElemento(self, atributo, valor):
        self.__body[atributo] = valor

    def setTitle(self, namescheme):
        self.__head = namescheme

    def delElemento(self, namescheme):
        # if self.esquema.haskey(namescheme):
        del self.__body[namescheme]
