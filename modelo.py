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

class Producto:
    def __init__(self, id_producto, nombre, precio, stock, categoria):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
 
    def esta_disponible(self, cantidad):
        return self.stock >= cantidad
 
    def actualizar_stock(self, cantidad):
        if self.stock + cantidad < 0:
            return False
        self.stock += cantidad
        return True
 
 
class DetallePedido:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = producto.precio    
 
    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario
 
 
class Pedido:
    def __init__(self, id_pedido):
        self.id_pedido = id_pedido
        self.estado = "ABIERTO"
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.detalles = []                        
 
    def agregar_detalle(self, producto, cantidad):
        if not producto.esta_disponible(cantidad):
            raise ValueError(f"Stock insuficiente de {producto.nombre} (hay {producto.stock})")
        producto.actualizar_stock(-cantidad)      
        for d in self.detalles:
            if d.producto is producto:
                d.cantidad += cantidad
                return
        self.detalles.append(DetallePedido(producto, cantidad))
 
    def calcular_total(self):
        return sum(d.calcular_subtotal() for d in self.detalles)
 
class Mesa:
    def __init__(self, numero_mesa, capacidad):
        self.numero_mesa = numero_mesa
        self.capacidad = capacidad
        self.estado = "LIBRE"
        self.mesero = None
        self.pedido = None
 
    def asignar_mesero(self, mesero):
        self.mesero = mesero
 
    def asignar_pedido(self, pedido):
        self.pedido = pedido
        self.estado = "OCUPADA"
 
    def liberar_mesa(self):
        self.pedido = None
        self.mesero = None
        self.estado = "LIBRE"












































