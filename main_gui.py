"""
main_gui.py — Interfaz Gráfica Integral (Semanas 5, 6 y 7 + Persistencia)
==========================================================================
Proyecto: Sistema de Gestión de Tienda y Pedidos
Estudiante: Jonathan Andrés Cerezo Álava
Materia: Programación Estructurada

Integra:
  1. POO (Primer Parcial): Clases Producto, ProductoElectronico, Marca, Cliente y Polimorfismo.
  2. Colecciones (Semana 5): list, dict, set en Catalogo.
  3. Interfaz Gráfica (Semana 6): Flet con eventos, validaciones y diseño reactivo.
  4. TDA Lineal y Patrones (Semana 7): Cola FIFO manual y Patrón Repository.
  5. Persistencia de Datos (Examen): Guardado y carga automática en archivos JSON.

Para ejecutar:
    pip install flet==0.23.2
    python main_gui.py
"""

import flet as ft
from catalogo import Catalogo
from producto import Producto
from producto_electronico import ProductoElectronico
from marca import Marca
from cliente_mayorista import ClienteMayorista
from cliente_minorista import ClienteMinorista
from pedido import Pedido
from repository import PedidoRepository
from persistencia import GestorPersistencia


def main(page: ft.Page):
    page.title = "Tienda Virtual - Sistema Integral (Semanas 5, 6 y 7 + Persistencia)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1020
    page.window.height = 760
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.padding = 16

    # ──────────────────────────────────────────────────────────────────────────
    # INICIALIZACIÓN DE MODELOS Y PERSISTENCIA
    # ──────────────────────────────────────────────────────────────────────────
    catalogo = Catalogo()
    if not GestorPersistencia.cargar_catalogo(catalogo):
        GestorPersistencia.cargar_demo_inicial(catalogo)
        GestorPersistencia.guardar_catalogo(catalogo)

    repo_pedidos = PedidoRepository()
    if not GestorPersistencia.cargar_pedidos(repo_pedidos):
        # Demo inicial de pedidos en cola
        p1 = Pedido("Jonathan Cerezo (Mayorista)", "Televisor", 1, 425.00)
        p2 = Pedido("Maria Lopez (Minorista)", "Celular", 1, 332.50)
        p3 = Pedido("Carlos Ruiz (Normal)", "Arroz", 5, 12.50)
        repo_pedidos.agregar_pedido(p1)
        repo_pedidos.agregar_pedido(p2)
        repo_pedidos.agregar_pedido(p3)
        GestorPersistencia.guardar_pedidos(repo_pedidos)

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1: CATÁLOGO DE PRODUCTOS (SEMANAS 5 Y 6 + PERSISTENCIA)
    # ──────────────────────────────────────────────────────────────────────────
    f_nombre   = ft.TextField(label="Nombre del Producto", width=220, border_color=ft.colors.BLUE_400)
    f_precio   = ft.TextField(label="Precio ($)", width=130, border_color=ft.colors.BLUE_400,
                              keyboard_type=ft.KeyboardType.NUMBER)
    f_cantidad = ft.TextField(label="Stock / Cantidad", width=130, border_color=ft.colors.BLUE_400,
                              keyboard_type=ft.KeyboardType.NUMBER)
    f_marca    = ft.TextField(label="Marca", width=160, border_color=ft.colors.BLUE_400)
    f_garantia = ft.TextField(label="Garantía (años)", width=140, border_color=ft.colors.BLUE_400,
                              disabled=True, keyboard_type=ft.KeyboardType.NUMBER)
    cb_electro = ft.Checkbox(label="Es producto electrónico", value=False)
    f_buscar   = ft.TextField(label="Buscar producto por nombre", width=320, border_color=ft.colors.BLUE_400)

    lbl_msg_cat = ft.Text("💾 Persistencia activa: datos sincronizados con 'productos.json'",
                          size=12, color=ft.colors.GREEN_800, italic=True)
    lbl_total_cat = ft.Text(f"Total: {catalogo.total()} productos en catálogo", size=13, weight=ft.FontWeight.W_500)

    def toggle_electro(e):
        f_garantia.disabled = not cb_electro.value
        f_garantia.update()

    cb_electro.on_change = toggle_electro

    tabla_cat = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Marca", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Garantía", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, ft.colors.BLUE_GREY_200),
        border_radius=8,
        horizontal_lines=ft.BorderSide(1, ft.colors.BLUE_GREY_100),
        bgcolor=ft.colors.WHITE,
    )

    def msg_cat(texto, color=ft.colors.GREEN_800):
        lbl_msg_cat.value = texto
        lbl_msg_cat.color = color
        lbl_msg_cat.update()

    def refrescar_catalogo(lista=None):
        prods = lista if lista is not None else catalogo.listar()
        tabla_cat.rows.clear()
        for p in prods:
            es_e = isinstance(p, ProductoElectronico)
            garantia_txt = f"{p.get_garantia()} año(s)" if es_e else "N/A"
            marca_txt    = p.get_marca().get_nombre() if es_e else "General"
            tabla_cat.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p.get_nombre())),
                    ft.DataCell(ft.Text("Electrónico" if es_e else "Estándar")),
                    ft.DataCell(ft.Text(marca_txt)),
                    ft.DataCell(ft.Text(f"${p.get_precio():.2f}")),
                    ft.DataCell(ft.Text(str(p.get_cantidad()))),
                    ft.DataCell(ft.Text(garantia_txt)),
                ],
                on_select_changed=lambda e, prod=p: cargar_fila_cat(prod),
            ))
        lbl_total_cat.value = f"Total: {catalogo.total()} productos en catálogo (almacenados en JSON)"
        tabla_cat.update()
        lbl_total_cat.update()
        actualizar_dropdown_productos()

    def limpiar_form_cat():
        for c in [f_nombre, f_precio, f_cantidad, f_marca, f_garantia]:
            c.value = ""
            c.error_text = ""
        cb_electro.value = False
        f_garantia.disabled = True
        page.update()

    def cargar_fila_cat(p):
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
        msg_cat(f"Producto '{p.get_nombre()}' seleccionado.", ft.colors.BLUE_700)
        page.update()

    def validar_cat():
        ok = True
        if not f_nombre.value.strip():
            f_nombre.error_text = "Requerido"; ok = False
        else:
            f_nombre.error_text = ""
        try:
            precio = float(f_precio.value)
            if precio < 0:
                f_precio.error_text = "Debe ser >= 0"; ok = False
            else:
                f_precio.error_text = ""
        except:
            f_precio.error_text = "Número inválido"; ok = False
        try:
            cant = int(f_cantidad.value)
            if cant < 0:
                f_cantidad.error_text = "Debe ser >= 0"; ok = False
            else:
                f_cantidad.error_text = ""
        except:
            f_cantidad.error_text = "Número inválido"; ok = False
        page.update()
        return ok

    def on_agregar_cat(e):
        if not validar_cat():
            msg_cat("Corrige los campos marcados en rojo.", ft.colors.RED_700)
            return
        nombre   = f_nombre.value.strip()
        precio   = float(f_precio.value)
        cantidad = int(f_cantidad.value)
        marca_n  = f_marca.value.strip() or "Genérica"
        if cb_electro.value:
            garantia = int(f_garantia.value or "1")
            p = ProductoElectronico(nombre, precio, cantidad, garantia, Marca(marca_n))
        else:
            p = Producto(nombre, precio, cantidad)

        if catalogo.agregar(p):
            GestorPersistencia.guardar_catalogo(catalogo)
            refrescar_catalogo()
            msg_cat(f"✅ '{nombre}' agregado y persistido en 'productos.json'.")
            limpiar_form_cat()
        else:
            msg_cat(f"⚠️ Ya existe un producto con el nombre '{nombre}' (el SET evitó duplicado).", ft.colors.RED_700)

    def on_buscar_cat(e):
        termino = f_buscar.value.strip()
        if not termino:
            refrescar_catalogo()
            msg_cat("Mostrando todos los productos del catálogo.", ft.colors.BLUE_700)
            return
        resultados = catalogo.buscar_parcial(termino)
        refrescar_catalogo(resultados)
        if resultados:
            msg_cat(f"🔍 Se encontraron {len(resultados)} resultado(s) para '{termino}'.", ft.colors.BLUE_700)
        else:
            msg_cat(f"❌ No se encontró ningún producto con '{termino}'.", ft.colors.RED_700)

    def on_actualizar_cat(e):
        nombre = f_nombre.value.strip()
        if not nombre:
            msg_cat("Selecciona primero un producto de la tabla.", ft.colors.ORANGE_800)
            return
        if not validar_cat():
            msg_cat("Valores numéricos no válidos.", ft.colors.RED_700)
            return
        precio   = float(f_precio.value)
        cantidad = int(f_cantidad.value)
        if catalogo.actualizar(nombre, nuevo_precio=precio, nueva_cantidad=cantidad):
            GestorPersistencia.guardar_catalogo(catalogo)
            refrescar_catalogo()
            msg_cat(f"✅ '{nombre}' actualizado y guardado en 'productos.json'.")
            limpiar_form_cat()
        else:
            msg_cat(f"No se pudo actualizar '{nombre}'.", ft.colors.RED_700)

    def on_eliminar_cat(e):
        nombre = f_nombre.value.strip()
        if not nombre:
            msg_cat("Selecciona primero un producto de la tabla.", ft.colors.ORANGE_800)
            return

        def confirmar(ev):
            dlg_confirm.open = False
            page.update()
            if catalogo.eliminar(nombre):
                GestorPersistencia.guardar_catalogo(catalogo)
                refrescar_catalogo()
                msg_cat(f"🗑️ '{nombre}' eliminado de las 3 colecciones y de 'productos.json'.")
                limpiar_form_cat()
            else:
                msg_cat(f"No se encontró '{nombre}'.", ft.colors.RED_700)

        def cancelar(ev):
            dlg_confirm.open = False
            page.update()

        dlg_confirm = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar '{nombre}' del catálogo y del archivo persistente?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Eliminar", on_click=confirmar, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE),
            ],
        )
        page.overlay.append(dlg_confirm)
        dlg_confirm.open = True
        page.update()

    def on_listar_todos_cat(e):
        f_buscar.value = ""
        refrescar_catalogo()
        msg_cat(f"Catálogo completo cargado: {catalogo.total()} productos.", ft.colors.BLUE_700)

    btn_agregar_cat    = ft.ElevatedButton("Agregar Producto", icon=ft.icons.ADD_BOX,
                                           on_click=on_agregar_cat, bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
    btn_buscar_cat     = ft.ElevatedButton("Buscar", icon=ft.icons.SEARCH, on_click=on_buscar_cat)
    btn_actualizar_cat = ft.ElevatedButton("Actualizar", icon=ft.icons.EDIT, on_click=on_actualizar_cat)
    btn_eliminar_cat   = ft.ElevatedButton("Eliminar", icon=ft.icons.DELETE, on_click=on_eliminar_cat,
                                           bgcolor=ft.colors.RED_50, color=ft.colors.RED_700)
    btn_listar_cat     = ft.OutlinedButton("Listar Todos", icon=ft.icons.LIST, on_click=on_listar_todos_cat)
    btn_limpiar_cat    = ft.OutlinedButton("Limpiar", icon=ft.icons.CLEAR, on_click=lambda e: limpiar_form_cat())

    vista_catalogo = ft.Container(
        padding=10,
        content=ft.Column([
            ft.Text("Gestión del Catálogo de Productos (Semanas 5 y 6)", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Text("Utiliza colecciones en memoria (list, dict, set) y almacena persistentemente en productos.json.", size=12, color=ft.colors.GREY_700),
            ft.Container(
                bgcolor=ft.colors.WHITE,
                padding=14,
                border_radius=8,
                border=ft.border.all(1, ft.colors.BLUE_GREY_100),
                content=ft.Column([
                    ft.Row([f_nombre, f_precio, f_cantidad, f_marca], wrap=True, spacing=10),
                    ft.Row([cb_electro, f_garantia], spacing=15),
                    ft.Row([btn_agregar_cat, btn_actualizar_cat, btn_eliminar_cat, btn_limpiar_cat], wrap=True, spacing=8),
                ], spacing=10),
            ),
            lbl_msg_cat,
            ft.Row([
                f_buscar,
                btn_buscar_cat,
                btn_listar_cat,
                ft.Text("(Clic en fila para editar)", size=11, color=ft.colors.GREY_500, italic=True),
            ], wrap=True, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            lbl_total_cat,
            ft.Container(
                content=ft.Column([tabla_cat], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200),
                border_radius=8,
                padding=10,
                height=250,
            ),
        ], spacing=8, scroll=ft.ScrollMode.AUTO)
    )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2: COLA DE PEDIDOS FIFO (SEMANA 7 + REPOSITORY + PERSISTENCIA)
    # ──────────────────────────────────────────────────────────────────────────
    f_ped_cliente  = ft.TextField(label="Nombre del Cliente", width=220, border_color=ft.colors.BLUE_400)
    dd_ped_tipo    = ft.Dropdown(
        label="Tipo de Cliente (Polimorfismo)",
        width=250,
        border_color=ft.colors.BLUE_400,
        value="Normal",
        options=[
            ft.dropdown.Option("Normal", "Normal (Sin descuento)"),
            ft.dropdown.Option("Mayorista", "Mayorista (15% de descuento)"),
            ft.dropdown.Option("Minorista", "Minorista (5% de descuento)"),
        ]
    )
    dd_ped_prod    = ft.Dropdown(label="Seleccionar Producto", width=220, border_color=ft.colors.BLUE_400)
    f_ped_cant     = ft.TextField(label="Cantidad", width=110, value="1", border_color=ft.colors.BLUE_400,
                                  keyboard_type=ft.KeyboardType.NUMBER)

    lbl_ped_resumen = ft.Text("Resumen de Cola: 0 pendientes | 0 procesados", size=13, weight=ft.FontWeight.W_500)
    lbl_ped_msg     = ft.Text("💾 Persistencia activa: pedidos sincronizados con 'pedidos.json'",
                              size=12, color=ft.colors.GREEN_800, italic=True)

    def msg_ped(texto, color=ft.colors.GREEN_800):
        lbl_ped_msg.value = texto
        lbl_ped_msg.color = color
        lbl_ped_msg.update()

    def actualizar_dropdown_productos():
        items = [ft.dropdown.Option(p.get_nombre(), f"{p.get_nombre()} (${p.get_precio():.2f})")
                 for p in catalogo.listar()]
        dd_ped_prod.options = items
        if items and (not dd_ped_prod.value or dd_ped_prod.value not in [p.get_nombre() for p in catalogo.listar()]):
            dd_ped_prod.value = items[0].key
        dd_ped_prod.update()

    fila_visual_cola = ft.Row(wrap=True, spacing=8)

    tabla_procesados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Fecha/Hora", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cant.", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Total Cobrado", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, ft.colors.BLUE_GREY_200),
        border_radius=8,
        horizontal_lines=ft.BorderSide(1, ft.colors.BLUE_GREY_100),
        bgcolor=ft.colors.WHITE,
    )

    def refrescar_pedidos():
        # Actualizar visualizador de la cola FIFO
        pendientes = repo_pedidos.listar_pendientes()
        fila_visual_cola.controls.clear()

        if not pendientes:
            fila_visual_cola.controls.append(
                ft.Container(
                    content=ft.Text("📭 La cola de atención está vacía. No hay pedidos pendientes.",
                                    color=ft.colors.GREY_600, italic=True),
                    padding=10,
                )
            )
        else:
            fila_visual_cola.controls.append(
                ft.Container(
                    content=ft.Text("⚡ FRENTE", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    bgcolor=ft.colors.BLUE_700,
                    padding=8,
                    border_radius=4,
                )
            )
            for idx, p in enumerate(pendientes):
                es_primero = (idx == 0)
                card_color = ft.colors.LIGHT_BLUE_50 if not es_primero else ft.colors.AMBER_50
                border_color = ft.colors.BLUE_400 if not es_primero else ft.colors.AMBER_700
                fila_visual_cola.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"Pedido #{p.id}", weight=ft.FontWeight.BOLD, size=12,
                                    color=ft.colors.AMBER_900 if es_primero else ft.colors.BLUE_900),
                            ft.Text(f"{p.cliente}", size=11),
                            ft.Text(f"{p.producto} x{p.cantidad}", size=10, color=ft.colors.GREY_700),
                            ft.Text(f"${p.total:.2f}", weight=ft.FontWeight.BOLD, size=11, color=ft.colors.GREEN_800),
                        ], spacing=2),
                        bgcolor=card_color,
                        border=ft.border.all(1.5 if es_primero else 1, border_color),
                        border_radius=6,
                        padding=6,
                    )
                )
                if idx < len(pendientes) - 1:
                    fila_visual_cola.controls.append(
                        ft.Icon(ft.icons.ARROW_FORWARD, size=16, color=ft.colors.BLUE_GREY_400)
                    )

            fila_visual_cola.controls.append(
                ft.Container(
                    content=ft.Text("FINAL", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    bgcolor=ft.colors.BLUE_GREY_600,
                    padding=8,
                    border_radius=4,
                )
            )

        # Actualizar tabla de procesados
        tabla_procesados.rows.clear()
        for p in reversed(repo_pedidos.listar_procesados()):
            tabla_procesados.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"#{p.id}")),
                    ft.DataCell(ft.Text(p.fecha)),
                    ft.DataCell(ft.Text(p.cliente)),
                    ft.DataCell(ft.Text(p.producto)),
                    ft.DataCell(ft.Text(str(p.cantidad))),
                    ft.DataCell(ft.Text(f"${p.total:.2f}")),
                    ft.DataCell(ft.Container(
                        content=ft.Text("Procesado", color=ft.colors.GREEN_800, weight=ft.FontWeight.BOLD, size=11),
                        bgcolor=ft.colors.GREEN_50,
                        padding=4,
                        border_radius=4,
                    )),
                ]
            ))

        sig = repo_pedidos.ver_siguiente() if repo_pedidos.hay_pendientes() else None
        sig_txt = f"Pedido #{sig.id} ({sig.cliente})" if sig else "Ninguno"
        lbl_ped_resumen.value = (
            f"Cola FIFO: {repo_pedidos.total_pendientes()} en espera | "
            f"Próximo a atender: {sig_txt} | "
            f"Total atendidos: {repo_pedidos.total_procesados()}"
        )
        fila_visual_cola.update()
        tabla_procesados.update()
        lbl_ped_resumen.update()

    def on_encolar_pedido(e):
        cliente_nom = f_ped_cliente.value.strip()
        if not cliente_nom:
            msg_ped("Ingresa el nombre del cliente.", ft.colors.RED_700)
            return
        prod_nom = dd_ped_prod.value
        if not prod_nom:
            msg_ped("Selecciona un producto del catálogo.", ft.colors.RED_700)
            return

        prod_obj = catalogo.buscar(prod_nom)
        if not prod_obj:
            msg_ped("Producto no encontrado en catálogo.", ft.colors.RED_700)
            return

        try:
            cant = int(f_ped_cant.value)
            if cant <= 0:
                msg_ped("La cantidad debe ser mayor a 0.", ft.colors.RED_700)
                return
        except:
            msg_ped("Cantidad inválida.", ft.colors.RED_700)
            return

        precio_unitario = prod_obj.get_precio()
        total_bruto = precio_unitario * cant

        # Polimorfismo con clases de Clientes del Primer Parcial
        tipo_cliente = dd_ped_tipo.value
        if tipo_cliente == "Mayorista":
            c_obj = ClienteMayorista(cliente_nom)
            total_neto = c_obj.calcularDescuento(total_bruto)
            etiqueta_cliente = f"{cliente_nom} (Mayorista -15%)"
        elif tipo_cliente == "Minorista":
            c_obj = ClienteMinorista(cliente_nom)
            total_neto = c_obj.calcularDescuento(total_bruto)
            etiqueta_cliente = f"{cliente_nom} (Minorista -5%)"
        else:
            total_neto = total_bruto
            etiqueta_cliente = f"{cliente_nom} (Normal)"

        precio_final_unitario = total_neto / cant
        nuevo_pedido = Pedido(etiqueta_cliente, prod_nom, cant, precio_final_unitario)

        repo_pedidos.agregar_pedido(nuevo_pedido)
        GestorPersistencia.guardar_pedidos(repo_pedidos)
        refrescar_pedidos()
        msg_ped(f"✅ Pedido #{nuevo_pedido.id} encolado al final de la fila y persistido en 'pedidos.json'.")
        f_ped_cliente.value = ""
        f_ped_cant.value = "1"
        page.update()

    def on_atender_siguiente(e):
        if not repo_pedidos.hay_pendientes():
            msg_ped("⚠️ No hay pedidos en cola para atender.", ft.colors.ORANGE_800)
            return

        pedido_atendido = repo_pedidos.procesar_siguiente()
        GestorPersistencia.guardar_pedidos(repo_pedidos)
        refrescar_pedidos()
        msg_ped(f"🎉 Pedido #{pedido_atendido.id} atendido con éxito (Total cobrado: ${pedido_atendido.total:.2f}). Guardado en JSON.", ft.colors.GREEN_800)

    btn_encolar = ft.ElevatedButton("➕ Encolar Pedido", icon=ft.icons.QUEUE,
                                   on_click=on_encolar_pedido, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE)
    btn_atender = ft.ElevatedButton("⚡ Atender Siguiente Pedido (FIFO)", icon=ft.icons.CHECK_CIRCLE,
                                   on_click=on_atender_siguiente, bgcolor=ft.colors.GREEN_700, color=ft.colors.WHITE)

    vista_pedidos = ft.Container(
        padding=10,
        content=ft.Column([
            ft.Text("Sistema de Gestión de Pedidos - Cola FIFO y Patrón Repository (Semana 7)",
                    size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
            ft.Text("Los pedidos ingresan por el final y se procesan estrictamente por el frente (First-In, First-Out).",
                    size=12, color=ft.colors.GREY_700),
            ft.Container(
                bgcolor=ft.colors.WHITE,
                padding=14,
                border_radius=8,
                border=ft.border.all(1, ft.colors.BLUE_GREY_100),
                content=ft.Column([
                    ft.Row([f_ped_cliente, dd_ped_tipo, dd_ped_prod, f_ped_cant], wrap=True, spacing=10),
                    ft.Row([btn_encolar, btn_atender], spacing=10),
                ], spacing=10),
            ),
            lbl_ped_msg,
            ft.Divider(),
            ft.Text("Visualización de la Cola FIFO en Tiempo Real:", weight=ft.FontWeight.BOLD, size=13),
            lbl_ped_resumen,
            ft.Container(
                content=ft.Column([fila_visual_cola], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200),
                border_radius=8,
                padding=12,
            ),
            ft.Divider(),
            ft.Text("Historial de Pedidos Procesados / Atendidos:", weight=ft.FontWeight.BOLD, size=13),
            ft.Container(
                content=ft.Column([tabla_procesados], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.BLUE_GREY_200),
                border_radius=8,
                padding=10,
                height=180,
            ),
        ], spacing=8, scroll=ft.ScrollMode.AUTO)
    )

    # ──────────────────────────────────────────────────────────────────────────
    # NAVEGACIÓN PRINCIPAL CON TABS (PESTAÑAS)
    # ──────────────────────────────────────────────────────────────────────────
    pestanas = ft.Tabs(
        selected_index=0,
        animation_duration=250,
        tabs=[
            ft.Tab(
                text="Catálogo de Productos",
                icon=ft.icons.STOREFRONT,
                content=vista_catalogo,
            ),
            ft.Tab(
                text="Cola de Pedidos (FIFO)",
                icon=ft.icons.FORMAT_LIST_NUMBERED,
                content=vista_pedidos,
            ),
        ],
        expand=1,
    )

    page.add(
        ft.Column([
            ft.Row([
                ft.Icon(ft.icons.SHOPPING_BAG, size=28, color=ft.colors.BLUE_800),
                ft.Column([
                    ft.Text("Sistema de Gestión de Tienda y Pedidos", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.Text("Examen Final: Integración Semanas 5, 6 y 7 | Persistencia de Datos JSON | Jonathan Cerezo", size=11, color=ft.colors.BLUE_GREY_700),
                ], spacing=1),
            ], alignment=ft.MainAxisAlignment.START),
            pestanas,
        ], expand=True, spacing=10)
    )

    refrescar_catalogo()
    refrescar_pedidos()


if __name__ == "__main__":
    ft.app(target=main)
