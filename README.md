# 🛒 Tienda Virtual — Sistema Integral de Gestión y Pedidos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Flet%200.23.2-00bcd4?logo=flutter&logoColor=white)
![Testing](https://img.shields.io/badge/Pytest-24%20Passed-brightgreen?logo=pytest&logoColor=white)
![Persistencia](https://img.shields.io/badge/Persistencia-JSON-orange)
![Estado](https://img.shields.io/badge/Examen-Completado-success)

**Estudiante:** Jonathan Andrés Cerezo Álava  
**Materia:** Programación Estructurada  
**Lenguaje Utilizado:** Python 3.10+  
**Actividad:** Examen — Presentación y Explicación del Proyecto (Semanas 5, 6 y 7)  
**Repositorio GitHub:** [jonathancerezo456-pixel/tienda-semana-7](https://github.com/jonathancerezo456-pixel/tienda-semana-7)  

---

## 📑 Tabla de Contenidos
1. [Descripción Breve](#1-descripción-breve)
2. [Objetivo del Proyecto](#2-objetivo-del-proyecto)
3. [Principales Funcionalidades](#3-principales-funcionalidades)
   - [Persistencia de Datos (Obligatorio)](#31--persistencia-de-datos-requisito-obligatorio)
   - [Interfaz Gráfica de Usuario](#32-️-interfaz-gráfica-de-usuario-gui-con-flet)
   - [Colecciones de Datos (Semana 5)](#33--manejo-de-colecciones-semana-5)
   - [TDA Lineal Cola FIFO y Repository (Semana 7)](#34--tda-lineal-cola-fifo-y-patrón-repository-semana-7)
   - [POO y Polimorfismo Dinámico](#35--programación-orientada-a-objetos-y-polimorfismo)
   - [Testing Automatizado con Pytest](#36--suite-de-pruebas-unitarias-con-pytest)
4. [Estructura y Organización del Código](#4-estructura-y-organización-del-código)
5. [Instrucciones de Instalación y Ejecución](#5-instrucciones-de-instalación-y-ejecución)
6. [Demostración de Persistencia en Vivo](#6-demostración-de-persistencia-en-vivo-paso-a-paso)

---

## 1. Descripción Breve

Este proyecto es una aplicación integral de escritorio desarrollada en **Python** para la administración de un catálogo comercial y el procesamiento de una fila de pedidos de clientes. 

El software unifica de forma progresiva todos los aprendizajes adquiridos a lo largo del curso:
- **Primer Parcial (POO):** Clases, encapsulamiento con atributos privados, herencia y polimorfismo dinámico (`Cliente`, `ClienteMayorista`, `ClienteMinorista`, `Producto`, `ProductoElectronico`, `Marca`).
- **Semana 5 (Colecciones):** Gestión eficiente de colecciones en memoria (`list`, `dict`, `set`) para operaciones CRUD y detección de duplicados.
- **Semana 6 (Interfaz Gráfica):** Interfaz moderna y reactiva basada en **Flet** con componentes interactivos y validación de formularios en tiempo real.
- **Semana 7 (TDA Lineal y Patrones):** Implementación manual de una **Cola FIFO con nodos enlazados**, desacoplamiento con el patrón de diseño **Repository** y suite de pruebas unitarias con **pytest**.
- **Requisito del Examen (Persistencia de Datos):** Módulo de persistencia local en archivos **JSON** que garantiza que los datos se preserven entre ejecuciones del programa.

---

## 2. Objetivo del Proyecto

Demostrar la aplicación práctica de los conocimientos de programación estructurada, modular y orientada a objetos mediante una solución de software completa que permita:
1. Administrar productos normales y electrónicos con operaciones CRUD y unicidad en tiempo constante $O(1)$.
2. Gestionar una fila de espera de pedidos bajo la política estricta **First-In, First-Out (FIFO)**.
3. Aplicar polimorfismo para calcular automáticamente descuentos especiales según el tipo de cliente.
4. Almacenar y recuperar la información de forma persistente y tolerante a fallos en archivos JSON.
5. Brindar una experiencia visual interactiva e intuitiva mediante una GUI de escritorio.

---

## 3. Principales Funcionalidades

### 3.1. 💾 Persistencia de Datos (Requisito Obligatorio)
- Implementada en el módulo [`persistencia.py`](persistencia.py) a través de la clase `GestorPersistencia`.
- **Almacenamiento y Recuperación:** Gestiona dos archivos JSON locales:
  - `productos.json`: Guarda la lista completa de productos (nombre, precio, stock, tipo, garantía y marca).
  - `pedidos.json`: Guarda tanto los pedidos en cola de espera (pendientes) como el historial de pedidos atendidos (procesados).
- **Sincronización Inmediata:** Cualquier alta, edición, eliminación, encolado o atención de pedido se graba al instante en disco.
- **Tolerancia a fallos:** Si la aplicación inicia sin los archivos JSON previos, el sistema detecta su ausencia, inicializa datos de prueba de forma transparente y genera los archivos automáticamente sin interrupciones ni errores.

### 3.2. 🖥️ Interfaz Gráfica de Usuario (GUI con Flet)
- Desarrollada en [`main_gui.py`](main_gui.py) utilizando la librería **Flet (v0.23.2)**.
- Estructura visual organizada en dos pestañas principales (*Tabs*):
  - **Pestaña 1: Catálogo de Productos:** 
    - Formulario reactivo con soporte para productos estándar y electrónicos (activa dinámicamente campo de garantía y marca).
    - Validación visual de entradas numéricas y campos requeridos.
    - Búsqueda en tiempo real por coincidencia de texto.
    - Carga interactiva al hacer clic en las filas de la tabla.
    - Cuadro de diálogo modal de confirmación antes de eliminar.
  - **Pestaña 2: Cola de Pedidos (FIFO):**
    - Formulario de emisión de pedidos seleccionando productos directamente del catálogo.
    - Selector de tipo de cliente que aplica automáticamente el descuento polimórfico.
    - **Visualizador gráfico de la Cola en tiempo real:** Muestra de forma secuencial los pedidos en espera (`⚡ FRENTE ➔ [Pedido #1] ➔ [Pedido #2] ➔ FINAL`).
    - Botón destacado para atender el siguiente pedido por orden FIFO.
    - Tabla con el historial de pedidos procesados con fecha, hora y totales.

### 3.3. 📦 Manejo de Colecciones (Semana 5)
En [`catalogo.py`](catalogo.py), se integran tres estructuras nativas de Python, cada una cumpliendo un objetivo específico de diseño algorítmico:

| Colección | Atributo | Propósito en el Catálogo | Complejidad Temporal |
|---|---|---|:---:|
| `list` | `_lista` | Mantiene el orden de inserción y permite listar/recorrer | $O(N)$ recorrido |
| `dict` | `_indice` | Permite búsquedas directas e instantáneas por nombre del producto | $O(1)$ búsqueda |
| `set` | `_nombres` | Valida la unicidad y previene duplicados en tiempo constante | $O(1)$ validación |

### 3.4. 🔄 TDA Lineal Cola FIFO y Patrón Repository (Semana 7)
- **Cola implementada manualmente:** En [`cola.py`](cola.py) mediante nodos enlazados (`NodoCola`), sin emplear `queue.Queue` ni `collections.deque`.
  - Operaciones: `encolar()` (agrega al final), `desencolar()` (elimina del frente), `frente()` (consulta el siguiente sin eliminar), `esta_vacia()`, `tamano()` y `listar()`.
- **Patrón Repository:** En [`repository.py`](repository.py), la clase `PedidoRepository` aísla el acceso y la estructura de datos interna del resto de la aplicación.
- **Encapsulación estricta:** En [`pedido.py`](pedido.py), atributos estrictamente privados (`__id`, `__cliente`, `__producto`, `__cantidad`, `__precio`, `__estado`), protegidos con decoradores `@property` y validación en setters.

### 3.5. 🧩 Programación Orientada a Objetos y Polimorfismo
- **Jerarquía de Clientes:**
  - `Cliente` ([`cliente.py`](cliente.py)): Clase abstracta con método abstracto `@abstractmethod def calcularDescuento(self, total)`.
  - `ClienteMayorista` ([`cliente_mayorista.py`](cliente_mayorista.py)): Implementa un **15% de descuento**.
  - `ClienteMinorista` ([`cliente_minorista.py`](cliente_minorista.py)): Implementa un **5% de descuento**.
- **Jerarquía de Productos:**
  - `Producto` ([`producto.py`](producto.py)): Clase base con encapsulamiento.
  - `ProductoElectronico` ([`producto_electronico.py`](producto_electronico.py)): Clase hija con herencia que añade `garantia` y composición con la clase `Marca` ([`marca.py`](marca.py)).

### 3.6. 🧪 Suite de Pruebas Unitarias con Pytest
- Implementada en [`test_semana7.py`](test_semana7.py) con **24 pruebas automatizadas**:
  - **12 pruebas de Cola FIFO:** Comprobación de cola vacía, inserción, extracción, orden FIFO estricto, manejo de excepciones (`IndexError`) y longitud.
  - **9 pruebas de Repository:** Registro de pedidos, procesamiento, orden de atención, cálculo de importes y transición de estados.
  - **3 pruebas de Persistencia JSON:** Almacenamiento y recuperación de catálogo, persistencia de cola de pedidos y tolerancia ante archivos inexistentes.
- **Resultado:** **24 passed (100% de éxito en 0.3 segundos)**.

---

## 4. Estructura y Organización del Código

```text
tienda/
│
├── persistencia.py          # Capa de persistencia: guarda y recupera datos en JSON (Examen)
├── main_gui.py              # Interfaz Gráfica interactiva con Flet (Catálogo + Cola de Pedidos)
│
├── cola.py                  # TDA Lineal: Cola FIFO manual con nodos enlazados (Semana 7)
├── pedido.py                # Clase Pedido con atributos privados, getters/setters y serialización
├── repository.py            # Patrón de diseño Repository para pedidos (Semana 7)
├── test_semana7.py          # Suite de 24 pruebas unitarias automatizadas con pytest
├── demo_semana7.py          # Demostración del funcionamiento de la cola por consola
│
├── catalogo.py              # Gestión del catálogo con colecciones list + dict + set (Semana 5)
├── producto.py              # Clase base Producto (POO - Primer Parcial)
├── producto_electronico.py  # Clase hija ProductoElectronico con garantía y marca
├── marca.py                 # Clase auxiliar Marca
├── cliente.py               # Clase base abstracta Cliente con método abstracto de descuento
├── cliente_mayorista.py     # Cliente con 15% de descuento (Polimorfismo dinámico)
├── cliente_minorista.py     # Cliente con 5% de descuento (Polimorfismo dinámico)
├── main.py                  # Demostración del primer parcial por consola
│
├── productos.json           # Archivo JSON de persistencia (se genera automáticamente)
├── pedidos.json             # Archivo JSON de persistencia de pedidos (se genera automáticamente)
└── README.md                # Documentación técnica completa del proyecto
```

---

## 5. Instrucciones de Instalación y Ejecución

### 5.1. Requisitos Previos
- Contar con **Python 3.10** o superior instalado en el equipo.

### 5.2. Instalación de Dependencias
Abra su terminal o consola en la carpeta raíz del proyecto y ejecute:

```bash
pip install flet==0.23.2 pytest
```

### 5.3. Ejecutar la Aplicación Gráfica (GUI Principal)
Para iniciar la interfaz interactiva completa con persistencia y cola de pedidos:

```bash
python main_gui.py
```

### 5.4. Ejecutar las Pruebas Unitarias
Para comprobar la integridad del sistema y las 24 pruebas automatizadas:

```bash
python -m pytest test_semana7.py -v
```

*Resultado esperado en consola:*
```text
============================= 24 passed in 0.30s ==============================
```

### 5.5. Ejecutar Demostraciones por Consola (Opcional)
```bash
# Demostración de Cola FIFO y Repository (Semana 7):
python demo_semana7.py

# Demostración de POO y Polimorfismo (Primer Parcial):
python main.py
```

---

## 6. Demostración de Persistencia en Vivo (Paso a Paso)

Para verificar la tolerancia a fallos y la persistencia de datos durante la evaluación:
1. **Generación automática:** Si la aplicación se inicia sin archivos JSON previos, el sistema detecta su ausencia y genera automáticamente `productos.json` y `pedidos.json` con datos iniciales de prueba.
2. **Registro de datos:** En la pestaña **Catálogo de Productos**, agregue un nuevo producto (ej. *"Tablet Lenovo"*, precio `$220`, stock `8`).
3. **Gestión en cola:** En la pestaña **Cola de Pedidos**, agregue un pedido para dicho producto y atienda uno de los pedidos pendientes mediante el botón verde **Atender Siguiente Pedido**.
4. **Cierre de aplicación:** Cierre la ventana de la interfaz gráfica.
5. **Comprobación en disco:** Abra los archivos `productos.json` y `pedidos.json` en el editor para constatar que los datos nuevos y modificados quedaron registrados físicamente en disco.
6. **Recuperación:** Vuelva a ejecutar `python main_gui.py` y observe cómo la aplicación recupera exactamente todo el estado anterior.
