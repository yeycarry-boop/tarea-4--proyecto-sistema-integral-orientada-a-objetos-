"""
=============================================================================
 SOFTWARE FJ - Clases Base, Servicios y Reserva
=============================================================================
 
 Descripción : Contiene excepciones, clases base, servicios y la clase
               Reserva con manejo de excepciones.
=============================================================================
"""

import logging                       # Registro de eventos y errores
from abc import ABC, abstractmethod  # Clases y métodos abstractos


# =============================================================================
# CONFIGURACIÓN DE LOGS
# =============================================================================
# Configuración general del archivo de registros.
logging.basicConfig(
    filename='software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# =============================================================================
# EXCEPCIONES PERSONALIZADAS
# =============================================================================

class SoftwareFJError(Exception):
    """
    Excepción base del sistema.

    Permite capturar todos los errores personalizados
    usando un único bloque except.
    """
    pass

class ValidacionDatoError(SoftwareFJError):
    """
    Error lanzado cuando un dato no cumple las validaciones.
    """
    pass

# =============================================================================
# CLASE ABSTRACTA BASE: Entidad
# =============================================================================

class Entidad(ABC):
    """
    Clase abstracta base para las entidades del sistema.

    Define un ID único y una representación en texto.
    """

    def __init__(self, id_entidad: str):
        """
        Inicializa y valida el ID de la entidad.
        """
        # Validar que el ID sea texto y no esté vacío
        if not id_entidad or not isinstance(id_entidad, str):
            raise ValidacionDatoError(
                "El ID de la entidad no puede estar vacío."
            )

        self._id = id_entidad

    @property
    def id(self) -> str:
        """Retorna el ID de la entidad."""
        return self._id

    @abstractmethod
    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        pass

# =============================================================================
# CLASE CLIENTE
# =============================================================================

class Cliente(Entidad):
    """
    Representa un cliente registrado en el sistema.

    Usa encapsulación con atributos privados.
    """

    def __init__(self, id_cliente: str, nombre: str, correo: str):
        """
        Inicializa y valida los datos del cliente.
        """
        super().__init__(id_cliente)

        # Validar nombre y correo
        if not nombre or "@" not in str(correo):
            raise ValidacionDatoError(
                f"Datos inválidos. Nombre: '{nombre}' | Correo: '{correo}'."
            )

        # Atributos privados
        self.__nombre = nombre
        self.__correo = correo

    def get_nombre(self) -> str:
        """Retorna el nombre del cliente."""
        return self.__nombre

    def get_correo(self) -> str:
        """Retorna el correo del cliente."""
        return self.__correo

    def __str__(self) -> str:
        """Representación del cliente."""
        return f"Cliente: {self.__nombre} (ID: {self.id})"

# =============================================================================
# CLASE ABSTRACTA: Servicio
# =============================================================================

class Servicio(Entidad, ABC):
    """
    Clase abstracta base para los servicios del sistema.
    """

    def __init__(self, id_servicio: str, nombre: str, costo_base: float):
        """
        Inicializa el servicio y valida el costo base.
        """
        super().__init__(id_servicio)

        # Validar costo positivo
        if not isinstance(costo_base, (int, float)) or costo_base <= 0:
            raise ValidacionDatoError(
                f"Costo inválido '{costo_base}'."
            )

        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_total(self, cantidad: float, **kwargs) -> float:
        """
        Método abstracto para calcular el costo total.
        """
        pass

    def __str__(self) -> str:
        """Representación del servicio."""
        return f"Servicio: {self.nombre} | Tarifa: ${self.costo_base:.2f}"

# =============================================================================
# SERVICIO: RESERVA DE SALA
# =============================================================================

class ReservaSala(Servicio):
    """
    Servicio de reserva de salas por horas.
    """

    def calcular_total(self, horas: float, limpieza: bool = False) -> float:
        """
        Calcula el costo total de la reserva.
        """
        # Validar horas positivas
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValidacionDatoError(
                f"Horas inválidas '{horas}'."
            )

        # Agrega costo extra si incluye limpieza
        return (self.costo_base * horas) + (35 if limpieza else 0)

# =============================================================================
# SERVICIO: ALQUILER DE EQUIPO
# =============================================================================

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    """

    def calcular_total(self, dias: float, seguro: bool = True) -> float:
        """
        Calcula el costo total del alquiler.
        """
        # Validar días positivos
        if not isinstance(dias, (int, float)) or dias <= 0:
            raise ValidacionDatoError(
                f"Días inválidos '{dias}'."
            )

        # Aplicar recargo por seguro
        tasa = 1.12 if seguro else 1.0

        return (self.costo_base * dias) * tasa

# =============================================================================
# CLASE RESERVA
# =============================================================================

class Reserva:
    """
    Representa una reserva realizada por un cliente.
    """

    def __init__(self, id_reserva: str, cliente, servicio,
                 duracion: float, **kwargs):
        """
        Inicializa la reserva y sus datos asociados.
        """
        self.id_reserva = id_reserva
        self.id = id_reserva  # Compatibilidad con otros módulos
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.extras = kwargs
        self.estado = "CREADA"
        self.total = 0.0

    def procesar(self) -> float:
        """
        Procesa la reserva y calcula el total.
        """
        try:
            # Validar cliente
            if not isinstance(self.cliente, Cliente):
                raise ValidacionDatoError(
                    "Cliente inválido."
                )

            # Validar duración positiva
            if not isinstance(self.duracion, (int, float)) or self.duracion <= 0:
                raise ValueError(
                    f"Duración inválida '{self.duracion}'."
                )

            # Polimorfismo: cada servicio calcula su costo
            self.total = self.servicio.calcular_total(
                self.duracion,
                **self.extras
            )

            # Reserva exitosa
            self.estado = "CONFIRMADA"

            logging.info(
                f"Reserva '{self.id_reserva}' procesada correctamente."
            )

            print(
                f"  ✔ Reserva {self.id_reserva} procesada | "
                f"Cliente: {self.cliente.get_nombre()} | "
                f"Total: ${self.total:.2f}"
            )

            return self.total

        except (ValidacionDatoError, ValueError) as e:
            # Error controlado
            self.estado = "ERROR_CONTROLADO"

            logging.error(
                f"Error controlado en reserva '{self.id_reserva}': {e}"
            )

            raise

        except Exception as e:
            # Error inesperado
            self.estado = "ERROR_CRITICO"

            logging.critical(
                f"Error crítico en reserva '{self.id_reserva}': {e}"
            )

            raise
