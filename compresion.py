
import os
import zipfile
import tarfile


class Comprimido():
    """Maneja la compresion y descompresion de archivos.
    Los formatos de compresion soportados son:
       - Zip
       - Tar
    """

    def __init__(self, Archivo, Modo = "r", Formato = None):
        """El parametro Archivo va a ser el objeto sobre el cual se
        realizaran las acciones.
        Si el archivo no existe se crea.

        Arguments:
        - `Archivo`: Nombre del archivo a ser manejado.
        - `Formato`: Si el archivo no existe, y si el valor de formato es un
                     elemento valido, se escribira con este formato.
        """

        self._Modo = self._Permisos(Modo)
        self._Formato = self._VerificarFormato(Archivo, Formato, self._Modo)
        self._Archivo = Archivo

        if self._Formato == "ZIP":
            self._Comprimido = zipfile.ZipFile(self._Archivo, self._Modo)
        else:
            self._Comprimido = tarfile.open(self._Archivo, self._Modo)


    def _Permisos(self, Modo):
        """Verificacion de permisos.

        Arguments:
        - `Modo`: Elemento que contiene el modo del fichero.
        """
        Modos = {"r","w","a"}
        for i in Modos:
            if i == Modo.lower():
                return i

        raise ValueError("Modo no soportado")


    def _Formato(self, Tipo):
        """Devuelve el tipo de formato del nombre del archivo.
        """
        Formatos = {"ZIP","TAR"}
        for i in Formatos:
            if i == Tipo.upper():
                return i

        raise FormatoNoSoportado("Formato Desconocido")


    def _obtener_formato(self, Archivo):
        """Devuelve el formato del archivo si es ZIP o TAR sino provoca una excepción,
        si el archio no existe retorna None.

        Arguments:
        - `Archivo`: Nombre del archivo del que se obtendra el formato.
        """
        Formato = None
        if os.path.exists(Archivo):
            print("Nombre del archivo ", Archivo)
            if zipfile.is_zipfile(Archivo):
                Formato = "ZIP"
            elif tarfile.is_tarfile(Archivo):
                Formato = "TAR"
            else:
                raise FormatoNoSoportado("Formato Desconocido")

        return Formato

    def Formato(self):
        return self._Formato

    def _VerificarFormato(self, Archivo, Formato, Modo="w"):
        """Devuelve el formato del archivo y como efecto secundario, establece 
        el valor de la variable local `Formato`.

        Arguments:
        - `Archivo`: Nombre del archivo del que se obtendra el formato.
        """
        if not Formato:
           Formato = self._obtener_formato(Archivo)

        if not Formato:
            Formato = "zip"

        Modo = self._Permisos(Modo)
        Formato = self._Formato(Formato)

        if os.path.exists(Archivo) and Modo != "w":
            FormatoC = self._obtener_formato(Archivo)
            if Formato.upper() != FormatoC and Modo != "w":
                raise ValueError("Formato del archivo difiere del especificado")
        else:
            if Modo == "r":
                raise ReadError("Archivo no ha sido encontrado")

        return Formato


    def ListaArchivos(self):
        """Devuelve la lista de los archivos que contiene el archivo comprimido
        """
        if self._Formato == "ZIP":
            return self._Comprimido.namelist()
        else:
            return self._Comprimido.getmembers()

    def ExtraerArchivo(self, Archivo):
        """Devuelve un objeto archivo extraido del objeto comprimido.

        Arguments:
        - `Archivo`:
        """
        return self._Comprimido.extract(Archivo)

    def agregar(self, Archivo):
        """Agregar un archivo al comprimido

        Arguments:
        - `self`:
        - `Archivo`:
        """
        if self._Formato == "ZIP":
            return self._Comprimido.write(Archivo)
        else:
            return self._Comprimido.add(Archivo, recursive = False)

    def cerrar(self):
        "Cerrar archivo"
        self._Modo = None
        self._Formato = None
        self._Archivo = None
        self._Comprimido.close()



class FormatoNoSoportado(Exception):
    """Clase que manejara las excepciones si el tipo de archivo no tiene soporte.
    """

    def __init__(self, value):
        """Obtiene el valor que produjo la excepcion.

        Arguments:
        - `Valor`: Contiene el valor que produjo la excepcion.
        """
        self.value = value

    def __str__(self):
        """Devuelve el valor que produjo la excepcion
        """
        return repr(self.value)
