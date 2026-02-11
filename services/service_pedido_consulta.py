from sqlalchemy.orm import Session
from models.models_pedidos import Pedido
from models.models_envios import Envio
from models.models_detalles_pedido import DetallePedido
from models.models_productos import Producto

from sqlalchemy.orm import Session
from models.models_pedidos import Pedido
from models.models_envios import Envio, EstadoEnvioEnum
from models.models_detalles_pedido import DetallePedido
from models.models_productos import Producto

def get_pedidos_no_entregados(db: Session, user_id: str):

    pedidos = (
        db.query(Pedido)
        .join(Envio, Envio.pedidos_id == Pedido.id)
        .filter(
            Pedido.usuarios_id == user_id,
            Pedido.activo == True,
            Envio.activo == True,
            Envio.estado != EstadoEnvioEnum.ENTREGADO,
            Envio.estado != EstadoEnvioEnum.CANCELADO
        )
        .all()
    )

    resultado = []

    for pedido in pedidos:
        envio = (
            db.query(Envio)
            .filter(
                Envio.pedidos_id == pedido.id,
                Envio.activo == True
            )
            .first()
        )

        detalles = (
            db.query(DetallePedido, Producto)
            .join(Producto, Producto.id == DetallePedido.productos_id)
            .filter(
                DetallePedido.pedidos_id == pedido.id,
                DetallePedido.activo == True
            )
            .all()
        )

        resultado.append({
            "pedido": {
                "id": pedido.id,
                "fecha": pedido.fecha,
                "importe_productos": float(pedido.importe_productos),
                "importe_envio": float(pedido.importe_envio),
            },
            "envio": {
                "estado": envio.estado,
                "numero_seguimiento": envio.numero_seguimiento,
            } if envio else None,
            "productos": [
                {
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "marca": producto.marca,
                    "color": producto.color,
                    "sku": producto.sku,
                    "imagen": producto.url_producto,
                    "precio_unitario": float(detalle.precio),
                    "cantidad": detalle.cantidad,
                    "subtotal": float(detalle.precio * detalle.cantidad)
                }
                for detalle, producto in detalles
            ]
        })

    return resultado

def get_pedido_completo(db: Session, pedido_id: str, user_id: str):
    pedido = db.query(Pedido).filter(
        Pedido.id == pedido_id,
        Pedido.usuarios_id == user_id,
        Pedido.activo == True
    ).first()

    if not pedido:
        return None

    envio = db.query(Envio).filter(
        Envio.pedidos_id == pedido_id,
        Envio.activo == True
    ).first()

    detalles = db.query(
        DetallePedido,
        Producto
    ).join(
        Producto, Producto.id == DetallePedido.productos_id
    ).filter(
        DetallePedido.pedidos_id == pedido_id,
        DetallePedido.activo == True
    ).all()

    return {
        "pedido": {
            "id": pedido.id,
            "numero": pedido.numero,
            "fecha": pedido.fecha,
            "importe_productos": float(pedido.importe_productos),
            "importe_envio": float(pedido.importe_envio),
        },
        "envio": None if not envio else {
            "estado": envio.estado,
            "numero_seguimiento": envio.numero_seguimiento,
            "fecha_entrega": envio.fecha_entrega
        },
        "productos": [
            {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "marca": producto.marca,
                "color": producto.color,
                "sku": producto.sku,
                "imagen": producto.url_producto,
                "precio_unitario": float(detalle.precio),
                "cantidad": detalle.cantidad,
                "subtotal": float(detalle.precio * detalle.cantidad)
            }
            for detalle, producto in detalles
        ]
    }
