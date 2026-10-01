# -*- coding: utf-8 -*-
"""
generar_pdf_semana7.py - Genera el PDF de entrega Semana 7
Ejecutar: python generar_pdf_semana7.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

PDF_SALIDA   = r"C:\Users\Personal\Desktop\Programacion Estructurada\tienda\Cerezo_Jonathan_Semana7.pdf"
IMG_PYTEST   = r"C:\Users\Personal\.gemini\antigravity\brain\e2945066-966d-49fb-ad51-05ba89caaaf5\pytest_results_semana7_1790897282666.jpg"
IMG_DEMO     = r"C:\Users\Personal\.gemini\antigravity\brain\e2945066-966d-49fb-ad51-05ba89caaaf5\demo_semana7_clean_1790897327182.jpg"

DEMO_OUTPUT = """\
=======================================================
  TIENDA - Sistema de Pedidos (Semana 7)
  Cola FIFO + Patrón Repository
=======================================================

-- Registrando pedidos en la cola --
  + Pedido #1 | Jonathan Cerezo | Laptop HP x1   | $1200.00 | [pendiente]
  + Pedido #2 | Maria Lopez     | Mouse USB x3   |   $46.50 | [pendiente]
  + Pedido #3 | Carlos Ruiz     | Teclado x2     |   $90.00 | [pendiente]
  + Pedido #4 | Ana Torres      | Monitor 24 x1  |  $350.00 | [pendiente]

Pedidos pendientes : 4
Siguiente a atender: Pedido #1 | Jonathan Cerezo | Laptop HP x1 | $1200.00

-- Procesando pedidos (orden FIFO) --
  [OK] Pedido #1 | Jonathan Cerezo | Laptop HP x1   | $1200.00 | [procesado]
  [OK] Pedido #2 | Maria Lopez     | Mouse USB x3   |   $46.50 | [procesado]
  [OK] Pedido #3 | Carlos Ruiz     | Teclado x2     |   $90.00 | [procesado]
  [OK] Pedido #4 | Ana Torres      | Monitor 24 x1  |  $350.00 | [procesado]

Total procesados: 4
Cola vacía      : True"""

PYTEST_OUTPUT = """\
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1
rootdir: Programación Estructurada/tienda
collected 21 items

test_semana7.py::TestCola::test_cola_nueva_esta_vacía               PASSED [ 4%]
test_semana7.py::TestCola::test_tamaño_inicial_es_cero              PASSED [ 9%]
test_semana7.py::TestCola::test_encolar_aumenta_tamaño              PASSED [14%]
test_semana7.py::TestCola::test_encolar_varios_elementos            PASSED [19%]
test_semana7.py::TestCola::test_frente_no_elimina_elemento          PASSED [23%]
test_semana7.py::TestCola::test_orden_fifo                          PASSED [28%]
test_semana7.py::TestCola::test_desencolar_reduce_tamaño            PASSED [33%]
test_semana7.py::TestCola::test_desencolar_hasta_vacía              PASSED [38%]
test_semana7.py::TestCola::test_desencolar_cola_vacía_lanza_error   PASSED [42%]
test_semana7.py::TestCola::test_frente_cola_vacía_lanza_error       PASSED [47%]
test_semana7.py::TestCola::test_listar_orden_correcto               PASSED [52%]
test_semana7.py::TestCola::test_len_retorna_tamaño                  PASSED [57%]
test_semana7.py::TestPedidoRepository::test_repositorio_nuevo_sin_pedidos    PASSED [61%]
test_semana7.py::TestPedidoRepository::test_agregar_pedido_aumenta_pendientes PASSED [66%]
test_semana7.py::TestPedidoRepository::test_ver_siguiente_no_elimina         PASSED [71%]
test_semana7.py::TestPedidoRepository::test_procesar_cambia_estado_a_procesado PASSED [76%]
test_semana7.py::TestPedidoRepository::test_procesar_reduce_pendientes       PASSED [80%]
test_semana7.py::TestPedidoRepository::test_orden_atención_fifo              PASSED [85%]
test_semana7.py::TestPedidoRepository::test_total_pedido_precio_por_cantidad PASSED [90%]
test_semana7.py::TestPedidoRepository::test_procesar_sin_pedidos_lanza_error PASSED [95%]
test_semana7.py::TestPedidoRepository::test_listar_procesados                PASSED [100%]

============================= 21 passed in 0.12s =============================="""


def P(texto, estilo):
    return Paragraph(texto, estilo)


def generar():
    doc = SimpleDocTemplate(
        PDF_SALIDA, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )

    estilos = getSampleStyleSheet()
    AZUL       = colors.HexColor("#1565C0")
    AZUL_CLARO = colors.HexColor("#E3F2FD")
    AZUL_BORDE = colors.HexColor("#90CAF9")
    VERDE      = colors.HexColor("#1B5E20")

    titulo_doc = ParagraphStyle("titulo_doc", parent=estilos["Title"],
        fontSize=18, textColor=AZUL, spaceAfter=4, alignment=TA_CENTER)
    subtitulo = ParagraphStyle("subtitulo", parent=estilos["Normal"],
        fontSize=11, textColor=colors.HexColor("#37474F"), spaceAfter=2, alignment=TA_CENTER)
    seccion = ParagraphStyle("seccion", parent=estilos["Heading2"],
        fontSize=13, textColor=AZUL, spaceBefore=12, spaceAfter=6)
    cuerpo = ParagraphStyle("cuerpo", parent=estilos["Normal"],
        fontSize=10, leading=16, alignment=TA_JUSTIFY, spaceAfter=6)
    celda = ParagraphStyle("celda", parent=estilos["Normal"],
        fontSize=9, leading=13, wordWrap='CJK')
    celda_b = ParagraphStyle("celda_b", parent=celda, fontName="Helvetica-Bold")
    cab = ParagraphStyle("cab", parent=celda,
        fontName="Helvetica-Bold", textColor=colors.white)
    code_style = ParagraphStyle("code_style", parent=estilos["Normal"],
        fontName="Courier", fontSize=8, leading=12,
        backColor=colors.HexColor("#F5F5F5"), leftIndent=0)
    pie_style = ParagraphStyle("pie", parent=estilos["Normal"],
        fontSize=9, textColor=colors.grey, alignment=TA_CENTER)

    h = []  # historia

    # ── ENCABEZADO ──────────────────────────────────────────────────────────
    h.append(Spacer(1, 0.3*cm))
    h.append(P("Tienda - Sistema de Pedidos", titulo_doc))
    h.append(P("Semana 7: Patrónes de Diseño, Testing Unitario y TDA Lineales", subtitulo))
    h.append(Spacer(1, 0.3*cm))
    h.append(HRFlowable(width="100%", thickness=1.5, color=AZUL))
    h.append(Spacer(1, 0.3*cm))

    # Datos estudiante
    datos = [
        [P("Estudiante",       celda_b), P("Jonathan Andres Cerezo Alava", celda)],
        [P("Materia",          celda_b), P("Programación Estructurada",     celda)],
        [P("Actividad",        celda_b), P("Semana 7",                       celda)],
        [P("Repositorio",      celda_b), P("https://github.com/jonathancerezo/tienda-python", celda)],
    ]
    t = Table(datos, colWidths=[4*cm, 12.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), AZUL_CLARO),
        ("GRID",       (0,0), (-1,-1), 0.5, AZUL_BORDE),
        ("PADDING",    (0,0), (-1,-1), 6),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    h.append(t)
    h.append(Spacer(1, 0.4*cm))
    h.append(HRFlowable(width="100%", thickness=0.5, color=AZUL_BORDE))

    # ── 1. DESCRIPCION ───────────────────────────────────────────────────────
    h.append(P("1. Descripción del Problema", seccion))
    h.append(P(
        "Se implementó un sistema de gestión de pedidos para la tienda. Cuando un cliente "
        "hace un pedido, este debe ser atendido en el mismo orden en que llegó: el primero "
        "en llegar es el primero en ser atendido. Este es el comportamiento de una "
        "<b>Cola FIFO (First In, First Out)</b>.", cuerpo))

    # ── 2. ESTRUCTURA DE DATOS ───────────────────────────────────────────────
    h.append(P("2. Estructura de Datos: Cola (Queue)", seccion))
    h.append(P(
        "La cola fue implementada <b>manualmente</b> en <b>cola.py</b> usando nodos enlazados "
        "(clase <i>NodoCola</i>), sin usar <i>queue.Queue</i> ni <i>collections.deque</i>.", cuerpo))

    ops = [
        [P("Operación",       cab), P("Metodo",         cab), P("Descripción", cab)],
        [P("Agregar",     celda_b), P("encolar()",    celda), P("Agrega un elemento al final de la cola.", celda)],
        [P("Eliminar",    celda_b), P("desencolar()", celda), P("Elimina y retorna el elemento del frente (lanza IndexError si vacía).", celda)],
        [P("Consultar",   celda_b), P("frente()",     celda), P("Retorna el siguiente elemento sin eliminarlo.", celda)],
        [P("Verificar",   celda_b), P("esta_vacía()", celda), P("Retorna True si no hay elementos en la cola.", celda)],
        [P("Cantidad",    celda_b), P("tamaño()",     celda), P("Retorna el número de elementos almacenados.", celda)],
    ]
    t2 = Table(ops, colWidths=[2.8*cm, 3.2*cm, 10.5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL),
        ("ROWBACKGROUND", (0,1), (-1,-1), [colors.white, AZUL_CLARO]),
        ("GRID",    (0,0), (-1,-1), 0.5, AZUL_BORDE),
        ("PADDING", (0,0), (-1,-1), 5),
        ("VALIGN",  (0,0), (-1,-1), "TOP"),
    ]))
    h.append(t2)

    # ── 3. PATRON REPOSITORY ────────────────────────────────────────────────
    h.append(P("3. Patrón de Diseño Repository", seccion))
    h.append(P(
        "El archivo <b>repository.py</b> implementa la clase <i>PedidoRepository</i> que "
        "aplica el patrón <b>Repository</b>. Este patrón <b>separa el acceso y manejo de "
        "los datos</b> (la Cola) <b>de la lógica principal</b> de la aplicación.", cuerpo))
    h.append(P(
        "La aplicación nunca manipula la Cola directamente. Solo usa los metodos del "
        "Repository: <i>agregar_pedido()</i>, <i>procesar_siguiente()</i>, "
        "<i>ver_siguiente()</i>, <i>hay_pendientes()</i>, <i>total_pendientes()</i>.", cuerpo))

    mets = [
        [P("Metodo",                    cab), P("Descripción", cab)],
        [P("agregar_pedido(pedido)",  celda_b), P("Encola un nuevo pedido al final de la fila de atención.", celda)],
        [P("procesar_siguiente()",    celda_b), P("Desencola el pedido del frente, lo marca como 'procesado' y lo guarda.", celda)],
        [P("ver_siguiente()",         celda_b), P("Retorna el pedido del frente sin procesarlo (consulta).", celda)],
        [P("hay_pendientes()",        celda_b), P("Retorna True si hay pedidos esperando ser atendidos.", celda)],
        [P("total_pendientes()",      celda_b), P("Retorna la cantidad de pedidos en la cola.", celda)],
        [P("listar_procesados()",     celda_b), P("Retorna la lista de pedidos ya atendidos.", celda)],
    ]
    t3 = Table(mets, colWidths=[5.5*cm, 11*cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#0D47A1")),
        ("ROWBACKGROUND", (0,1), (-1,-1), [colors.white, colors.HexColor("#E8F5E9")]),
        ("GRID",    (0,0), (-1,-1), 0.5, AZUL_BORDE),
        ("PADDING", (0,0), (-1,-1), 5),
        ("VALIGN",  (0,0), (-1,-1), "TOP"),
    ]))
    h.append(t3)

    # ── 4. PRUEBAS UNITARIAS ────────────────────────────────────────────────
    h.append(PageBreak())
    h.append(P("4. Pruebas Unitarias (pytest)", seccion))
    h.append(P(
        "Se implementaron <b>21 pruebas unitarias</b> en <b>test_semana7.py</b> usando "
        "<b>pytest</b>, divididas en dos clases: <i>TestCola</i> (12 pruebas) y "
        "<i>TestPedidoRepository</i> (9 pruebas).", cuerpo))

    pruebas = [
        [P("Clase",              cab), P("Prueba",             cab), P("Que verifica", cab)],
        [P("TestCola",       celda_b), P("test_cola_nueva_esta_vacía",           celda), P("Cola recién creada esta vacía.", celda)],
        [P("TestCola",       celda_b), P("test_tamaño_inicial_es_cero",          celda), P("Tamaño inicial es 0.", celda)],
        [P("TestCola",       celda_b), P("test_encolar_aumenta_tamaño",          celda), P("Encolar un elemento aumenta el tamaño.", celda)],
        [P("TestCola",       celda_b), P("test_frente_no_elimina_elemento",      celda), P("frente() no elimina el elemento.", celda)],
        [P("TestCola",       celda_b), P("test_orden_fifo",                      celda), P("Los elementos salen en orden FIFO.", celda)],
        [P("TestCola",       celda_b), P("test_desencolar_cola_vacía_lanza_error",celda), P("IndexError al desencolar cola vacía.", celda)],
        [P("TestCola",       celda_b), P("test_frente_cola_vacía_lanza_error",   celda), P("IndexError al ver frente de cola vacía.", celda)],
        [P("TestCola",       celda_b), P("test_listar_orden_correcto",           celda), P("listar() retorna elementos en orden correcto.", celda)],
        [P("TestRepo",       celda_b), P("test_repositorio_nuevo_sin_pedidos",   celda), P("Repository nuevo sin pedidos.", celda)],
        [P("TestRepo",       celda_b), P("test_agregar_pedido_aumenta_pendientes",celda), P("Agregar pedido aumenta pendientes.", celda)],
        [P("TestRepo",       celda_b), P("test_procesar_cambia_estado",          celda), P("Procesar cambia estado a 'procesado'.", celda)],
        [P("TestRepo",       celda_b), P("test_orden_atención_fifo",             celda), P("Pedidos procesados en orden de llegada.", celda)],
        [P("TestRepo",       celda_b), P("test_procesar_sin_pedidos_lanza_error",celda), P("IndexError al procesar sin pedidos.", celda)],
    ]
    t4 = Table(pruebas, colWidths=[2.5*cm, 6*cm, 8*cm])
    t4.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL),
        ("ROWBACKGROUND", (0,1), (-1,-1), [colors.white, AZUL_CLARO]),
        ("GRID",    (0,0), (-1,-1), 0.5, AZUL_BORDE),
        ("PADDING", (0,0), (-1,-1), 4),
        ("VALIGN",  (0,0), (-1,-1), "TOP"),
    ]))
    h.append(t4)

    # ── 5. RESULTADOS PRUEBAS ───────────────────────────────────────────────
    h.append(P("5. Resultado de las Pruebas Unitarias", seccion))
    h.append(P("Comando ejecutado: <b>python -m pytest test_semana7.py -v</b>", cuerpo))
    h.append(Spacer(1, 0.2*cm))
    h.append(Image(IMG_PYTEST, width=16.5*cm, height=9.3*cm))
    h.append(Spacer(1, 0.3*cm))
    h.append(P("<b>Resultado: 21 pruebas ejecutadas — 21 PASSED (0 FAILED)</b>",
               ParagraphStyle("ok", parent=cuerpo, textColor=VERDE, fontName="Helvetica-Bold")))

    # ── 6. DEMO ─────────────────────────────────────────────────────────────
    h.append(P("6. Salida del Programa (demo_semana7.py)", seccion))
    h.append(P("Comando ejecutado: <b>python demo_semana7.py</b>", cuerpo))
    h.append(Spacer(1, 0.2*cm))
    h.append(Image(IMG_DEMO, width=16.5*cm, height=9.3*cm))


    # ── PIE ─────────────────────────────────────────────────────────────────
    h.append(Spacer(1, 0.8*cm))
    h.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    h.append(Spacer(1, 0.2*cm))
    h.append(P("Jonathan Andres Cerezo Alava | Programación Estructurada | Semana 7", pie_style))
    h.append(P("https://github.com/jonathancerezo/tienda-python", pie_style))

    doc.build(h)
    print("PDF generado: " + PDF_SALIDA)


if __name__ == "__main__":
    generar()
