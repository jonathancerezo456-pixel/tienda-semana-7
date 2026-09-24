"""
catalogo.py — Semana 5: Colecciones
=====================================
Usa las clases existentes (Producto, ProductoElectronico, Marca)
tal como están en la carpeta tienda.

Tres colecciones de Python:
  • list  → _lista       : guarda el orden de inserción, permite iterar
  • dict  → _indice      : búsqueda rápida O(1) por nombre (clave única)
  • set   → _nombres     : evita registros duplicados
"""

from producto import Producto
from producto_electronico import ProductoElectronico
from marca import Marca


class Catalogo:
    """Catálogo de productos que usa list, dict y set."""

    def __init__(self):
        # list — permite recorrer y mantiene el orden
        self._lista = []

        # dict — acceso directo por nombre del producto
        self._indice = {}

        # set — evita duplicados (dos productos con el mismo nombre)
        self._nombres = set()

    # ── C — Crear ─────────────────────────────────────────────────────────────
    def agregar(self, producto) -> bool:
        """
        Agrega un producto al catálogo.
        Retorna True si se agregó, False si ya existía (duplicado).
        El SET es quien detecta duplicados en O(1).
        """
        clave = producto.get_nombre().lower()

        if clave in self._nombres:
            return False  # duplicado — el set lo detecta

        self._lista.append(producto)          # list
        self._indice[clave] = producto        # dict
        self._nombres.add(clave)              # set
        return True

    # ── R — Leer ──────────────────────────────────────────────────────────────
    def buscar(self, nombre: str):
        """
        Busca un producto por nombre exacto.
        Usa el DICT para acceso O(1).
        Retorna el producto o None si no existe.
        """
        return self._indice.get(nombre.lower(), None)

    def buscar_parcial(self, texto: str) -> list:
        """Busca productos cuyo nombre contenga el texto (sin importar mayúsculas)."""
        texto = texto.lower()
        return [p for p in self._lista if texto in p.get_nombre().lower()]

    def listar(self) -> list:
        """Retorna todos los productos (usa la LIST para mantener el orden)."""
        return list(self._lista)

    # ── U — Actualizar ────────────────────────────────────────────────────────
    def actualizar(self, nombre: str, nuevo_nombre: str = None,
                   nuevo_precio: float = None, nueva_cantidad: int = None) -> bool:
        """
        Actualiza los datos de un producto existente.
        Retorna True si se actualizó, False si no se encontró.
        """
        producto = self.buscar(nombre)
        if producto is None:
            return False

        clave_vieja = nombre.lower()

        if nuevo_nombre and nuevo_nombre.strip():
            nueva_clave = nuevo_nombre.lower()
            # Actualizar las tres colecciones con la nueva clave
            self._indice.pop(clave_vieja)
            self._nombres.discard(clave_vieja)
            producto.set_nombre(nuevo_nombre)
            self._indice[nueva_clave] = producto
            self._nombres.add(nueva_clave)

        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)

        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)

        return True

    # ── D — Eliminar ──────────────────────────────────────────────────────────
    def eliminar(self, nombre: str) -> bool:
        """
        Elimina un producto del catálogo (de las tres colecciones).
        Retorna True si se eliminó, False si no existía.
        """
        clave = nombre.lower()
        if clave not in self._nombres:
            return False

        producto = self._indice.pop(clave)   # dict
        self._nombres.discard(clave)          # set
        self._lista.remove(producto)          # list
        return True

    # ── Utilidades ────────────────────────────────────────────────────────────
    def total(self) -> int:
        return len(self._lista)

    def __str__(self) -> str:
        if not self._lista:
            return "El catálogo está vacío."
        lineas = ["=== Catálogo ==="]
        for p in self._lista:
            tipo = type(p).__name__
            lineas.append(f"  [{tipo}] {p.get_nombre()} — ${p.get_precio()} — Stock: {p.get_cantidad()}")
        return "\n".join(lineas)
