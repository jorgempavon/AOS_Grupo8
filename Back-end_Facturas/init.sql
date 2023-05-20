CREATE TABLE factura (
    id_factura VARCHAR(200) NOT NULL,
    estado VARCHAR(200),
    VIN_coche VARCHAR(200) NOT NULL,
    Id_cliente VARCHAR(200) NOT NULL,
    fecha_factura DATE,
    importe_total DECIMAL(10, 2),
    PRIMARY KEY (id_factura)
);

CREATE TABLE relacionFT (
    id INT AUTO_INCREMENT,
    id_factura VARCHAR(200) NOT NULL,
    id_trabajo VARCHAR(200) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_factura) REFERENCES factura(id_factura) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT IGNORE INTO factura
    (id_factura, estado, VIN_coche, Id_cliente, fecha_factura, importe_total)
    VALUES
    ('2023-0000', 'Emitida', 'RT3DKGNF0KX480214', '09975463Y', '2023-05-16', 233.00);

INSERT IGNORE INTO relacionFT
    (id_factura, id_trabajo)
    VALUES
    ('2023-0000', 'T222');

INSERT IGNORE INTO factura
    (id_factura, estado, VIN_coche, Id_cliente, fecha_factura, importe_total)
    VALUES
    ('2023-0001', 'Pagada', 'RT3DKGNF0KX480214', '04975462Y', '2023-05-31', 500.00);

INSERT IGNORE INTO relacionFT
    (id_factura, id_trabajo)
    VALUES
    ('2023-0001', 'T222');

INSERT IGNORE INTO relacionFT
    (id_factura, id_trabajo)
    VALUES
    ('2023-0001', 'T555');