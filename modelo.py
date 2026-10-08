from datetime import datetime
from abc import ABC, abstractmethod
 
class Empleado(ABC):
    def __init__(self, id_empleado, nombres, apellidos, dni, telefono):
        self.id_empleado = id_empleado
        self.nombres = nombres
        self.apellidos = apellidos
        self.dni = dni
        self.telefono = telefono

    @abstractmethod
    def obtener_datos(self):
        return f"{self.nombres} {self.apellidos} (DNI {self.dni})"
 
 
class Mesero(Empleado):                      
    def __init__(self, id_empleado, nombres, apellidos, dni, telefono, turno):
        super().__init__(id_empleado, nombres, apellidos, dni, telefono)
        self.turno = turno
        self.estado_activo = True
 
    def confirmar_pago(self, venta):
        venta.pago_confirmado = True
    
    def obtener_datos(self):
        return f"{self.nombres} {self.apellidos} (DNI {self.dni})"