from Facturas_trabajos.model_relacion.modelRelacion.modeRelacionFT import RelacionFT
from database import db
from sqlalchemy import Date, Integer
from flask import current_app


class Factura(db.Model):
    
    __tablename__="factura"
    id_factura=db.Column(db.String(200),primary_key=True)
    estado=db.Column(db.String(200))
    VIN_coche=db.Column(db.String(200))
    Id_cliente=db.Column(db.String(200))
    fecha_factura=db.Column(Date)
    importe_total=db.Column(Integer)
    

    
   
    def __init__(self,id_factura,estado,VIN_coche,Id_cliente,fecha_factura,importe_total):
        self.id_factura=id_factura
        self.estado=estado
        self.VIN_coche=VIN_coche
        self.Id_cliente=Id_cliente
        self.fecha_factura=fecha_factura
        self.importe_total=importe_total

    def json(self):
        fechaSerializable=self.fecha_factura.isoformat()
        importeSerializable=str(self.importe_total)
        listaTrabajos=[]
        respRelacionFT:RelacionFT=RelacionFT.encontrar_PorIDfactura(self.id_factura)
        for i in respRelacionFT:
            listaTrabajos.append(i.json()["id_trabajo"])
            
        linksTrabajos=[]
        for i in listaTrabajos:
            linksTrabajos.append({"href":f'http://127.0.0.1:5000/api/v1/trabajos/{i}',
                    "rel":'trabajos_get trabajos_put trabajos_delete trabajos_options'})


        return {"factura":{
            "Id_factura":self.id_factura,
            "Estado": self.estado,
            "VIN_coche":self.VIN_coche,
            "Id_cliente":self.Id_cliente,
            "trabajos":listaTrabajos,
            "Fecha factura":fechaSerializable,
            "Importe total":importeSerializable
            },
            "links":{
                "parent":{ "href":'http://127.0.0.1:5000/api/v1/facturas',
                            "rel":'factura_post factura_cget factura_coptions'},
                
                "self":{ "href": f'http://127.0.0.1:5000/api/v1/facturas/{self.id_factura}',
                          "rel":"factura_get factura_delete factura_put factura_options" },

                "cliente":{ "href": f'http://127.0.0.1:5000/api/v1/clientes/{self.Id_cliente}',
                          "rel":"cliente_get cliente_put cliente_delete cliente_options"},

                "vehiculo":{"href": f'http://127.0.0.1:5000/api/v1/vehiculos/{self.VIN_coche}',
                          "rel":"vehiculo_get vehiculo_put vehiculo_delete vehiculo_options"},
                
                "trabajos":linksTrabajos
                
                }
            }
    
    @classmethod
    def find(cls,estado,VIN_coche,fecha_factura,Id_cliente,trabajos,intervalo_inferior,intervalo_superior,order,ordering,page):
        
        query=cls.query
        if trabajos!= None:
            relacionFT:RelacionFT=RelacionFT.devolverFacturas(trabajos)
            if relacionFT!=None:
                lista_idsFacturas=[]
                for i in relacionFT:
                    lista_idsFacturas.append( i.json()["id_factura"])
                    print(i)
                query=query.filter(cls.id_factura.in_(lista_idsFacturas))
        if estado!=None:
            query=cls.query.filter_by(estado=estado)
        if VIN_coche!=None:
            query=query.filter_by(VIN_coche=VIN_coche)
        if fecha_factura!=None:
            query=query.filter_by(fecha_factura=fecha_factura)
        if Id_cliente!=None:
            query=query.filter_by(Id_cliente=Id_cliente)
        
        if order!=None:
            if order=="id_factura":
                if ordering=="ASC":
                    query=query.order_by(cls.id_factura.asc())
                elif ordering=="DESC":
                    query=query.order_by(cls.id_factura.desc())
                else:
                    query=query=query.order_by(cls.id_factura)
            else:
                if ordering=="ASC":
                    query=query.order_by(cls.fecha_factura.asc())
                elif ordering=="DESC":
                    query=query.order_by(cls.fecha_factura.desc())
                else:
                    query=query.order_by(cls.fecha_factura)
        
        if intervalo_inferior!=None and intervalo_superior!=None:
            query=query.filter(cls.importe_total.between(intervalo_inferior,intervalo_superior))
        elif intervalo_inferior!=None:
            query=query.filter(cls.importe_total>=intervalo_inferior)
        elif intervalo_superior!=None:
            query=query.filter(cls.importe_total<=intervalo_superior)
            
                
        if page!=None:
            print("HOLA")
        
        return query.all()
        
    
    @classmethod
    def find_byid_factura(cls,id_factura):
        
        return cls.query.filter_by(id_factura=id_factura).first()
    
    def save_to_db(self):
        
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        
        db.session.delete(self)
        db.session.commit()
