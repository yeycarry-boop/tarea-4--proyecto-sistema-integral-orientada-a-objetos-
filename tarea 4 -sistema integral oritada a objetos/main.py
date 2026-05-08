"""
=============================================================================
 SOFTWARE FJ - Código 4: Programa Principal
=============================================================================
 Archivo     : main.py
 Descripción : Ejecuta el sistema Software FJ y simula operaciones de
               clientes, servicios, reservas y ventas.
=============================================================================
"""

import logging  # Manejo de logs

# Clases y excepciones del sistema
from sistema_fj import (
    SoftwareFJError,
    ValidacionDatoError,
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    Reserva
)

# Módulos de ventas
from registro_ventas import RegistroVentas
from consulta_ventas import ConsultaVentas


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """
    Ejecuta pruebas del sistema:
    - Registro de clientes
    - Registro de servicios
    - Procesamiento de reservas
    - Resumen de ventas
    """

    # Encabezado del sistema
    print("=" * 60)
    print("   SISTEMA SOFTWARE FJ - Gestión de Clientes y Reservas")
    print("=" * 60)

    # Registro de ventas y listas en memoria
    registro = RegistroVentas()
    clientes = []
    servicios = []


    # =========================================================================
    # SECCIÓN 1: CLIENTES
    # =========================================================================
    # Registros válidos e inválidos para probar validaciones.
    # =========================================================================
    print("\n>>> SECCIÓN 1: Registro de Clientes")
    print("-" * 60)

    # Cliente válido
    try:
        c1 = Cliente("C001", "Yeiron Mora", "yeiron@softwarefj.com")
        clientes.append(c1)
        print(f"  ✔ {c1}")
    except ValidacionDatoError as e:
        print(f"  ✘ Error al registrar cliente C001: {e}")

    # Cliente válido
    try:
        c2 = Cliente("C002", "Omar Sanchez", "omar.sanchez@softwarefj.com")
        clientes.append(c2)
        print(f"  ✔ {c2}")
    except ValidacionDatoError as e:
        print(f"  ✘ Error al registrar cliente C002: {e}")

    # Cliente válido
    try:
        c3 = Cliente("C003", "Stefany Plaza", "stefany.plaza@softwarefj.com")
        clientes.append(c3)
        print(f"  ✔ {c3}")
    except ValidacionDatoError as e:
        print(f"  ✘ Error al registrar cliente C003: {e}")

    # Cliente válido
    try:
        c4 = Cliente("C004", "Luis Serna", "luis.serna@softwarefj.com")
        clientes.append(c4)
        print(f"  ✔ {c4}")
    except ValidacionDatoError as e:
        print(f"  ✘ Error al registrar cliente C004: {e}")

    # Cliente inválido: nombre vacío
    try:
        c5 = Cliente("C005", "", "sinnom@email.com")
        clientes.append(c5)
        print(f"  ✔ {c5}")
    except ValidacionDatoError as e:
        print(f"  ✘ [ESPERADO] Error en cliente C005: {e}")

    # Cliente inválido: correo incorrecto
    try:
        c6 = Cliente("C006", "Cliente Invalido", "correo-invalido")
        clientes.append(c6)
        print(f"  ✔ {c6}")
    except ValidacionDatoError as e:
        print(f"  ✘ [ESPERADO] Error en cliente C006: {e}")


    # =========================================================================
    # SECCIÓN 2: SERVICIOS
    # =========================================================================
    # Registro de servicios válidos e inválidos.
    # =========================================================================
    print("\n>>> SECCIÓN 2: Registro de Servicios")
    print("-" * 60)

    # Servicio válido
    try:
        s1 = ReservaSala("S001", "Sala Ejecutiva A", 50.0)
        servicios.append(s1)
        print(f"  ✔ {s1}")
    except ValidacionDatoError as e:
        print(f"  ✘ Error al registrar servicio S001: {e}")

    # Servicio válido
    try:
        s2 = ReservaSala("S002", "Sala de Conferencias B", 75.0)
        servicios.append(s2)
        print(f"  ✔ {s2}")
    except ValidacionDatoError as e:
        print(f"  ✘ Error al registrar servicio S002: {e}")

    # Servicio válido
    try:
        s3 = AlquilerEquipo("S003", "Laptop Dell XPS", 35.0)
        servicios.append(s3)
        print(f"  ✔ {s3}")
    except ValidacionDatoError as e:
        print(f"  ✘ Error al registrar servicio S003: {e}")

    # Servicio inválido: costo negativo
    try:
        s4 = AlquilerEquipo("S004", "Equipo Defectuoso", -20.0)
        servicios.append(s4)
        print(f"  ✔ {s4}")
    except ValidacionDatoError as e:
        print(f"  ✘ [ESPERADO] Error en servicio S004: {e}")


    # =========================================================================
    # SECCIÓN 3: RESERVAS
    # =========================================================================
    # Reservas exitosas y fallidas con manejo de errores.
    # =========================================================================
    print("\n>>> SECCIÓN 3: Procesamiento de Reservas")
    print("-" * 60)

    # Reserva válida
    print("\n  [Reserva R001] Yeiron Mora | Sala Ejecutiva A")
    try:
        r1 = Reserva("R001", c1, s1, 2, limpieza=False)
        r1.procesar()
        registro.registrar(r1)
    except Exception as e:
        print(f"  ✘ Error en reserva R001: {e}")

    # Reserva válida
    print("\n  [Reserva R002] Omar Sanchez | Sala Conferencias")
    try:
        r2 = Reserva("R002", c2, s2, 3, limpieza=True)
        r2.procesar()
        registro.registrar(r2)
    except Exception as e:
        print(f"  ✘ Error en reserva R002: {e}")

    # Reserva válida
    print("\n  [Reserva R003] Stefany Plaza | Laptop Dell XPS")
    try:
        r3 = Reserva("R003", c3, s3, 4, seguro=True)
        r3.procesar()
        registro.registrar(r3)
    except Exception as e:
        print(f"  ✘ Error en reserva R003: {e}")

    # Reserva válida
    print("\n  [Reserva R004] Luis Serna | Sala Ejecutiva A")
    try:
        r4 = Reserva("R004", c4, s1, 5, limpieza=True)
        r4.procesar()
        registro.registrar(r4)
    except Exception as e:
        print(f"  ✘ Error en reserva R004: {e}")

    # Error: duración en cero
    print("\n  [Reserva R005] Duración inválida")
    try:
        r5 = Reserva("R005", c2, s1, 0)
        r5.procesar()
        registro.registrar(r5)
    except Exception as e:
        print(f"  ✘ [ESPERADO] Error en reserva R005: {type(e).__name__}: {e}")

    # Error: duración negativa
    print("\n  [Reserva R006] Duración negativa")
    try:
        r6 = Reserva("R006", c3, s3, -5, seguro=False)
        r6.procesar()
        registro.registrar(r6)
    except Exception as e:
        print(f"  ✘ [ESPERADO] Error en reserva R006: {type(e).__name__}: {e}")

    # Error: cliente inválido
    print("\n  [Reserva R007] Cliente inválido")
    try:
        r7 = Reserva("R007", "No soy un cliente", s2, 2)
        r7.procesar()
        registro.registrar(r7)
    except Exception as e:
        print(f"  ✘ [ESPERADO] Error en reserva R007: {type(e).__name__}: {e}")


    # =========================================================================
    # SECCIÓN 4: RESUMEN DE VENTAS
    # =========================================================================
    # Mostrar ventas confirmadas y total general.
    # =========================================================================
    ventas_confirmadas = registro.obtener_ventas()
    ConsultaVentas.mostrar_resumen(ventas_confirmadas)

    # Mensaje final
    print("\n  Sistema ejecutado correctamente.")
    print("  Revisa 'software_fj.log' para más detalles.\n")

    logging.info("Sistema Software FJ finalizado correctamente.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
# Ejecuta main() solo si este archivo se corre directamente.
if __name__ == "__main__":
    main()
