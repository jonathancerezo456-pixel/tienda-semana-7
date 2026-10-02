"""
persistencia.py — Capa de Persistencia de Datos (JSON)
=======================================================
Gestiona el almacenamiento y recuperación de información en formato JSON
para el Catálogo de Productos y el Repositorio de Pedidos.
Cumple con el requisito obligatorio de persistencia de datos del proyecto.
"""

import json
import os
from producto import Producto
from producto_electronico import ProductoElectronico
from marca import Marca
from pedido import Pedido

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_PRODUCTOS = os.path.join(BASE_DIR, "productos.json")
ARCHIVO_PEDIDOS   = os.path.join(BASE_DIR, "pedidos.json")


class GestorPersistencia:
    """Clase utilitaria para guardar y cargar datos de la tienda en archivos JSON."""

    @staticmethod
    def guardar_catalogo(catalogo, ruta=ARCHIVO_PRODUCTOS) -> bool:
        """
        Serializa todos los productos del catálogo y los guarda en un archivo JSON.
        """
        try:
            datos = []
            for p in catalogo.listar():
                es_electronico = isinstance(p, ProductoElectronico)
                item = {
                    "nombre": p.get_nombre(),
                    "precio": p.get_precio(),
                    "cantidad": p.get_cantidad(),
                    "es_electronico": es_electronico,
                }
                if es_electronico:
                    item["garantia"] = p.get_garantia()
                    item["marca"] = p.get_marca().get_nombre()
                datos.append(item)

            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[Error Persistencia] No se pudo guardar el catálogo: {e}")
            return False

    @staticmethod
    def cargar_catalogo(catalogo, ruta=ARCHIVO_PRODUCTOS) -> bool:
        """
        Lee el archivo JSON y reconstruye los objetos Producto y ProductoElectronico
        en el catálogo. Retorna True si se cargaron datos con éxito.
        """
        if not os.path.exists(ruta):
            return False

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)

            for item in datos:
                if item.get("es_electronico"):
                    marca_obj = Marca(item.get("marca", "Generica"))
                    p = ProductoElectronico(
                        item["nombre"],
                        float(item["precio"]),
                        int(item["cantidad"]),
                        int(item.get("garantia", 1)),
                        marca_obj
                    )
                else:
                    p = Producto(
                        item["nombre"],
                        float(item["precio"]),
                        int(item["cantidad"])
                    )
                catalogo.agregar(p)
            return True
        except Exception as e:
            print(f"[Error Persistencia] No se pudo cargar el catálogo: {e}")
            return False

    @staticmethod
    def guardar_pedidos(repository, ruta=ARCHIVO_PEDIDOS) -> bool:
        """
        Guarda los pedidos en cola (pendientes) y los ya procesados en un archivo JSON.
        """
        try:
            datos = {
                "pendientes": [p.to_dict() for p in repository.listar_pendientes()],
                "procesados": [p.to_dict() for p in repository.listar_procesados()]
            }
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[Error Persistencia] No se pudieron guardar los pedidos: {e}")
            return False

    @staticmethod
    def cargar_pedidos(repository, ruta=ARCHIVO_PEDIDOS) -> bool:
        """
        Recupera pedidos pendientes (encolándolos en la Cola FIFO) y pedidos procesados
        desde un archivo JSON.
        """
        if not os.path.exists(ruta):
            return False

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)

            for item in datos.get("pendientes", []):
                p = Pedido.from_dict(item)
                repository.agregar_pedido(p)

            for item in datos.get("procesados", []):
                p = Pedido.from_dict(item)
                repository.restaurar_procesado(p)
            return True
        except Exception as e:
            print(f"[Error Persistencia] No se pudieron cargar los pedidos: {e}")
            return False

    @staticmethod
    def cargar_demo_inicial(catalogo):
        """Carga datos de prueba predeterminados en caso de primer inicio."""
        marca_samsung  = Marca("Samsung")
        marca_sony     = Marca("Sony")
        marca_generica = Marca("Generica")

        catalogo.agregar(ProductoElectronico("Televisor", 500.00, 5,  2, marca_samsung))
        catalogo.agregar(ProductoElectronico("Celular",   350.00, 12, 1, marca_sony))
        catalogo.agregar(Producto("Arroz",   2.50,  100))
        catalogo.agregar(Producto("Aceite",  3.75,   80))
        catalogo.agregar(ProductoElectronico("Audifonos", 45.00, 30, 1, marca_generica))


# Funciones de conveniencia compatibles
guardar_catalogo = GestorPersistencia.guardar_catalogo
cargar_catalogo  = GestorPersistencia.cargar_catalogo
guardar_pedidos   = GestorPersistencia.guardar_pedidos
cargar_pedidos    = GestorPersistencia.cargar_pedidos
