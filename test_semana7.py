import pytest
from cola import Cola
from pedido import Pedido
from repository import PedidoRepository


# ============================================================
# PRUEBAS DE LA COLA
# ============================================================

class TestCola:

    def test_cola_nueva_esta_vacia(self):
        """Una cola recien creada debe estar vacia."""
        c = Cola()
        assert c.esta_vacia() is True

    def test_tamano_inicial_es_cero(self):
        """El tamano inicial debe ser 0."""
        assert Cola().tamano() == 0

    def test_encolar_aumenta_tamano(self):
        """Encolar un elemento debe aumentar el tamano."""
        c = Cola()
        c.encolar("A")
        assert c.tamano() == 1
        assert c.esta_vacia() is False

    def test_encolar_varios_elementos(self):
        """Encolar varios elementos refleja el tamano correcto."""
        c = Cola()
        c.encolar("A"); c.encolar("B"); c.encolar("C")
        assert c.tamano() == 3

    def test_frente_no_elimina_elemento(self):
        """frente() debe retornar el primer elemento sin eliminarlo."""
        c = Cola()
        c.encolar("Primero")
        c.encolar("Segundo")
        assert c.frente() == "Primero"
        assert c.tamano() == 2

    def test_orden_fifo(self):
        """La cola debe mantener orden FIFO: primero en entrar, primero en salir."""
        c = Cola()
        for i in [1, 2, 3, 4, 5]:
            c.encolar(i)
        resultado = [c.desencolar() for _ in range(5)]
        assert resultado == [1, 2, 3, 4, 5]

    def test_desencolar_reduce_tamano(self):
        """desencolar() debe reducir el tamano en 1."""
        c = Cola()
        c.encolar("X"); c.encolar("Y")
        c.desencolar()
        assert c.tamano() == 1

    def test_desencolar_hasta_vacia(self):
        """Desencolar todos los elementos debe dejar la cola vacia."""
        c = Cola()
        c.encolar(1); c.encolar(2)
        c.desencolar(); c.desencolar()
        assert c.esta_vacia() is True

    def test_desencolar_cola_vacia_lanza_error(self):
        """desencolar() en cola vacia debe lanzar IndexError."""
        with pytest.raises(IndexError):
            Cola().desencolar()

    def test_frente_cola_vacia_lanza_error(self):
        """frente() en cola vacia debe lanzar IndexError."""
        with pytest.raises(IndexError):
            Cola().frente()

    def test_listar_orden_correcto(self):
        """listar() debe retornar los elementos en orden frente->final."""
        c = Cola()
        c.encolar("p1"); c.encolar("p2"); c.encolar("p3")
        assert c.listar() == ["p1", "p2", "p3"]

    def test_len_retorna_tamano(self):
        """len(cola) debe retornar el tamano correcto."""
        c = Cola()
        c.encolar("a"); c.encolar("b")
        assert len(c) == 2


# ============================================================
# PRUEBAS DEL REPOSITORY
# ============================================================

class TestPedidoRepository:

    def setup_method(self):
        """Se ejecuta antes de cada prueba."""
        Pedido._contador = 1
        self.repo = PedidoRepository()

    def test_repositorio_nuevo_sin_pedidos(self):
        """Un repository nuevo no debe tener pedidos."""
        assert self.repo.hay_pendientes() is False
        assert self.repo.total_pendientes() == 0

    def test_agregar_pedido_aumenta_pendientes(self):
        """Agregar un pedido debe aparecer en los pendientes."""
        self.repo.agregar_pedido(Pedido("Juan", "Laptop", 1, 1200.0))
        assert self.repo.total_pendientes() == 1
        assert self.repo.hay_pendientes() is True

    def test_ver_siguiente_no_elimina(self):
        """ver_siguiente() no debe eliminar el pedido de la cola."""
        p = Pedido("Ana", "Mouse", 2, 25.0)
        self.repo.agregar_pedido(p)
        self.repo.ver_siguiente()
        assert self.repo.total_pendientes() == 1

    def test_procesar_cambia_estado_a_procesado(self):
        """procesar_siguiente() debe cambiar el estado del pedido a 'procesado'."""
        self.repo.agregar_pedido(Pedido("Carlos", "Teclado", 1, 45.0))
        procesado = self.repo.procesar_siguiente()
        assert procesado.estado == "procesado"

    def test_procesar_reduce_pendientes(self):
        """Procesar debe mover el pedido de pendientes a procesados."""
        self.repo.agregar_pedido(Pedido("Luis", "Monitor", 1, 300.0))
        self.repo.procesar_siguiente()
        assert self.repo.total_pendientes() == 0
        assert self.repo.total_procesados() == 1

    def test_orden_atencion_fifo(self):
        """Los pedidos deben procesarse en el orden en que llegaron."""
        for nombre in ["Cliente1", "Cliente2", "Cliente3"]:
            self.repo.agregar_pedido(Pedido(nombre, "ProductoX", 1, 10.0))
        assert self.repo.procesar_siguiente().cliente == "Cliente1"
        assert self.repo.procesar_siguiente().cliente == "Cliente2"
        assert self.repo.procesar_siguiente().cliente == "Cliente3"

    def test_total_pedido_precio_por_cantidad(self):
        """El total del pedido debe ser precio * cantidad."""
        p = Pedido("Maria", "Monitor", 2, 300.0)
        assert p.total == 600.0

    def test_procesar_sin_pedidos_lanza_error(self):
        """Procesar cuando no hay pedidos debe lanzar IndexError."""
        with pytest.raises(IndexError):
            self.repo.procesar_siguiente()

    def test_listar_procesados(self):
        """listar_procesados() debe retornar los pedidos atendidos."""
        self.repo.agregar_pedido(Pedido("Luis",  "Silla", 1, 150.0))
        self.repo.agregar_pedido(Pedido("Rosa",  "Mesa",  1, 200.0))
        self.repo.procesar_siguiente()
        procesados = self.repo.listar_procesados()
        assert len(procesados) == 1
        assert procesados[0].cliente == "Luis"


# ============================================================
# PRUEBAS DE PERSISTENCIA (JSON)
# ============================================================

from catalogo import Catalogo
from producto import Producto
from producto_electronico import ProductoElectronico
from marca import Marca
from persistencia import GestorPersistencia


class TestPersistencia:

    def test_guardar_y_cargar_catalogo(self, tmp_path):
        """Debe guardar y recuperar productos normales y electronicos correctamente."""
        archivo = str(tmp_path / "test_productos.json")
        cat_origen = Catalogo()
        cat_origen.agregar(Producto("Arroz", 2.5, 50))
        cat_origen.agregar(ProductoElectronico("TV 4K", 600.0, 5, 2, Marca("LG")))

        # Guardar
        assert GestorPersistencia.guardar_catalogo(cat_origen, archivo) is True

        # Cargar en un catalogo nuevo
        cat_destino = Catalogo()
        assert GestorPersistencia.cargar_catalogo(cat_destino, archivo) is True
        assert cat_destino.total() == 2

        prod1 = cat_destino.buscar("Arroz")
        assert prod1 is not None
        assert prod1.get_precio() == 2.5
        assert prod1.get_cantidad() == 50

        prod2 = cat_destino.buscar("TV 4K")
        assert prod2 is not None
        assert isinstance(prod2, ProductoElectronico)
        assert prod2.get_garantia() == 2
        assert prod2.get_marca().get_nombre() == "LG"

    def test_guardar_y_cargar_pedidos(self, tmp_path):
        """Debe guardar y recuperar pedidos pendientes y procesados respetando el orden FIFO."""
        archivo = str(tmp_path / "test_pedidos.json")
        repo_origen = PedidoRepository()
        p1 = Pedido("Cliente 1", "Laptop", 1, 1000.0)
        p2 = Pedido("Cliente 2", "Mouse", 2, 25.0)
        repo_origen.agregar_pedido(p1)
        repo_origen.agregar_pedido(p2)
        repo_origen.procesar_siguiente()  # p1 pasa a procesado, p2 queda pendiente

        assert GestorPersistencia.guardar_pedidos(repo_origen, archivo) is True

        repo_destino = PedidoRepository()
        assert GestorPersistencia.cargar_pedidos(repo_destino, archivo) is True
        assert repo_destino.total_pendientes() == 1
        assert repo_destino.total_procesados() == 1

        siguiente = repo_destino.ver_siguiente()
        assert siguiente.cliente == "Cliente 2"
        assert siguiente.producto == "Mouse"

    def test_cargar_archivo_inexistente_retorna_false(self, tmp_path):
        """Si el archivo no existe, debe retornar False sin lanzar excepcion."""
        archivo = str(tmp_path / "inexistente.json")
        cat = Catalogo()
        assert GestorPersistencia.cargar_catalogo(cat, archivo) is False
        repo = PedidoRepository()
        assert GestorPersistencia.cargar_pedidos(repo, archivo) is False
