def mostrar_menu():
    print("\n==== GESTOR DE USUARIOS ====")
    print("1. Registrar usuario")
    print("2. Mostrar usuario")
    print("3. Buscar usuario")
    print("4. Actualizar usuario")
    print("5. Eliminar usuario")
    print("6. Salir")

usuarios = []
opcion = ""

while opcion != "6":
    mostrar_menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Ingrese el nombre: ")
        correo = input("Ingrese el correo: ")
        edad = input("Ingrese la edad: ")
        usuario = {
            "nombre": nombre,
            "correo": correo,
            "edad": edad
        }
        usuarios.append(usuario)
        print("Usuario registrado")

    elif opcion == "2":
        if len(usuarios) == 0:
            print("No hay usuarios registrados")
        else:
            for usuario in usuarios:
                print("Nombre:", usuario["nombre"])
                print("Correo:", usuario["correo"])
                print("Edad:", usuario["edad"])
                print("--------------------")

    elif opcion == "3":
        usuario_buscado = input("Ingrese nombre:")
        encontrado = False
        for usuario in usuarios:
            if usuario["nombre"] == usuario_buscado:
                print("Nombre:", usuario["nombre"])
                print("Correo:", usuario["correo"])
                print("Edad:", usuario["edad"])
                print("--------------------")
                encontrado = True 
        if encontrado == False:
            print("Usuario no encontrado")

    elif opcion == "4":
        usuario_buscado = input("Ingrese nombre del usuario a actualizar:")
        encontrado = False
        for usuario in usuarios:
            if usuario["nombre"] == usuario_buscado:
                encontrado = True
                nuevo_nombre = input("Ingrese el nuevo nombre:")
                nuevo_correo = input("Ingrese el nuevo correo:")
                nueva_edad = input("Ingrese la nueva edad:")

                usuario["nombre"] = nuevo_nombre
                usuario["correo"] = nuevo_correo
                usuario["edad"] = nueva_edad
                print("Usuario actualizado")
        if encontrado == False:
            print("Usuario no encontrado")

    elif opcion == "5":
        usuario_buscado = input("Ingrese el nombre del usuario a eliminar:")
        encontrado = False
        for usuario in usuarios:
            if usuario["nombre"] == usuario_buscado:
                usuarios.remove(usuario)
                encontrado = True
                print("Usuario eliminado")
                break
        if encontrado == False:
            print("Usuario no encontrado")
    elif opcion == "6":
        print("Saliendo del sistema")
    else:
        print("Opción incorrecta")
