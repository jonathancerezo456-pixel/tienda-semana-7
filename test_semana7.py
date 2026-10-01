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
