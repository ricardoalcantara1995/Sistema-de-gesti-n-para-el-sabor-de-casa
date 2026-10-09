import tkinter as tk
from tkinter import ttk, messagebox
from controlador import Restaurante
 
gestor = Restaurante("Mi Restaurante", cantidad_mesas=10)

gestor.registrar_mesero("Ana", "Pérez", "12345678", "999111222", "Mañana")
gestor.registrar_producto("Ceviche", 28.0, 20, "Platos")
gestor.registrar_producto("Chicha morada", 8.0, 30, "Bebidas")
 
root = tk.Tk()
root.title(gestor.nombre_empresa)
root.geometry("820x560")
nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True, padx=8, pady=8)
 
 
def campo(parent, texto, fila):
    ttk.Label(parent, text=texto).grid(row=fila, column=0, sticky="w", pady=2)
    e = ttk.Entry(parent, width=24)
    e.grid(row=fila, column=1, padx=6, pady=2)
    return e
 
 
def tabla(parent, columnas, alto=8):
    t = ttk.Treeview(parent, columns=columnas, show="headings", height=alto)
    for c in columnas:
        t.heading(c, text=c)
        t.column(c, width=110)
    return t
 
 

f_mes = ttk.Frame(nb, padding=10)
nb.add(f_mes, text="Meseros")
e_nom, e_ape, e_dni, e_tel, e_turno = (campo(f_mes, t, i) for i, t in
    enumerate(["Nombres", "Apellidos", "DNI", "Teléfono", "Turno"]))
t_mes = tabla(f_mes, ("ID", "Nombre", "DNI", "Turno"))
t_mes.grid(row=7, column=0, columnspan=3, pady=10, sticky="nsew")
 
 
def refrescar_meseros():
    t_mes.delete(*t_mes.get_children())
    for m in gestor.listar_meseros():
        t_mes.insert("", "end", values=(m.id_empleado, m.nombres + " " + m.apellidos, m.dni, m.turno))
    cb_mesero["values"] = [f"{m.id_empleado} - {m.nombres}" for m in gestor.listar_meseros()]
 
 
def guardar_mesero():
    if not e_nom.get() or not e_dni.get():
        return messagebox.showwarning("Falta dato", "Nombres y DNI son obligatorios")
    gestor.registrar_mesero(e_nom.get(), e_ape.get(), e_dni.get(), e_tel.get(), e_turno.get())
    for e in (e_nom, e_ape, e_dni, e_tel, e_turno):
        e.delete(0, "end")
    refrescar_meseros()
 
 
ttk.Button(f_mes, text="Crear mesero", command=guardar_mesero).grid(row=5, column=1, pady=6, sticky="w")
 

f_pro = ttk.Frame(nb, padding=10)
nb.add(f_pro, text="Productos")
p_nom, p_pre, p_sto, p_cat = (campo(f_pro, t, i) for i, t in
    enumerate(["Nombre", "Precio", "Stock", "Categoría"]))
t_pro = tabla(f_pro, ("ID", "Nombre", "Precio", "Stock", "Categoría"))
t_pro.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew")
 
 
def refrescar_productos():
    t_pro.delete(*t_pro.get_children())
    for p in gestor.listar_productos():
        t_pro.insert("", "end", values=(p.id_producto, p.nombre, f"S/ {p.precio:.2f}", p.stock, p.categoria))
    cb_prod["values"] = [f"{p.id_producto} - {p.nombre}" for p in gestor.listar_productos()]
 
 
def guardar_producto():
    try:
        gestor.registrar_producto(p_nom.get(), float(p_pre.get()), int(p_sto.get()), p_cat.get())
    except ValueError:
        return messagebox.showwarning("Dato inválido", "Precio debe ser número y stock entero")
    for e in (p_nom, p_pre, p_sto, p_cat):
        e.delete(0, "end")
    refrescar_productos()
 
 
ttk.Button(f_pro, text="Crear producto", command=guardar_producto).grid(row=4, column=1, pady=6, sticky="w")
 

f_ped = ttk.Frame(nb, padding=10)
nb.add(f_ped, text="Mesas y pedido")
 
ttk.Label(f_ped, text="Mesa").grid(row=0, column=0, sticky="w")
cb_mesa = ttk.Combobox(f_ped, values=[m.numero_mesa for m in gestor.mesas], width=6, state="readonly")
cb_mesa.grid(row=0, column=1, sticky="w")
ttk.Label(f_ped, text="Mesero").grid(row=0, column=2, sticky="e")
cb_mesero = ttk.Combobox(f_ped, width=22, state="readonly")
cb_mesero.grid(row=0, column=3, sticky="w", padx=6)
lbl_estado = ttk.Label(f_ped, text="")
lbl_estado.grid(row=0, column=4, padx=10)
 
ttk.Label(f_ped, text="Producto").grid(row=1, column=0, sticky="w", pady=6)
cb_prod = ttk.Combobox(f_ped, width=24, state="readonly")
cb_prod.grid(row=1, column=1, columnspan=2, sticky="w")
ttk.Label(f_ped, text="Cant.").grid(row=1, column=3, sticky="e")
sp_cant = ttk.Spinbox(f_ped, from_=1, to=50, width=5)
sp_cant.set(1)
sp_cant.grid(row=1, column=4, sticky="w")
 
t_det = tabla(f_ped, ("Producto", "Cant.", "P. unit.", "Subtotal"), alto=9)
t_det.grid(row=2, column=0, columnspan=6, pady=8, sticky="nsew")
lbl_total = ttk.Label(f_ped, text="Total: S/ 0.00", font=("Arial", 13, "bold"))
lbl_total.grid(row=3, column=0, columnspan=3, sticky="w")
 
 
def mesa_sel():
    if not cb_mesa.get():
        messagebox.showinfo("Mesa", "Elige una mesa")
        return None
    return int(cb_mesa.get())
 
def refrescar_pedido(*_):
    t_det.delete(*t_det.get_children())
    n = cb_mesa.get()
    if not n:
        return
    mesa = gestor.buscar_mesa(int(n))
    lbl_estado.config(text=f"Estado: {mesa.estado}")
    pedido = gestor.consultar_consumo_mesa(int(n))
    if pedido:
        for d in pedido.detalles:
            t_det.insert("", "end", values=(d.producto.nombre, d.cantidad,
                         f"{d.precio_unitario:.2f}", f"{d.calcular_subtotal():.2f}"))
        lbl_total.config(text=f"Total: S/ {pedido.calcular_total():.2f}")
    else:
        lbl_total.config(text="Total: S/ 0.00")
 
 
def agregar():
    n = mesa_sel()
    if n is None or not cb_prod.get():
        return
    mesa = gestor.buscar_mesa(n)
    if mesa.pedido is None:                               # tomar pedido = abrir la cuenta de la mesa
        if not cb_mesero.get():
            return messagebox.showwarning("Mesero", "Elige el mesero que atiende")
        id_m = int(cb_mesero.get().split(" - ")[0])
        mesero = next(m for m in gestor.listar_meseros() if m.id_empleado == id_m)
        gestor.tomar_pedido(n, mesero)
    id_p = int(cb_prod.get().split(" - ")[0])
    prod = next(p for p in gestor.listar_productos() if p.id_producto == id_p)
    try:
        gestor.agregar_consumo(n, prod, int(sp_cant.get()))
    except ValueError as err:
        return messagebox.showerror("No se pudo agregar", str(err))
    refrescar_pedido()
    refrescar_productos()                                  # el stock bajó
 
 
ttk.Button(f_ped, text="Agregar al pedido", command=agregar).grid(row=1, column=5, padx=6)
cb_mesa.bind("<<ComboboxSelected>>", refrescar_pedido)
 
# --- pago ---
pago = ttk.LabelFrame(f_ped, text="Cobrar", padding=8)
pago.grid(row=4, column=0, columnspan=6, sticky="we", pady=8)
ttk.Label(pago, text="Método").grid(row=0, column=0)
cb_metodo = ttk.Combobox(pago, values=["EFECTIVO", "YAPE", "PLIN"], width=10, state="readonly")
cb_metodo.set("EFECTIVO")
cb_metodo.grid(row=0, column=1, padx=6)
ttk.Label(pago, text="Monto entregado").grid(row=0, column=2)
e_monto = ttk.Entry(pago, width=10)
e_monto.grid(row=0, column=3, padx=6)
var_conf = tk.BooleanVar()
ttk.Checkbutton(pago, text="Mesero confirma Yape/Plin", variable=var_conf).grid(row=0, column=4, padx=6)
 
 
def cobrar():
    n = mesa_sel()
    if n is None or gestor.consultar_consumo_mesa(n) is None:
        return messagebox.showwarning("Cobrar", "La mesa no tiene pedido")
    try:
        monto = float(e_monto.get() or 0)
    except ValueError:
        return messagebox.showwarning("Monto", "Monto inválido")
    venta, ok = gestor.registrar_venta(n, cb_metodo.get(), monto, var_conf.get())
    if not ok:
        return messagebox.showwarning("Pago no válido",
            "Monto insuficiente" if venta.metodo_pago == "EFECTIVO" else "Falta confirmar el pago digital")
    msg = f"Venta #{venta.id_venta} cobrada: S/ {venta.monto_total:.2f}"
    if venta.metodo_pago == "EFECTIVO":
        msg += f"\nVuelto: S/ {venta.vuelto:.2f}"
    messagebox.showinfo("Cobrado", msg)
    e_monto.delete(0, "end")
    var_conf.set(False)
    refrescar_pedido()
 
 
ttk.Button(pago, text="Cobrar", command=cobrar).grid(row=0, column=5, padx=10)
 

f_res = ttk.Frame(nb, padding=10)
nb.add(f_res, text="Consumo de mesas / Caja")
t_mesas = tabla(f_res, ("Mesa", "Estado", "Mesero", "Consumo"), alto=12)
t_mesas.pack(fill="x")
lbl_caja = ttk.Label(f_res, text="", justify="left")
lbl_caja.pack(anchor="w", pady=10)
 
 
def refrescar_resumen(*_):
    t_mesas.delete(*t_mesas.get_children())
    for m in gestor.mesas:
        total = m.pedido.calcular_total() if m.pedido else 0
        t_mesas.insert("", "end", values=(m.numero_mesa, m.estado,
                       m.mesero.nombres if m.mesero else "-", f"S/ {total:.2f}"))
    c = gestor.generar_cuadre_caja()
    top = gestor.obtener_plato_mas_vendido()
    lbl_caja.config(text=(f"Efectivo: S/ {c['EFECTIVO']:.2f}   Yape: S/ {c['YAPE']:.2f}   "
                          f"Plin: S/ {c['PLIN']:.2f}\nTOTAL: S/ {c['TOTAL']:.2f}\n"
                          f"Plato más vendido: {top.nombre if top else '-'}"))
 
 
nb.bind("<<NotebookTabChanged>>", refrescar_resumen)
refrescar_meseros()
refrescar_productos()
root.mainloop()
