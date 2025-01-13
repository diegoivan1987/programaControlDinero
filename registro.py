import datetime
import os

class Gasto:
    def __init__(self, fecha, persona, cantidad, concepto, cuenta, lugar, pagado='no', fechaPagado=None):
        self.fecha = fecha
        self.persona = persona
        self.cantidad = cantidad
        self.concepto = concepto
        self.cuenta = cuenta  # Antes era 'origen'
        self.lugar = lugar
        self.pagado = pagado
        self.fechaPagado = fechaPagado

class Dinero:
    def __init__(self, cantidad, concepto, tipo):
        self.cantidad = cantidad
        self.concepto = concepto  # Nombre de la cuenta
        self.tipo = tipo          # Lugar: Efectivo, BBVA, Banamex, etc.

dinero_disponible = []
gastos_registrados = []
log_de_operaciones = []

def cargar_log():
    if os.path.exists('log.txt'):
        with open('log.txt', 'r') as f:
            for linea in f.readlines():
                datos = linea.strip().split(',')
                entrada = {
                    "Operacion": datos[0],
                    "Cantidad": float(datos[1]),
                    "Lugar": datos[2] or None,
                    "Cuenta": datos[3] or None,
                    "Concepto": datos[4],
                    "Fecha": datos[5]
                }
                log_de_operaciones.append(entrada)

def agregar_log(operacion, cantidad, lugar, cuenta, concepto, fecha):
    entrada = {
        "Operacion": operacion,
        "Cantidad": cantidad,
        "Lugar": lugar,
        "Cuenta": cuenta,
        "Concepto": concepto,
        "Fecha": fecha
    }
    log_de_operaciones.append(entrada)
    guardar_log()  # Guarda el log después de agregar una entrada

def guardar_log():
    with open('log.txt', 'w') as f:
        for entrada in log_de_operaciones:
            f.write(f"{entrada['Operacion']},{entrada['Cantidad']},{entrada['Lugar'] or ''},{entrada['Cuenta'] or ''},{entrada['Concepto']},{entrada['Fecha']}\n")

def mostrar_log():
    for entrada in log_de_operaciones:
        print("------")
        for clave, valor in entrada.items():
            print(f"{clave}: {valor}")

def cargar_datos():
    if os.path.exists('dinero.txt'):
        with open('dinero.txt', 'r') as f:
            for linea in f.readlines():
                cantidad, concepto, tipo = linea.strip().split(",")
                dinero_disponible.append(Dinero(float(cantidad), concepto, tipo))
    
    if os.path.exists('gastos.txt'):
        with open('gastos.txt', 'r') as f:
            for linea in f.readlines():
                fecha, persona, cantidad, concepto, cuenta, lugar, pagado, fechaPagado = linea.strip().split(",")
                gastos_registrados.append(
                    Gasto(fecha, persona, float(cantidad), concepto, cuenta, lugar, pagado, fechaPagado or None)
                )

def guardar_datos():
    with open('dinero.txt', 'w') as f:
        for dinero in dinero_disponible:
            f.write(f"{dinero.cantidad},{dinero.concepto},{dinero.tipo}\n")
    
    with open('gastos.txt', 'w') as f:
        for gasto in gastos_registrados:
            f.write(f"{gasto.fecha},{gasto.persona},{gasto.cantidad},{gasto.concepto},{gasto.cuenta},{gasto.lugar},{gasto.pagado},{gasto.fechaPagado or ''}\n")

def menu():
    print("1. Registrar dinero disponible")
    print("2. Registrar un gasto (una sola cuenta)")
    print("3. Registrar un pago")
    print("4. Ver dinero disponible")
    print("5. Ver gastos registrados")
    print("6. Ver total de deuda de una persona")
    print("7. Hacer un movimiento de dinero (entre cuentas)")
    print("8. Mostrar log")
    print("9. Salir")
    print("10. Registrar gasto grande en un lugar (best fit)")

    while True:
        opcion = input("Selecciona una opción: ")
        if opcion in ['1', '2', '3', '4', '5', '6', '7','8','9','10']:
            return opcion
        else:
            print("Opción no válida")

def registrar_dinero():
    cantidad = float(input("Ingresa la cantidad de dinero: "))
    concepto = input("Ingresa el concepto del dinero: ")
    
    print("Selecciona el tipo/lugar de dinero:")
    print("1. Efectivo")
    print("2. BBVA")
    print("3. Banamex")
    tipo_opcion = input("Elige una opción (1/2/3): ")
    if tipo_opcion == '1':
        tipo = "Efectivo"
    elif tipo_opcion == '2':
        tipo = "BBVA"
    elif tipo_opcion == '3':
        tipo = "Banamex"
    else:
        print("Opción inválida, se asigna por defecto 'Efectivo'.")
        tipo = "Efectivo"

    dinero = Dinero(cantidad, concepto, tipo)
    dinero_disponible.append(dinero)
    
    print("Dinero registrado exitosamente!\n")
    agregar_log("Registrar dinero", cantidad, None, None, concepto, datetime.datetime.now().strftime("%d-%m-%Y"))
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
    
    # Listar cuentas disponibles
    cuentas = list(set([dinero.tipo for dinero in dinero_disponible]))
    print("Cuentas (lugares) disponibles:")
    for i, cta in enumerate(cuentas, start=1):
        print(f"{i}. {cta}")
    opcion_cuenta = input("Elige una cuenta/lugar: ")
    if opcion_cuenta.isdigit() and int(opcion_cuenta) <= len(cuentas):
        cuenta = cuentas[int(opcion_cuenta) - 1]
    else:
        print("Opción no válida, por favor ingresa un número de la lista.")
        return
    
    # Listar conceptos disponibles relacionados a la cuenta elegida
    conceptos_relacionados = list(set([d.concepto for d in dinero_disponible if d.tipo == cuenta]))
    if not conceptos_relacionados:
        print("No hay conceptos disponibles para la cuenta/lugar elegido. Registra dinero antes de continuar.")
        return
    
    print("Conceptos disponibles:")
    for i, concepto in enumerate(conceptos_relacionados, start=1):
        saldo_concepto = next(d.cantidad for d in dinero_disponible if d.concepto == concepto and d.tipo == cuenta)
        print(f"{i}. {concepto} - {saldo_concepto} disponibles")
    
    opcion_concepto = input("Elige un concepto: ")
    if opcion_concepto.isdigit() and int(opcion_concepto) <= len(conceptos_relacionados):
        conceptoDisponible = conceptos_relacionados[int(opcion_concepto) - 1]
    else:
        print("Opción no válida, por favor ingresa un número de la lista.")
        return
    
    # Verificar disponibilidad de fondos
    for dinero in dinero_disponible:
        if dinero.concepto == conceptoDisponible and dinero.tipo == cuenta:
            if dinero.cantidad < cantidad:
                print("Fondos insuficientes para registrar el gasto.")
                return
            else:
                dinero.cantidad -= cantidad  # Restar el gasto
                break  # Ya aplicamos el descuento
    
    gasto = Gasto(fecha, persona, cantidad, conceptoGasto, conceptoDisponible,cuenta)
    gastos_registrados.append(gasto)
    print("Gasto registrado exitosamente!\n")
    agregar_log("Registrar gasto", cantidad, cuenta, None, conceptoGasto, fecha)
    guardar_datos()

def mover_dinero():
    # Listar cuentas (lugares) disponibles
    cuentas = list(set([dinero.tipo for dinero in dinero_disponible]))
    print("Cuentas disponibles:")
    for i, cta in enumerate(cuentas, start=1):
        print(f"{i}. {cta}")
    origen_inicial_opcion = input("Elige la cuenta inicial del dinero: ")
    
    if origen_inicial_opcion.isdigit() and int(origen_inicial_opcion) <= len(cuentas):
        cuenta_inicial = cuentas[int(origen_inicial_opcion) - 1]
    else:
        print("Opción no válida, por favor ingresa un número de la lista.")
        return
    
    # Listar conceptos disponibles para la cuenta inicial seleccionada
    conceptos_iniciales = list(set([dinero.concepto for dinero in dinero_disponible if dinero.tipo == cuenta_inicial]))
    print("Conceptos disponibles en la cuenta inicial:")
    for i, concepto in enumerate(conceptos_iniciales, start=1):
        print(f"{i}. {concepto}")
    concepto_opcion = input("Elige el concepto del dinero a mover: ")
    
    if concepto_opcion.isdigit() and int(concepto_opcion) <= len(conceptos_iniciales):
        concepto_seleccionado = conceptos_iniciales[int(concepto_opcion) - 1]
    else:
        print("Opción no válida, por favor ingresa un número de la lista.")
        return
    
    # Encuentra y muestra la cantidad disponible en el concepto seleccionado
    cantidad_disponible = next((d.cantidad for d in dinero_disponible 
                                if d.tipo == cuenta_inicial and d.concepto == concepto_seleccionado), 0)
    print(f"Cantidad disponible en {cuenta_inicial} - {concepto_seleccionado}: {cantidad_disponible}")
    
    # Elegir cuenta final
    print("Cuentas disponibles para mover el dinero:")
    for i, cta in enumerate(cuentas, start=1):
        print(f"{i}. {cta}")
    origen_final_opcion = input("Elige la cuenta final del dinero: ")
    
    if origen_final_opcion.isdigit() and int(origen_final_opcion) <= len(cuentas):
        cuenta_final = cuentas[int(origen_final_opcion) - 1]
    else:
        print("Opción no válida, por favor ingresa un número de la lista.")
        return
    
    # Pide al usuario ingresar el monto a mover
    cantidad_a_mover = float(input("Ingresa la cantidad de dinero a mover: "))
    
    # Validar fondos
    if cantidad_a_mover > cantidad_disponible or cantidad_a_mover <= 0:
        print("Cantidad no válida. Debe ser un valor positivo y menor o igual a la cantidad disponible.")
        return
    
    # Mover el dinero
    for dinero in dinero_disponible:
        if dinero.tipo == cuenta_inicial and dinero.concepto == concepto_seleccionado:
            dinero.cantidad -= cantidad_a_mover  # Resta la cantidad a mover del origen inicial
    
    # Si el concepto ya existe en la cuenta final, añadir el dinero a ese concepto
    for d in dinero_disponible:
        if d.tipo == cuenta_final and d.concepto == concepto_seleccionado:
            d.cantidad += cantidad_a_mover  # Suma la cantidad a mover a la cuenta final
            print("Dinero movido exitosamente!")
            agregar_log("Mover dinero", cantidad_a_mover, cuenta_final, cuenta_inicial, 
                        concepto_seleccionado, datetime.datetime.now().strftime("%d-%m-%Y"))
            guardar_datos()
            return
    
    # Si el concepto no existe en la cuenta final, crear un nuevo objeto Dinero
    nuevo_dinero = Dinero(cantidad_a_mover, concepto_seleccionado, cuenta_final)
    dinero_disponible.append(nuevo_dinero)
    print("Dinero movido y nuevo concepto creado exitosamente!")
    agregar_log("Mover dinero", cantidad_a_mover, cuenta_final, cuenta_inicial, 
                concepto_seleccionado, datetime.datetime.now().strftime("%d-%m-%Y"))
    guardar_datos()

def ver_dinero():
    print("\nDinero disponible:")
    
    # Ordenar la lista de dinero por el atributo tipo
    dinero_ordenado = sorted(dinero_disponible, key=lambda d: d.tipo)
    
    # Mostrar cabecera de la tabla
    print("{:<10} {:<15} {:<10}".format("Cantidad", "Concepto", "Tipo"))
    print("="*35)
    
    # Acumular totales por cada tipo
    totales_por_tipo = {}
    
    for d in dinero_ordenado:
        print("{:<10} {:<15} {:<10}".format(d.cantidad, d.concepto, d.tipo))
        if d.tipo not in totales_por_tipo:
            totales_por_tipo[d.tipo] = 0
        totales_por_tipo[d.tipo] += d.cantidad
    
    print()
    # Mostrar totales por cada tipo
    for tipo, total in totales_por_tipo.items():
        print(f"Total {tipo}: {total}")
    print()

def ver_gastos():
    print("\nGastos registrados:")
    print("{:<15} {:<15} {:<10} {:<20} {:<15} {:<15}".format("Fecha", "Persona", "Cantidad", "Concepto", "Cuenta", "Fecha Pagado"))
    print("="*95)
    for gasto in gastos_registrados:
        print("{:<15} {:<15} {:<10} {:<20} {:<15} {:<15}".format(
            gasto.fecha, gasto.persona, gasto.cantidad, 
            gasto.concepto, gasto.cuenta, gasto.fechaPagado or ''
        ))
    print()

def registrar_pago():
    print("\nGastos no pagados:")
    
    # Filtrar los gastos que no están pagados
    gastos_no_pagados = [gasto for gasto in gastos_registrados if gasto.pagado == 'no']
    
    if not gastos_no_pagados:
        print("0 gastos no pagados.")
        return
    
    # Convertir las fechas de string a objetos datetime y ordenar los gastos por fecha
    formato_fecha = "%d-%m-%Y"
    gastos_no_pagados.sort(key=lambda x: datetime.datetime.strptime(x.fecha, formato_fecha))
    
    # Mostrar gastos no pagados
    for i, gasto in enumerate(gastos_no_pagados, start=1):
        print(f"{i}. {gasto.persona} - {gasto.concepto} - {gasto.cantidad} - {gasto.fecha} - Lugar: {gasto.lugar} - Cuenta: {gasto.cuenta}")
    
    opcion_gasto = int(input("Elige un gasto para pagar: "))
    
    if opcion_gasto > len(gastos_no_pagados) or opcion_gasto <= 0:
        print("Opción no válida, por favor selecciona un gasto de la lista.")
        return
    
    # Obtener el gasto seleccionado
    gasto_seleccionado = gastos_no_pagados[opcion_gasto - 1]
    
    # Pedir la cantidad a pagar
    cantidad_pago = float(input("Ingresa la cantidad a pagar: "))
    
    if cantidad_pago > gasto_seleccionado.cantidad:
        print("La cantidad ingresada no puede ser mayor al gasto.")
        return
    
    tipo_pago = input("Elige el tipo de pago (externo/interno): ")
    
    if tipo_pago == 'interno':
        # Acumular las cantidades por lugar
        cuentas_disponibles = {}
        for d in dinero_disponible:
            if d.tipo not in cuentas_disponibles:
                cuentas_disponibles[d.tipo] = d.cantidad
            else:
                cuentas_disponibles[d.tipo] += d.cantidad
        
        # Mostrar cuentas disponibles y su cantidad
        print("Cuentas disponibles y su cantidad:")
        for i, (cuenta, ctd) in enumerate(cuentas_disponibles.items(), start=1):
            print(f"{i}. {cuenta} - Cantidad: {ctd}")
        
        opcion_cuenta = input("Elige una cuenta desde donde se hará el pago: ")
        if not opcion_cuenta.isdigit() or int(opcion_cuenta) > len(cuentas_disponibles) or int(opcion_cuenta) < 1:
            print("Opción no válida, por favor ingresa un número de la lista.")
            return
        cuenta_seleccionada = list(cuentas_disponibles.keys())[int(opcion_cuenta) - 1]
        
        # Listar conceptos disponibles para la cuenta seleccionada
        conceptos_disponibles = {d.concepto: d.cantidad 
                                 for d in dinero_disponible if d.tipo == cuenta_seleccionada}
        
        if not conceptos_disponibles:
            print(f"No hay conceptos en la cuenta {cuenta_seleccionada} con fondos disponibles.")
            return
        
        print("Conceptos disponibles y su cantidad:")
        lista_conceptos = list(conceptos_disponibles.items())  # (concepto, cantidad)
        for i, (conc, ctd) in enumerate(lista_conceptos, start=1):
            print(f"{i}. {conc} - Cantidad: {ctd}")
        
        opcion_concepto = input("Elige un concepto desde donde se hará el pago: ")
        if not opcion_concepto.isdigit() or int(opcion_concepto) > len(lista_conceptos) or int(opcion_concepto) < 1:
            print("Opción no válida, por favor ingresa un número de la lista.")
            return
        
        concepto_seleccionado = lista_conceptos[int(opcion_concepto) - 1][0]
        
        # Verificar disponibilidad de fondos
        for d in dinero_disponible:
            if d.concepto == concepto_seleccionado and d.tipo == cuenta_seleccionada:
                if d.cantidad < cantidad_pago:
                    print("Fondos insuficientes para realizar el pago.")
                    return
                else:
                    d.cantidad -= cantidad_pago  # Restar el pago
                    break
    
    # Actualizar el gasto
    gasto_seleccionado.cantidad -= cantidad_pago
    if gasto_seleccionado.cantidad == 0:
        gasto_seleccionado.pagado = 'si'
        fecha_pagado = input("Ingresa la fecha de pago (DD-MM-YYYY): ")
        gasto_seleccionado.fechaPagado = fecha_pagado
    
    # Sumar la cantidad pagada a la combinación (cuenta, lugar) del gasto
    combinacion_existente = False
    for d in dinero_disponible:
        if d.concepto == gasto_seleccionado.cuenta and d.tipo == gasto_seleccionado.lugar:
            d.cantidad += cantidad_pago
            combinacion_existente = True
            break
    
    if not combinacion_existente:
        # Crear nueva combinación usando la clase Dinero
        nuevo_dinero = Dinero(cantidad_pago, gasto_seleccionado.cuenta, gasto_seleccionado.lugar)
        dinero_disponible.append(nuevo_dinero)
    
    print("Pago registrado exitosamente!\n")
    agregar_log("Registrar pago", cantidad_pago, gasto_seleccionado.lugar, gasto_seleccionado.cuenta, 
                gasto_seleccionado.concepto, datetime.datetime.now().strftime("%d-%m-%Y"))
    guardar_datos()

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
    
    # Calcular el total de gastos no pagados
    total = 0
    print("\nGastos no pagados de", persona_seleccionada)
    for gasto in gastos_registrados:
        if gasto.persona == persona_seleccionada and gasto.pagado == 'no':
            print(f"{gasto.concepto} - {gasto.cantidad} - {gasto.fecha} - {gasto.lugar} - {gasto.cuenta}")
            total += gasto.cantidad
    
    if total == 0:
        print("No hay gastos no pagados para esta persona.\n")
    else:
        print(f"\nEl total de gastos no pagados de {persona_seleccionada} es: {total}\n")

# ------------------------------------------------------------------------
# NUEVA FUNCIÓN:
# "Registrar gasto grande" (Best Fit) que afecte múltiples cuentas de un MISMO lugar.
# ------------------------------------------------------------------------
def registrar_gasto_multicuenta():
    """
    Permite ingresar un gasto grande que se descuenta de varias cuentas
    (Dinero) pertenecientes a un mismo 'lugar' (tipo). Se usará un
    enfoque de 'best fit' para ir descontando.
    
    - Se crea un Gasto parcial por cada cuenta afectada, con el concepto
      y la fecha/persona que indique el usuario.
    - Si se terminan los fondos de ese lugar y aún queda importe por descontar,
      se mostrará al usuario cuánto quedo sin descontar.
    """
    print("== Registrar gasto grande (best fit) en varias cuentas de un mismo lugar ==")
    
    # 1. Pedir datos básicos
    fecha = input("Ingresa la fecha del gasto (DD-MM-YYYY): ")
    persona = input("Ingresa la persona asociada al gasto: ")
    concepto_gasto = input("Ingresa el motivo/concepto del gasto: ")
    try:
        monto_total = float(input("Ingresa el monto TOTAL del gasto: "))
    except ValueError:
        print("Valor inválido de monto.")
        return

    # 2. Seleccionar lugar (tipo)
    lugares_disponibles = list(set([d.tipo for d in dinero_disponible]))
    if not lugares_disponibles:
        print("No hay lugares registrados. Primero registra dinero en 'dinero_disponible'.")
        return
    
    print("Lugares disponibles:")
    for i, lugar in enumerate(lugares_disponibles, start=1):
        print(f"{i}. {lugar}")
    opcion_lugar = input("Elige un lugar: ")
    if not opcion_lugar.isdigit() or int(opcion_lugar) < 1 or int(opcion_lugar) > len(lugares_disponibles):
        print("Opción no válida")
        return
    
    lugar_seleccionado = lugares_disponibles[int(opcion_lugar) - 1]
    
    # 3. Filtrar las cuentas (Dinero) que correspondan a ese lugar
    cuentas_lugar = [d for d in dinero_disponible if d.tipo == lugar_seleccionado and d.cantidad > 0]
    
    if not cuentas_lugar:
        print(f"No hay fondos en el lugar '{lugar_seleccionado}'.")
        return
    
    # 4. Enfoque de "best fit" para ir descontando del monto_total
    #    Básicamente, en cada iteración:
    #      - Buscamos si alguna cuenta puede cubrir 'monto_restante' COMPLETAMENTE.
    #        Si sí, elegimos la que deje menor leftover (cantidad - monto_restante).
    #      - Si ninguna puede cubrirlo completamente, tomamos la cuenta con el MAYOR saldo
    #        y hacemos un descuento parcial.
    
    monto_restante = monto_total
    
    while monto_restante > 0 and any(d.cantidad > 0 for d in cuentas_lugar):
        # Filtrar cuentas con fondos y ordenarlas
        cuentas_disponibles = [d for d in cuentas_lugar if d.cantidad > 0]
        
        # 1) Revisar si alguna cubre el monto_restante
        cuentas_que_cubren = [d for d in cuentas_disponibles if d.cantidad >= monto_restante]
        
        if cuentas_que_cubren:
            # De las que pueden cubrir todo, elegimos la de leftover más pequeño
            # leftover = d.cantidad - monto_restante
            # Buscamos min leftover
            mejor_cuenta = min(cuentas_que_cubren, key=lambda x: (x.cantidad - monto_restante))
            
            # Descontamos
            mejor_cuenta.cantidad -= monto_restante
            monto_parcial = monto_restante
            monto_restante = 0
            
            # Registrar en gastos
            gasto_parcial = Gasto(
                fecha=fecha,
                persona=persona,
                cantidad=monto_parcial,
                concepto=concepto_gasto,
                cuenta=mejor_cuenta.concepto,
                lugar=lugar_seleccionado,
                pagado='no'
            )
            gastos_registrados.append(gasto_parcial)
            
            # Agregar log
            agregar_log("Registrar gasto multicuenta (best fit)",
                        monto_parcial,
                        lugar_seleccionado,
                        mejor_cuenta.concepto,
                        concepto_gasto,
                        fecha)
        else:
            # Nadie puede cubrir el monto_restante completo,
            # así que tomamos la cuenta con mayor cantidad
            cuenta_mayor = max(cuentas_disponibles, key=lambda x: x.cantidad)
            
            # Descontamos parcial
            descuento = cuenta_mayor.cantidad  # todo lo que tenga
            cuenta_mayor.cantidad = 0
            monto_restante -= descuento
            
            # Registrar en gastos
            gasto_parcial = Gasto(
                fecha=fecha,
                persona=persona,
                cantidad=descuento,
                concepto=concepto_gasto,
                cuenta=cuenta_mayor.concepto,
                lugar=cuenta_mayor.tipo,
                pagado='no'
            )
            gastos_registrados.append(gasto_parcial)
            
            # Agregar log
            agregar_log("Registrar gasto multicuenta (best fit)",
                        descuento,
                        lugar_seleccionado,
                        cuenta_mayor.concepto,
                        concepto_gasto,
                        fecha)
    
    # 5. Si quedó monto_restante > 0, no se cubrió el gasto totalmente
    if monto_restante > 0:
        print(f"No fue posible cubrir el total del gasto. Cantidad sin descontar: {monto_restante:.2f}")
    else:
        print("El gasto se ha cubierto completamente.")
    
    guardar_datos()

# ------------------------------------------------------------------------
# Integrar la nueva función en el flujo principal
# ------------------------------------------------------------------------

if __name__ == "__main__":
    cargar_datos()
    cargar_log()
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
            mover_dinero()
        elif opcion == '8':
            mostrar_log()
        elif opcion == '9':
            break
        elif opcion == '10':
            registrar_gasto_multicuenta()
        else:
            print("Opción no válida, intenta de nuevo.")