# Proyecto Tienda - Catálogo de Productos
**Materia:** Programación Estructurada  
**Estudiante:** Jonathan Andrés Cerezo Álava  
**Actividad:** Semanas 5 y 6  

---

## Descripción
Este proyecto es una aplicación en Python para gestionar el catálogo de una tienda. Integra conceptos de programación orientada a objetos (clases, herencia, encapsulación y polimorfismo) desarrollados en semanas anteriores, junto con los nuevos temas:
- **Semana 5:** Manejo de colecciones de datos (`list`, `dict` y `set`) para implementar operaciones CRUD.
- **Semana 6:** Creación de una interfaz gráfica de usuario (GUI) interactiva usando la librería **Flet**.

---

## Requisitos e Instalación

Para ejecutar la aplicación se necesita tener instalado Python (versión 3.10 o superior) y la librería `flet`:

```bash
pip install flet
```

---

##  Cómo ejecutar el programa

### 1. Interfaz Gráfica (Semana 6)
Para abrir la aplicación visual:
```bash
python main_gui.py
```

### 2. Prueba por Consola (Semana 5 y anteriores)
Para ver la demostración por terminal del catálogo y polimorfismo:
```bash
python main.py
```

---

##  Estructura de Archivos

- `producto.py`: Clase base con atributos privados (`__nombre`, `__precio`, `__cantidad`) y métodos getters/setters.
- `producto_electronico.py`: Clase hija que hereda de `Producto` y añade `marca` y `garantía (años)`.
- `marca.py`: Clase auxiliar para representar la marca del producto.
- `cliente.py`: Clase abstracta que define el método para calcular descuentos.
- `cliente_mayorista.py` / `cliente_minorista.py`: Clases que aplican diferentes porcentajes de descuento (polimorfismo).
- `catalogo.py`: **(Semana 5)** Contiene la lógica del catálogo utilizando tres colecciones:
  - `list`: Mantiene el orden en que se agregan los productos para listarlos o recorrerlos.
  - `dict`: Permite búsquedas rápidas por nombre en tiempo $O(1)$.
  - `set`: Evita el ingreso de productos con nombres duplicados.
- `main_gui.py`: **(Semana 6)** Interfaz gráfica desarrollada con Flet, con tabla de datos, validaciones y botones CRUD.

---

##  Funcionalidades de la Interfaz Gráfica
1. **Agregar producto:** Permite ingresar nombre, precio, cantidad y marca. Si se marca la casilla "Es electrónico", habilita el campo de garantía en años.
2. **Buscar:** Busca coincidencias por nombre dentro del catálogo y filtra la tabla.
3. **Actualizar:** Modifica precio y stock del producto seleccionado.
4. **Eliminar:** Quita un producto de todas las colecciones tras confirmar la acción.
5. **Listar todos:** Vuelve a cargar todos los registros existentes en la tabla.
