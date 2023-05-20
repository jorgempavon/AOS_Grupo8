from database import db
from sqlalchemy import Date, Integer

class RelacionFT(db.Model):
    __tablename__="relacionFT"
    id=db.Column(Integer, primary_key=True, autoincrement=True)
    id_factura=db.Column(db.String(200))
    id_trabajo=db.Column(db.String(200))

    def __init__(self,id_factura,id_trabajo):
        self.id_factura=id_factura
        self.id_trabajo=id_trabajo

    def json(self):
        return{
            "Id":self.id,
            "id_factura": self.id_factura,
            "id_trabajo":self.id_trabajo
            }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def devolverFacturas(cls,trabajos):
        
        query=cls.query
        listaTrabajos=[trabajos]
        print(listaTrabajos)
        for i in listaTrabajos:
            print(i)
            query=query.filter_by(id_trabajo=i)
            
        print(query.all())
        return query.all()
    
    @classmethod
    def encontrar_PorIDfactura(cls,id_factura):
        return cls.query.filter_by(id_factura=id_factura).all()
