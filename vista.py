import tkinter as tk
from tkinter import ttk, messagebox
from controlador import Restaurante
 
gestor = Restaurante("Mi Restaurante", cantidad_mesas=10)
# datos de prueba
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
 
 
# ================= PESTAÑA MESEROS =================
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
 
# ================= PESTAÑA PRODUCTOS =================
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
 
# ================= PESTAÑA MESAS / PEDIDO / PAGO =================
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
 
 
