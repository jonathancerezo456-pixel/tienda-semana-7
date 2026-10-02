# 🛒 Tienda Virtual — Sistema Integral de Gestión y Pedidos

**Estudiante:** Jonathan Andrés Cerezo Álava  
**Materia:** Programación Estructurada  
**Lenguaje Utilizado:** Python 3.10+  
**Entrega:** Examen — Presentación y Explicación del Proyecto (Semanas 5, 6 y 7)  
**Repositorio GitHub:** [jonathancerezo456-pixel/tienda-semana-7](https://github.com/jonathancerezo456-pixel/tienda-semana-7)  

---

## 1. Descripción Breve

Este proyecto es una aplicación de escritorio desarrollada en **Python** para la gestión de productos y procesamiento de pedidos en una tienda comercial. Integra de manera unificada todos los conceptos desarrollados a lo largo del curso:

1. **Primer Parcial (POO):** Clases, encapsulación con atributos privados, herencia y polimorfismo dinámico (`Cliente`, `ClienteMayorista`, `ClienteMinorista`, `Producto`, `ProductoElectronico`, `Marca`).
2. **Semana 5 (Colecciones):** Implementación de un catálogo utilizando `list`, `dict` y `set` para optimizar búsquedas, inserciones y validación de duplicados.
3. **Semana 6 (Interfaz Gráfica):** Creación de una GUI moderna, reactiva e interactiva utilizando la librería **Flet**.
4. **Semana 7 (TDA Lineal y Patrones):** Implementación manual de una **Cola FIFO con nodos enlazados**, administración mediante el patrón de diseño **Repository** y suite de pruebas unitarias con **pytest**.
5. **Elemento del Examen (Persistencia de Datos):** Módulo de persistencia que almacena y recupera el estado completo de la aplicación en archivos **JSON** locales.

---

## 2. Objetivo del Proyecto

El objetivo principal es demostrar la aplicación práctica de los conocimientos de programación estructurada y orientada a objetos en una solución de software completa, modular y robusta. 

La aplicación permite:
- Administrar el catálogo de productos con operaciones CRUD completas y prevención de duplicados en $O(1)$.
- Gestionar una fila de pedidos de clientes garantizando atención en orden de llegada (**First-In, First-Out**).
- Aplicar polimorfismo para calcular automáticamente descuentos especiales según el tipo de cliente.
- Mantener la información persistente entre sesiones mediante archivos JSON.
- Proporcionar una interfaz visual amigable y reactiva para el usuario final.

---

## 3. Principales Funcionalidades

### 3.1. 💾 Persistencia de Datos (Requisito Obligatorio)
- Implementada en el módulo [`persistencia.py`](persistencia.py) a través de la clase `GestorPersistencia`.
- **Almacenamiento y Recuperación:** Guarda y carga los datos en dos archivos JSON locales:
  - `productos.json`: Guarda la lista completa de productos normales y electrónicos (precios, stock, garantías y marcas).
  - `pedidos.json`: Guarda tanto los pedidos que se encuentran en cola de espera (pendientes) como el historial de pedidos ya atendidos (procesados).
- **Sincronización Inmediata:** Cualquier acción realizada en la interfaz (agregar producto, editar precio, eliminar producto, encolar pedido o atender pedido) se guarda inmediatamente en disco.
- **Tolerancia a fallos:** Si los archivos no existen al abrir el programa por primera vez, el sistema inicializa datos de demostración y genera los archivos automáticamente.

### 3.2. 🖥️ Interfaz Gráfica de Usuario (GUI con Flet)
- Desarrollada en [`main_gui.py`](main_gui.py) utilizando **Flet** (tecnología basada en Flutter).
- Cuenta con dos pestañas (*Tabs*) integradas:
  - **Pestaña 1: Catálogo de Productos:** Formulario para agregar productos (estándar o electrónicos con garantía y marca), validación visual de campos en tiempo real, búsqueda por coincidencia parcial, tabla de datos interactiva (al hacer clic en una fila se carga en el formulario) y diálogo modal de confirmación antes de eliminar.
  - **Pestaña 2: Cola de Pedidos (FIFO):** Formulario para crear pedidos asociando clientes del catálogo, selección de tipo de cliente (Normal, Mayorista con 15% de descuento, Minorista con 5% de descuento), **visualizador dinámico de la Cola en tiempo real** (`⚡ FRENTE ➔ [Pedido #1] ➔ [Pedido #2] ➔ FINAL`), botón destacado para atender el siguiente pedido y tabla con el historial de pedidos procesados.

### 3.3. 📦 Manejo de Colecciones (Semana 5)
Implementado en [`catalogo.py`](catalogo.py), donde cada colección cumple un rol específico:
- `list` (`_lista`): Preserva el orden cronológico de inserción y permite iterar los productos en la tabla.
- `dict` (`_indice`): Permite realizar búsquedas exactas por nombre en tiempo constante $O(1)$.
- `set` (`_nombres`): Verifica la unicidad del nombre del producto e impide registros duplicados en tiempo constante $O(1)$.

### 3.4. 🔄 TDA Lineal Cola FIFO y Patrón Repository (Semana 7)
- **Cola implementada manualmente:** En [`cola.py`](cola.py) mediante nodos enlazados (`NodoCola`), sin usar librerías externas como `queue` o `deque`. Métodos implementados: `encolar()`, `desencolar()`, `frente()`, `esta_vacia()`, `tamano()`, `listar()`.
- **Patrón Repository:** En [`repository.py`](repository.py), la clase `PedidoRepository` aísla la estructura de datos interna de la lógica de negocio de la tienda.
- **Encapsulación:** En [`pedido.py`](pedido.py), atributos estrictamente privados (`__id`, `__cliente`, `__producto`, `__total`, `__estado`), propiedades (`@property`) y validación en setters.

### 3.5. 🧩 Programación Orientada a Objetos y Polimorfismo
- Clases [`cliente.py`](cliente.py) (clase abstracta con `@abstractmethod calcularDescuento`), [`cliente_mayorista.py`](cliente_mayorista.py) (aplica 15% de descuento) y [`cliente_minorista.py`](cliente_minorista.py) (aplica 5% de descuento).
- Clases [`producto.py`](producto.py), [`producto_electronico.py`](producto_electronico.py) y [`marca.py`](marca.py) con herencia y sobrecarga de atributos.

### 3.6. 🧪 Suite de Pruebas Unitarias
- Implementada en [`test_semana7.py`](test_semana7.py) con **24 pruebas unitarias** ejecutadas con `pytest`:
  - 12 pruebas para la Cola FIFO (casos de borde, colas vacías, orden FIFO, tamaño, excepciones).
  - 9 pruebas para el Repositorio de Pedidos (atención de pedidos, estados, transiciones).
  - 3 pruebas para la capa de Persistencia JSON (guardado, recuperación y validación de archivos inexistentes).
- **Resultado:** 24 pruebas superadas exitosamente (100% de cobertura funcional).

---

## 4. Estructura y Organización del Código

```text
tienda/
│
├── persistencia.py          # Capa de persistencia: guarda y recupera datos en JSON (Examen)
├── main_gui.py              # Interfaz Gráfica con Flet (Catálogo + Cola de Pedidos)
│
├── cola.py                  # TDA Lineal: Cola FIFO manual con nodos enlazados (Semana 7)
├── pedido.py                # Clase Pedido con atributos privados y serialización
├── repository.py            # Patrón de diseño Repository para pedidos (Semana 7)
├── test_semana7.py          # 24 Pruebas unitarias automatizadas con pytest
├── demo_semana7.py          # Demostración del funcionamiento por consola
│
├── catalogo.py              # Gestión del catálogo con colecciones list + dict + set (Semana 5)
├── producto.py              # Clase base Producto (POO - Primer Parcial)
├── producto_electronico.py  # Clase derivada ProductoElectronico con garantía y marca
├── marca.py                 # Clase auxiliar Marca
├── cliente.py               # Clase base abstracta Cliente
├── cliente_mayorista.py     # Cliente con 15% de descuento (Polimorfismo)
├── cliente_minorista.py     # Cliente con 5% de descuento (Polimorfismo)
├── main.py                  # Demostración del primer parcial por consola
│
├── productos.json           # Archivo de persistencia (se genera automáticamente al iniciar)
├── pedidos.json             # Archivo de persistencia de pedidos (se genera automáticamente)
└── README.md                # Documentación del proyecto
```

---

## 5. Instrucciones de Instalación y Ejecución

### 5.1. Requisitos Previos
- Tener instalado **Python 3.10** o superior en el sistema.

### 5.2. Instalación de Dependencias
Abra su terminal o consola en la carpeta del proyecto y ejecute:

```bash
pip install flet==0.23.2 pytest
```

### 5.3. Ejecutar la Aplicación Gráfica (GUI Principal)
Para iniciar la interfaz interactiva con persistencia y cola de pedidos:

```bash
python main_gui.py
```

### 5.4. Ejecutar las Pruebas Unitarias
Para verificar el correcto funcionamiento del 100% de las pruebas automatizadas:

```bash
python -m pytest test_semana7.py -v
```
*Resultado esperado:* `24 passed`

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
1. **Generación automática:** Si la aplicación se inicia sin archivos JSON previos, el sistema detecta su ausencia y genera automáticamente `productos.json` y `pedidos.json` con datos iniciales de demostración.
2. **Registro de datos:** En la pestaña **Catálogo de Productos**, agregue un nuevo producto (ej. *"Tablet Lenovo"*, precio `$220`, stock `8`).
3. **Gestión en cola:** En la pestaña **Cola de Pedidos**, agregue un pedido para dicho producto y atienda uno de los pedidos pendientes mediante el botón FIFO.
4. **Cierre de aplicación:** Cierre la ventana de la interfaz gráfica.
5. **Comprobación en disco:** Abra los archivos `productos.json` y `pedidos.json` generados en el editor para constatar que los datos nuevos y modificados quedaron registrados en disco.
6. **Recuperación:** Vuelva a ejecutar `python main_gui.py` y observe cómo la aplicación recupera exactamente todo el estado anterior.
