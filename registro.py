import datetime
import os

class Gasto:
    def __init__(self, fecha, persona, cantidad, concepto, origen, lugar, pagado='no',fechaPagado=None):
        self.fecha = fecha
        self.persona = persona
        self.cantidad = cantidad
        self.concepto = concepto
        self.origen = origen
        self.lugar = lugar
        self.pagado = pagado
        self.fechaPagado = fechaPagado

class Dinero:
    def __init__(self, cantidad, concepto, tipo):
        self.cantidad = cantidad
        self.concepto = concepto
        self.tipo = tipo

dinero_disponible = []
gastos_registrados = []

def cargar_datos():
    if os.path.exists('dinero.txt'):
        with open('dinero.txt', 'r') as f:
            for linea in f.readlines():
                cantidad, concepto, tipo = linea.strip().split(",")
                dinero_disponible.append(Dinero(float(cantidad), concepto, tipo))
    
    if os.path.exists('gastos.txt'):
        with open('gastos.txt', 'r') as f:
            for linea in f.readlines():
                fecha, persona, cantidad, concepto, origen, lugar, pagado, fechaPagado = linea.strip().split(",")
                gastos_registrados.append(Gasto(fecha, persona, float(cantidad), concepto, origen, lugar, pagado, fechaPagado or None))

def guardar_datos():
    with open('dinero.txt', 'w') as f:
        for dinero in dinero_disponible:
            f.write(f"{dinero.cantidad},{dinero.concepto},{dinero.tipo}\n")
    
    with open('gastos.txt', 'w') as f:
        for gasto in gastos_registrados:
            f.write(f"{gasto.fecha},{gasto.persona},{gasto.cantidad},{gasto.concepto},{gasto.origen},{gasto.lugar},{gasto.pagado},{gasto.fechaPagado or ''}\n")

def menu():
    print("1. Registrar dinero disponible")
    print("2. Registrar un gasto")
    print("3. Registrar un pago")
    print("4. Ver dinero disponible")
    print("5. Ver gastos registrados")
    print("6. Ver total de deuda de una persona")
    print("7. Salir")

    while True:
        opcion = input("Selecciona una opción: ")
        if opcion in ['1', '2', '3', '4', '5', '6', '7']:
            return opcion
        else:
            print("Opción no válida, por favor ingresa un número del 1 al 7.")


def registrar_dinero():
    cantidad = float(input("Ingresa la cantidad de dinero: "))
    concepto = input("Ingresa el concepto del dinero: ")
    tipo = input("Ingresa el tipo de dinero ('1.-Efectivo', '2.-Banco', etc): ")
    try:
        tipoN = int(tipo)
        if tipoN == 1:
            tipo = "Efectivo"
        if tipoN == 2:
            tipo = "Banco"
    except:
        tipo =  tipo
    dinero = Dinero(cantidad, concepto, tipo)
    dinero_disponible.append(dinero)
    print("Dinero registrado exitosamente!\n")
    guardar_datos()

def registrar_gasto():

    # Verificar la cantidad
    cantidad = float(input("Ingresa la cantidad gastada: "))
    conceptoGasto = input("Ingresa el motivo del gasto: ")
    fecha = input("Ingresa la fecha del gasto (DD-MM-YYYY): ")
    
    # Lista de personas ya registradas
    personas = list(set([gasto.persona for gasto in gastos_registrados]))
    print("Personas ya registradas:")
    for i, persona in enumerate(personas, start=1):
        print(f"{i}. {persona}")
    print(f"{len(personas) + 1}. Registrar nueva persona")
    opcion_persona = input("Elige una opción: ")
    if opcion_persona.isdigit() and int(opcion_persona) <= len(personas):
        persona = personas[int(opcion_persona) - 1]
    else:
        persona = input("Ingresa la nueva persona relacionada: ")
    
    # Listar orígenes disponibles
    origenes = list(set([dinero.tipo for dinero in dinero_disponible]))
    print("Orígenes disponibles:")
    for i, origen in enumerate(origenes, start=1):
        print(f"{i}. {origen}")
    opcion_origen = input("Elige un origen: ")
    if opcion_origen.isdigit() and int(opcion_origen) <= len(origenes):
        origen = origenes[int(opcion_origen) - 1]
    else:
        print("Opción no válida, por favor ingresa un número de la lista.")
        return
    
    # Listar conceptos disponibles
    conceptos = list(set([dinero.concepto for dinero in dinero_disponible]))
    print("Conceptos disponibles:")
    for i, concepto in enumerate(conceptos, start=1):
        print(f"{i}. {concepto}")
    opcion_concepto = input("Elige un concepto: ")
    if opcion_concepto.isdigit() and int(opcion_concepto) <= len(conceptos):
        conceptoDisponible = conceptos[int(opcion_concepto) - 1]
    else:
        print("Opción no válida, por favor ingresa un número de la lista.")
        return
    
    
    # Verificar disponibilidad de fondos
    for dinero in dinero_disponible:
        if dinero.concepto == conceptoDisponible and dinero.tipo == origen:
            if dinero.cantidad < cantidad:
                print("Fondos insuficientes para registrar el gasto.")
                return
            else:
                dinero.cantidad -= cantidad  # Restar el gasto
    
    gasto = Gasto(fecha, persona, cantidad, conceptoGasto, conceptoDisponible, origen)
    gastos_registrados.append(gasto)
    print("Gasto registrado exitosamente!\n")
    guardar_datos()


def ver_dinero():
    print("\nDinero disponible:")
    
    # Ordenar la lista de dinero por el atributo tipo
    dinero_ordenado = sorted(dinero_disponible, key=lambda dinero: dinero.tipo)
    
    # Encabezado de la tabla
    print("{:<10} {:<15} {:<10}".format("Cantidad", "Concepto", "Tipo"))
    print("="*35)
    
    for dinero in dinero_ordenado:
        print("{:<10} {:<15} {:<10}".format(dinero.cantidad, dinero.concepto, dinero.tipo))
    
    print()


def ver_gastos():
    print("\nGastos registrados:")
    print("{:<15} {:<15} {:<10} {:<20} {:<15} {:<15}".format("Fecha", "Persona", "Cantidad", "Concepto", "Origen", "Fecha Pagado"))
    print("="*95)
    for gasto in gastos_registrados:
        print("{:<15} {:<15} {:<10} {:<20} {:<15} {:<15}".format(gasto.fecha, gasto.persona, gasto.cantidad, gasto.concepto, gasto.origen, gasto.fechaPagado or ''))
    print()


def registrar_pago():
    print("\nGastos no pagados:")
    
    # Filtrar los gastos que no están pagados
    gastos_no_pagados = [gasto for gasto in gastos_registrados if gasto.pagado == 'no']
    
    if not gastos_no_pagados:
        print("0 gastos no pagados.")
        return
    
    # Mostrar gastos no pagados
    for i, gasto in enumerate(gastos_no_pagados, start=1):
        print(f"{i}. {gasto.persona} - {gasto.concepto} - {gasto.cantidad} - {gasto.fecha}")
    
    opcion_gasto = int(input("Elige un gasto para pagar: "))
    
    if opcion_gasto > len(gastos_no_pagados):
        print("Opción no válida, por favor selecciona un gasto de la lista.")
        return
    
    # Obtener el gasto seleccionado
    gasto_seleccionado = gastos_no_pagados[opcion_gasto - 1]
    
    # Pedir la cantidad a pagar
    cantidad_pago = float(input("Ingresa la cantidad a pagar: "))
    
    if cantidad_pago > gasto_seleccionado.cantidad:
        print("La cantidad ingresada no puede ser mayor al gasto.")
        return
    
    # Actualizar el gasto y el dinero disponible
    gasto_seleccionado.cantidad -= cantidad_pago
    
    if gasto_seleccionado.cantidad == 0:
        gasto_seleccionado.pagado = 'si'
        fecha_pagado = input("Ingresa la fecha de pago (DD-MM-YYYY): ")  # Añadir fecha de pago
        gasto_seleccionado.fechaPagado = fecha_pagado
    
    for dinero in dinero_disponible:
        if dinero.concepto == gasto_seleccionado.origen and dinero.tipo == gasto_seleccionado.lugar:
            dinero.cantidad += cantidad_pago
    
    print("Pago registrado exitosamente!\n")
    guardar_datos()

def seleccionar_opcion(opciones, mensaje):
    for i, opcion in enumerate(opciones, start=1):
        print(f"{i}. {opcion}")
    print(f"{len(opciones) + 1}. Registrar nueva opción")
    
    while True:
        opcion = input(mensaje)
        if opcion.isdigit() and 1 <= int(opcion) <= len(opciones) + 1:
            return int(opcion)
        else:
            print("Opción no válida, por favor ingresa un número de la lista.")

def ver_total_por_persona():
    if not gastos_registrados:
        print("\nNo hay gastos registrados.\n")
        return

    # Obtener lista única de personas
    personas = list(set(gasto.persona for gasto in gastos_registrados))

    # Mostrar lista de personas
    print("\nSelecciona una persona:")
    for i, persona in enumerate(personas, 1):
        print(f"{i}. {persona}")
    
    try:
        seleccion = int(input("Ingresa el número de la persona: "))
        if seleccion < 1 or seleccion > len(personas):
            raise ValueError("Selección inválida.")
    except ValueError as e:
        print(f"\nError: {e}\n")
        return
    
    persona_seleccionada = personas[seleccion - 1]
    
    # Calcular el total de gastos de la persona seleccionada
    total = sum(gasto.cantidad for gasto in gastos_registrados if gasto.persona == persona_seleccionada)
    
    print(f"\nEl total de gastos de {persona_seleccionada} es: {total}\n")


if __name__ == "__main__":
    cargar_datos()
    while True:
        opcion = menu()
        if opcion == '1':
            registrar_dinero()
        elif opcion == '2':
            registrar_gasto()
        elif opcion == '3':
            registrar_pago()
        elif opcion == '4':
            ver_dinero()
        elif opcion == '5':
            ver_gastos()
        elif opcion == '6':
            ver_total_por_persona()
        elif opcion == '7':
            break
        else:
            print("Opción no válida, intenta de nuevo.")
