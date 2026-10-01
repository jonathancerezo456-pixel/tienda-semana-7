# Tienda - Semana 7: Patrones de Diseno, Testing Unitario y TDA Lineales

**Estudiante:** Jonathan Andres Cerezo Alava
**Materia:** Programacion Estructurada
**Actividad:** Semana 7

---

## Descripcion del proyecto

Se implemento un sistema de gestion de pedidos para la tienda usando una **Cola (Queue)**
como tipo de dato abstracto lineal, administrada a traves del patron de diseno **Repository**.

### Problema seleccionado

Cuando un cliente hace un pedido en la tienda, debe ser atendido en el mismo orden en que llego
(el primero en llegar es el primero en ser atendido). Esto es un problema tipico de una **Cola FIFO**.

### Estructura de datos: Cola (Queue)

La cola fue implementada **manualmente** con nodos enlazados, sin usar `queue.Queue` ni `collections.deque`.

| Operacion        | Metodo         | Descripcion                                 |
|------------------|----------------|---------------------------------------------|
| Agregar          | `encolar()`    | Agrega un elemento al final de la cola      |
| Eliminar         | `desencolar()` | Elimina y retorna el elemento del frente    |
| Consultar        | `frente()`     | Ve el siguiente sin eliminarlo              |
| Verificar vacia  | `esta_vacia()` | Retorna True si no hay elementos            |
| Cantidad         | `tamano()`     | Retorna el numero de elementos en la cola   |

### Patron Repository

`PedidoRepository` separa el acceso a los datos de la logica principal. La aplicacion no
manipula la Cola directamente, sino a traves de metodos como `agregar_pedido()`,
`procesar_siguiente()` y `ver_siguiente()`.

---

## Archivos del proyecto

```
tienda/
|-- cola.py              # Cola FIFO manual con nodos enlazados (Semana 7)
|-- pedido.py            # Clase Pedido con encapsulacion
|-- repository.py        # Patron Repository para gestionar pedidos
|-- demo_semana7.py      # Demostracion por consola
|-- test_semana7.py      # 21 pruebas unitarias con pytest
|
|-- catalogo.py          # Semana 5: Colecciones list + dict + set
|-- main_gui.py          # Semana 6: Interfaz grafica con Flet
|-- producto.py
|-- producto_electronico.py
|-- marca.py
|-- cliente.py
|-- cliente_mayorista.py
|-- cliente_minorista.py
|-- README.md
```

---

## Instalacion de dependencias

```bash
pip install pytest
pip install flet==0.23.2
```

---

## Ejecutar la demo (Semana 7)

```bash
cd "Programacion Estructurada\tienda"
python demo_semana7.py
```

---

## Ejecutar las pruebas unitarias

```bash
python -m pytest test_semana7.py -v
```

Resultado esperado: **21 passed**

---

## Ejecutar la interfaz grafica (Semana 6)

```bash
python main_gui.py
```
