from modelo import Mesero, Mesa, Producto, Pedido, Venta

class Restaurante:
    def __init__(self, nombre_empresa, cantidad_mesas=10):
        self.nombre_empresa = nombre_empresa
        self.meseros = []
        self.productos = []
        self.ventas = []
        self.mesas = [Mesa(n, 4) for n in range(1, cantidad_mesas + 1)]
        self._sig_empleado = self._sig_producto = self._sig_pedido = self._sig_venta = 1
 
    def registrar_mesero(self, nombres, apellidos, dni, telefono, turno):
        m = Mesero(self._sig_empleado, nombres, apellidos, dni, telefono, turno)
        self._sig_empleado += 1
        self.meseros.append(m)
        return m
 
    def listar_meseros(self):
        return list(self.meseros)
 
    def registrar_producto(self, nombre, precio, stock, categoria):
        p = Producto(self._sig_producto, nombre, precio, stock, categoria)
        self._sig_producto += 1
        self.productos.append(p)
        return p
 
    def listar_productos(self):
        return list(self.productos)
 

    def buscar_mesa(self, numero_mesa):
        return next(m for m in self.mesas if m.numero_mesa == numero_mesa)
 
    def tomar_pedido(self, numero_mesa, mesero):
        mesa = self.buscar_mesa(numero_mesa)
        if mesa.pedido is None:
            mesa.asignar_mesero(mesero)
            mesa.asignar_pedido(Pedido(self._sig_pedido))
            self._sig_pedido += 1
        return mesa.pedido

    def agregar_consumo(self, numero_mesa, producto, cantidad):
        mesa = self.buscar_mesa(numero_mesa)
        if mesa.pedido is None:
            raise ValueError("La mesa no tiene pedido abierto")
        mesa.pedido.agregar_detalle(producto, cantidad)
 
    def consultar_consumo_mesa(self, numero_mesa):
        return self.buscar_mesa(numero_mesa).pedido
 
    def registrar_venta(self, numero_mesa, metodo_pago, monto_entregado=0.0, confirmado=False):
        mesa = self.buscar_mesa(numero_mesa)
        if mesa.pedido is None:
            raise ValueError("La mesa no tiene pedido")
        venta = Venta(self._sig_venta, mesa.pedido, metodo_pago)
        venta.monto_entregado = monto_entregado
        venta.pago_confirmado = confirmado and metodo_pago != "EFECTIVO"
        if not venta.procesar_pago():
            return venta, False
        self._sig_venta += 1
        mesa.pedido.estado = "PAGADO"
        self.ventas.append(venta)
        mesa.liberar_mesa()
        return venta, True
 
    def obtener_plato_mas_vendido(self):
        conteo = {}
        for v in self.ventas:
            for d in v.pedido.detalles:
                conteo[d.producto] = conteo.get(d.producto, 0) + d.cantidad
        return max(conteo, key=conteo.get) if conteo else None
 
    def generar_cuadre_caja(self):
        cuadre = {"EFECTIVO": 0.0, "YAPE": 0.0, "PLIN": 0.0}
        for v in self.ventas:
            cuadre[v.metodo_pago] += v.monto_total
        cuadre["TOTAL"] = sum(cuadre.values())
        return cuadre