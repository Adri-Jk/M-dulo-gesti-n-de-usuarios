from abc import ABC, abstractmethod
import json
import os

# S: mostrar el menú es una responsabilidad específica
def mostrar_menu():
    print("\n==== GESTOR DE USUARIOS ====")
    print("1. Registrar usuario")
    print("2. Mostrar usuarios")
    print("3. Buscar usuario")
    print("4. Actualizar usuario")
    print("5. Eliminar usuario")
    print("6. Salir")

# I: interfaces separadas según las operaciones
class Consultable(ABC):
    @abstractmethod
    def mostrar(self):
        pass

    @abstractmethod
    def buscar(self, nombre):
        pass

class Modificable(ABC):
    @abstractmethod
    def registrar(self, usuario):
        pass

    @abstractmethod
    def actualizar(self, nombre, datos):
        pass

    @abstractmethod
    def eliminar(self, nombre):
        pass

class AlmacenamientoUsuarios(Consultable, Modificable):
    pass

# Primera implementación del almacenamiento
class AlmacenamientoLista(AlmacenamientoUsuarios):
    def __init__(self):
        self.usuarios = []

    def registrar(self, usuario):
        self.usuarios.append(usuario)

    def mostrar(self):
        return self.usuarios

    def buscar(self, nombre):
        for usuario in self.usuarios:
            if usuario["nombre"] == nombre:
                return usuario
        return None

    def actualizar(self, nombre, datos):
        usuario = self.buscar(nombre)
        if usuario is not None:
            usuario.update(datos)
            return True
        return False

    def eliminar(self, nombre):
        usuario = self.buscar(nombre)
        if usuario is not None:
            self.usuarios.remove(usuario)
            return True
        return False

# O: se agrega una nueva forma de guardar sin modificar el gestor
class AlmacenamientoArchivo(AlmacenamientoUsuarios):
    def __init__(self, archivo="usuarios.json"):
        self.archivo = archivo

    def cargar_usuarios(self):
        if not os.path.exists(self.archivo):
            return []
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def guardar_usuarios(self, usuarios):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

    def registrar(self, usuario):
        usuarios = self.cargar_usuarios()
        usuarios.append(usuario)
        self.guardar_usuarios(usuarios)

    def mostrar(self):
        return self.cargar_usuarios()

    def buscar(self, nombre):
        for usuario in self.cargar_usuarios():
            if usuario["nombre"] == nombre:
                return usuario
        return None

    def actualizar(self, nombre, datos):
        usuarios = self.cargar_usuarios()
        for usuario in usuarios:
            if usuario["nombre"] == nombre:
                usuario.update(datos)
                self.guardar_usuarios(usuarios)
                return True
        return False

    def eliminar(self, nombre):
        usuarios = self.cargar_usuarios()
        nuevos = [
            usuario for usuario in usuarios
            if usuario["nombre"] != nombre
        ]
        if len(nuevos) == len(usuarios):
            return False
        self.guardar_usuarios(nuevos)
        return True

# D: el gestor recibe el almacenamiento desde fuera
class GestorUsuarios:
    def __init__(self, almacenamiento):
        self.almacenamiento = almacenamiento

    def registrar(self, usuario):
        if self.buscar(usuario["nombre"]) is not None:
            return False
        self.almacenamiento.registrar(usuario)
        return True

    def mostrar(self):
        return self.almacenamiento.mostrar()

    def buscar(self, nombre):
        return self.almacenamiento.buscar(nombre)

    def actualizar(self, nombre, datos):
        return self.almacenamiento.actualizar(nombre, datos)

    def eliminar(self, nombre):
        return self.almacenamiento.eliminar(nombre)

# Funciones para interactuar con el usuario
def registrar_usuario(gestor):
    nombre = input("Ingrese el nombre: ")
    correo = input("Ingrese el correo: ")
    edad = input("Ingrese la edad: ")

    usuario = {
        "nombre": nombre,
        "correo": correo,
        "edad": edad
    }
    if gestor.registrar(usuario):
        print("Usuario registrado")
    else:
        print("Ya existe un usuario con ese nombre")

def mostrar_usuarios(gestor):
    usuarios = gestor.mostrar()
    if len(usuarios) == 0:
        print("No hay usuarios registrados")
    else:
        for usuario in usuarios:
            print("Nombre:", usuario["nombre"])
            print("Correo:", usuario["correo"])
            print("Edad:", usuario["edad"])
            print("--------------------")

def buscar_usuario(gestor):
    nombre = input("Ingrese nombre: ")
    usuario = gestor.buscar(nombre)
    if usuario is None:
        print("Usuario no encontrado")
    else:
        print("Nombre:", usuario["nombre"])
        print("Correo:", usuario["correo"])
        print("Edad:", usuario["edad"])
        print("--------------------")

def actualizar_usuario(gestor):
    nombre = input("Ingrese nombre del usuario a actualizar: ")
    if gestor.buscar(nombre) is None:
        print("Usuario no encontrado")
        return
    nuevo_nombre = input("Ingrese el nuevo nombre: ")
    nuevo_correo = input("Ingrese el nuevo correo: ")
    nueva_edad = input("Ingrese la nueva edad: ")

    datos = {
        "nombre": nuevo_nombre,
        "correo": nuevo_correo,
        "edad": nueva_edad
    }
    if gestor.actualizar(nombre, datos):
        print("Usuario actualizado")
    else:
        print("Usuario no encontrado")

def eliminar_usuario(gestor):
    nombre = input("Ingrese el nombre del usuario a eliminar: ")
    if gestor.eliminar(nombre):
        print("Usuario eliminado")
    else:
        print("Usuario no encontrado")
# L: se puede sustituir una implementación por otra
# almacenamiento = AlmacenamientoArchivo()
almacenamiento = AlmacenamientoLista()

gestor = GestorUsuarios(almacenamiento)

opcion = ""

while opcion != "6":
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        registrar_usuario(gestor)
    elif opcion == "2":
        mostrar_usuarios(gestor)
    elif opcion == "3":
        buscar_usuario(gestor)
    elif opcion == "4":
        actualizar_usuario(gestor)
    elif opcion == "5":
        eliminar_usuario(gestor)
    elif opcion == "6":
        print("Saliendo del sistema")
    else:
        print("Opción incorrecta")
