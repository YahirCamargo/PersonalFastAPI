from sqlalchemy import Column, DateTime, Numeric,ForeignKey,String
from sqlalchemy.dialects.mysql import SMALLINT, CHAR, TINYINT,TEXT
from db.database import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(SMALLINT(unsigned=True),nullable=False,primary_key=True,autoincrement=True)
    nombre = Column(String(60),nullable=False)
    precio = Column(Numeric(7,2), nullable=False,index=True)
    sku = Column(CHAR(15), nullable=False,unique=True)
    color = Column(String(15),nullable=False)
    marca = Column(String(20),nullable=False,index=True)
    descripcion = Column(TEXT,nullable=True)
    peso = Column(Numeric(5,1),nullable=False)
    alto = Column(Numeric(5,1),nullable=False,default=0.0)
    ancho = Column(Numeric(5,1),nullable=False,default=0.0)
    profundidad = Column(Numeric(5,1),nullable=False,default=0.0)
    categorias_id = Column(
        TINYINT(unsigned=True),
        ForeignKey("categorias.id"),
        index=True,
        nullable=False
    )
    url_producto = Column(String(255),nullable=False)


"""
CREATE TABLE `productos` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) NOT NULL,
  `precio` decimal(7,2) NOT NULL,
  `sku` char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Código único del producto',
  `color` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'desconocido',
  `marca` varchar(20) NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `peso` decimal(5,1) NOT NULL COMMENT 'En kilogramos',
  `alto` decimal(5,1) NOT NULL DEFAULT '0.0',
  `ancho` decimal(5,1) NOT NULL DEFAULT '0.0',
  `profundidad` decimal(5,1) NOT NULL DEFAULT '0.0',
  `categorias_id` tinyint unsigned NOT NULL,
  `url_producto` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku_UNIQUE` (`sku`),
  KEY `idx_marca` (`marca`),
  KEY `idx_precio` (`precio`),
  KEY `fk_productos_categorias_idx` (`categorias_id`),
  FULLTEXT KEY `idx_nombre_desc_fulltext` (`nombre`,`descripcion`),
  CONSTRAINT `fk_productos_categorias` FOREIGN KEY (`categorias_id`) REFERENCES `categorias` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Productos del sistema (InnoDB para consistencia de inventario)';
/*!40101 SET character_set_client = @saved_cs_client */;
"""