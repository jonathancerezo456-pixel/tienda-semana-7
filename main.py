from producto import Producto
from producto_electronico import ProductoElectronico
from marca import Marca
from cliente_mayorista import ClienteMayorista
from cliente_minorista import ClienteMinorista

# Producto normal
producto1 = Producto("Arroz", 2.50, 10)

print("Producto normal:")
print("Nombre:", producto1.get_nombre())
print("Precio:", producto1.get_precio())
print("Cantidad:", producto1.get_cantidad())

print("--------------------")

# Marca
marca1 = Marca("Samsung")

# Producto electrónico
producto2 = ProductoElectronico("Televisor", 500, 5, 2, marca1)

print("Producto electrónico:")
print("Nombre:", producto2.get_nombre())
print("Precio:", producto2.get_precio())
print("Cantidad:", producto2.get_cantidad())
print("Garantía:", producto2.get_garantia(), "años")
print("Marca:", producto2.get_marca().get_nombre())

print("--------------------")

# Demostración de Polimorfismo con Clientes
cliente_mayorista = ClienteMayorista("Cliente Mayorista")
cliente_minorista = ClienteMinorista("Cliente Minorista")

clientes = [cliente_mayorista, cliente_minorista]
total_ejemplo = 100

print("Prueba de Polimorfismo (Descuentos):")
for cliente in clientes:
    total_con_descuento = cliente.calcularDescuento(total_ejemplo)
    print("Nombre del cliente:", cliente.get_nombre())
    print("Total original:", total_ejemplo)
    print("Total con descuento:", total_con_descuento)
    print("--------------------")
