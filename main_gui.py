"""
main_gui.py — Semana 6: Interfaz Gráfica con Flet + Manejo de Eventos
=======================================================================
Usa las clases existentes de la carpeta tienda:
  Producto, ProductoElectronico, Marca
Y el catalogo implementado en la Semana 5 (catalogo.py).

Para ejecutar:
    pip install flet
    python main_gui.py
"""

import flet as ft
from catalogo import Catalogo
from producto import Producto
from producto_electronico import ProductoElectronico
from marca import Marca


# Datos de demo al iniciar
def cargar_demo(catalogo):
    marca_samsung  = Marca("Samsung")
    marca_sony     = Marca("Sony")
    marca_generica = Marca("Generica")

    catalogo.agregar(ProductoElectronico("Televisor", 500.00, 5,  2, marca_samsung))
    catalogo.agregar(ProductoElectronico("Celular",   350.00, 12, 1, marca_sony))
    catalogo.agregar(Producto("Arroz",   2.50,  100))
    catalogo.agregar(Producto("Aceite",  3.75,   80))
    catalogo.agregar(ProductoElectronico("Audifonos", 45.00, 30, 1, marca_generica))


def main(page: ft.Page):
    page.title = "Tienda - Catalogo de Productos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width  = 950
    page.window.height = 680
    page.bgcolor = ft.colors.WHITE
    page.padding = 15

    catalogo = Catalogo()
    cargar_demo(catalogo)

    # ── Campos de entrada ──────────────────────────────────────────────────
    f_nombre   = ft.TextField(label="Nombre",   width=220, border_color=ft.colors.BLUE_400)
    f_precio   = ft.TextField(label="Precio",   width=130, border_color=ft.colors.BLUE_400,
                              keyboard_type=ft.KeyboardType.NUMBER)
    f_cantidad = ft.TextField(label="Cantidad", width=110, border_color=ft.colors.BLUE_400,
                              keyboard_type=ft.KeyboardType.NUMBER)
    f_marca    = ft.TextField(label="Marca",    width=150, border_color=ft.colors.BLUE_400)
    f_garantia = ft.TextField(label="Garantía (años)", width=150,
                              border_color=ft.colors.BLUE_400,
                              disabled=True,
                              keyboard_type=ft.KeyboardType.NUMBER)
    cb_electro = ft.Checkbox(label="Es electronico", value=False)
    f_buscar   = ft.TextField(label="Buscar por nombre", width=280,
                              border_color=ft.colors.BLUE_400)

    lbl_msg = ft.Text("", size=13, color=ft.colors.GREEN_700)

    def toggle_electro(e):
        f_garantia.disabled = not cb_electro.value
        f_garantia.update()

    cb_electro.on_change = toggle_electro

    # ── Tabla ──────────────────────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Marca")),
            ft.DataColumn(ft.Text("Precio"),   numeric=True),
            ft.DataColumn(ft.Text("Cantidad"), numeric=True),
            ft.DataColumn(ft.Text("Garantía")),
        ],
        rows=[],
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=4,
        horizontal_lines=ft.BorderSide(1, ft.colors.GREY_300),
        bgcolor=ft.colors.WHITE,
    )

    lbl_total = ft.Text("Total: 0 productos", size=12, color=ft.colors.GREY_700)

    # ── Helpers ────────────────────────────────────────────────────────────
    def msg(texto, color=ft.colors.GREEN_700):
        lbl_msg.value = texto
        lbl_msg.color = color
        lbl_msg.update()

    def refrescar(lista=None):
        productos = lista if lista is not None else catalogo.listar()
        tabla.rows.clear()
        for p in productos:
            es_e = isinstance(p, ProductoElectronico)
            garantia_txt = f"{p.get_garantia()} año(s)" if es_e else "-"
            marca_txt    = p.get_marca().get_nombre()     if es_e else "-"
            tabla.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p.get_nombre())),
                    ft.DataCell(ft.Text("Electronico" if es_e else "Normal")),
                    ft.DataCell(ft.Text(marca_txt)),
                    ft.DataCell(ft.Text(f"${p.get_precio():.2f}")),
                    ft.DataCell(ft.Text(str(p.get_cantidad()))),
                    ft.DataCell(ft.Text(garantia_txt)),
                ],
                on_select_changed=lambda e, prod=p: cargar_fila(prod),
            ))
        lbl_total.value = f"Total: {catalogo.total()} producto(s)"
        tabla.update()
        lbl_total.update()

    def limpiar():
        for c in [f_nombre, f_precio, f_cantidad, f_marca, f_garantia]:
            c.value = ""
            c.error_text = ""
        cb_electro.value = False
        f_garantia.disabled = True
        msg("")
        page.update()

    def cargar_fila(p):
        f_nombre.value   = p.get_nombre()
        f_precio.value   = str(p.get_precio())
        f_cantidad.value = str(p.get_cantidad())
        if isinstance(p, ProductoElectronico):
            cb_electro.value    = True
            f_garantia.disabled = False
            f_garantia.value    = str(p.get_garantia())
            f_marca.value       = p.get_marca().get_nombre()
        else:
            cb_electro.value    = False
            f_garantia.disabled = True
            f_garantia.value    = ""
            f_marca.value       = ""
        msg(f"Producto '{p.get_nombre()}' cargado.", ft.colors.BLUE_700)
        page.update()

    def validar():
        ok = True
        if not f_nombre.value.strip():
            f_nombre.error_text = "Obligatorio"; ok = False
        else:
            f_nombre.error_text = ""
        try:
            float(f_precio.value); f_precio.error_text = ""
        except:
            f_precio.error_text = "Numero invalido"; ok = False
        try:
            int(f_cantidad.value); f_cantidad.error_text = ""
        except:
            f_cantidad.error_text = "Numero invalido"; ok = False
        page.update()
        return ok

    # ── Eventos CRUD ───────────────────────────────────────────────────────
    def on_agregar(e):
        if not validar():
            msg("Error: revisa los campos.", ft.colors.RED_700); return
        nombre   = f_nombre.value.strip()
        precio   = float(f_precio.value)
        cantidad = int(f_cantidad.value)
        marca_n  = f_marca.value.strip() or "Generica"
        if cb_electro.value:
            garantia = int(f_garantia.value or "1")
            p = ProductoElectronico(nombre, precio, cantidad, garantia, Marca(marca_n))
        else:
            p = Producto(nombre, precio, cantidad)
        if catalogo.agregar(p):
            refrescar()
            msg(f"Producto '{nombre}' agregado correctamente.")
            limpiar()
        else:
            msg(f"Error: ya existe un producto llamado '{nombre}'.", ft.colors.RED_700)

    def on_buscar(e):
        termino = f_buscar.value.strip()
        if not termino:
            refrescar(); msg("Mostrando todos los productos.", ft.colors.BLUE_700); return
        resultados = catalogo.buscar_parcial(termino)
        refrescar(resultados)
        if resultados:
            msg(f"Se encontraron {len(resultados)} resultado(s).", ft.colors.BLUE_700)
        else:
            msg(f"No se encontro '{termino}'.", ft.colors.RED_700)

    def on_actualizar(e):
        nombre = f_nombre.value.strip()
        if not nombre:
            msg("Carga un producto primero (clic en la tabla).", ft.colors.ORANGE_700); return
        if not validar():
            msg("Error: revisa los campos.", ft.colors.RED_700); return
        try:
            precio   = float(f_precio.value)   if f_precio.value   else None
            cantidad = int(f_cantidad.value)    if f_cantidad.value else None
        except:
            msg("Precio o cantidad invalidos.", ft.colors.RED_700); return
        if catalogo.actualizar(nombre, nuevo_precio=precio, nueva_cantidad=cantidad):
            refrescar()
            msg(f"Producto '{nombre}' actualizado correctamente.")
            limpiar()
        else:
            msg(f"No se encontro '{nombre}'.", ft.colors.RED_700)

    def on_eliminar(e):
        nombre = f_nombre.value.strip()
        if not nombre:
            msg("Carga un producto primero (clic en la tabla).", ft.colors.ORANGE_700); return

        def confirmar(e):
            d.open = False; page.update()
            if catalogo.eliminar(nombre):
                refrescar()
                msg(f"Producto '{nombre}' eliminado.")
                limpiar()
            else:
                msg(f"No se encontro '{nombre}'.", ft.colors.RED_700)

        def cancelar(e):
            d.open = False; page.update()

        d = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminacion"),
            content=ft.Text(f"Deseas eliminar '{nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Eliminar", on_click=confirmar),
            ],
        )
        page.overlay.append(d)
        d.open = True
        page.update()

    def on_listar(e):
        f_buscar.value = ""
        refrescar()
        msg(f"Total: {catalogo.total()} producto(s) en el catalogo.", ft.colors.BLUE_700)

    def on_limpiar(e):
        f_buscar.value = ""
        limpiar(); refrescar()

    # ── Botones ────────────────────────────────────────────────────────────
    btn_agregar    = ft.ElevatedButton("Agregar",    on_click=on_agregar)
    btn_buscar_btn = ft.ElevatedButton("Buscar",     on_click=on_buscar)
    btn_actualizar = ft.ElevatedButton("Actualizar", on_click=on_actualizar)
    btn_eliminar   = ft.ElevatedButton("Eliminar",   on_click=on_eliminar)
    btn_listar     = ft.ElevatedButton("Listar todos", on_click=on_listar)
    btn_limpiar    = ft.OutlinedButton("Limpiar",    on_click=on_limpiar)

    # ── Layout ─────────────────────────────────────────────────────────────
    page.add(
        ft.Column([
            # Titulo
            ft.Text("Tienda - Catalogo de Productos",
                    size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Text("Semana 5 y 6 | Programacion Estructurada",
                    size=12, color=ft.colors.GREY_600),
            ft.Divider(),

            # Formulario
            ft.Text("Datos del producto:", weight=ft.FontWeight.BOLD),
            ft.Row([f_nombre, f_precio, f_cantidad, f_marca], wrap=True, spacing=8),
            ft.Row([cb_electro, f_garantia], spacing=12),

            # Botones CRUD
            ft.Row([
                btn_agregar, btn_buscar_btn, btn_actualizar,
                btn_eliminar, btn_listar, btn_limpiar,
            ], wrap=True, spacing=6),

            # Mensaje
            lbl_msg,
            ft.Divider(),

            # Buscador
            ft.Row([
                f_buscar,
                ft.Text("(haz clic en una fila para cargarla)", size=11,
                        color=ft.colors.GREY_500, italic=True),
            ]),
            lbl_total,

            # Tabla
            ft.Container(
                content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=4,
                padding=8,
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    )

    refrescar()


if __name__ == "__main__":
    ft.app(target=main)
