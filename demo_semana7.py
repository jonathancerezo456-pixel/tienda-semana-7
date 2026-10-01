from cola import Cola
from pedido import Pedido
from repository import PedidoRepository


def main():
    print("=" * 55)
    print("  TIENDA - Sistema de Pedidos (Semana 7)")
    print("  Cola FIFO + Patron Repository")
    print("=" * 55)

    repo = PedidoRepository()

    # Registrar pedidos en la cola
    pedidos = [
        Pedido("Jonathan Cerezo", "Laptop HP",   1, 1200.00),
        Pedido("Maria Lopez",     "Mouse USB",   3,   15.50),
        Pedido("Carlos Ruiz",     "Teclado",     2,   45.00),
        Pedido("Ana Torres",      "Monitor 24",  1,  350.00),
    ]

    print("\n-- Registrando pedidos en la cola --")
    for p in pedidos:
        repo.agregar_pedido(p)
        print(f"  + {p}")

    print(f"\nPedidos pendientes : {repo.total_pendientes()}")
    print(f"Siguiente a atender: {repo.ver_siguiente()}")

    print("\n-- Procesando pedidos (orden FIFO) --")
    while repo.hay_pendientes():
        procesado = repo.procesar_siguiente()
        print(f"  [OK] {procesado}")

    print(f"\nTotal procesados: {repo.total_procesados()}")
    print(f"Cola vacia      : {not repo.hay_pendientes()}")
    print("\nPedidos atendidos:")
    for p in repo.listar_procesados():
        print(f"  {p}")


if __name__ == "__main__":
    main()
