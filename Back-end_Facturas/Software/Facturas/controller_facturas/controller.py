import hashlib
import random

from flask import make_response
from Facturas.model_facturas.model import *
from Facturas_trabajos.model_relacion.modelRelacion.modeRelacionFT import RelacionFT

from helpers.HTTP_Problems import *

class FacturasController():

    def busqueda(estado,VIN_coche,fecha_factura,Id_cliente,trabajos,intervalo_inferior,intervalo_superior,order,ordering,page):
        respModel:Factura=Factura.find(estado,VIN_coche,fecha_factura,Id_cliente,trabajos,intervalo_inferior,intervalo_superior,order,ordering,page)
        listaObj=[]
        for i in respModel:
            listaObj.append(i.json())
        
       
        
        if page==None:
            page=1
            prevPage="selfPage"
            prevNumber=page
        else:
            prevPage="prevPage"
            prevNumber=int(page)-1


        return {
            "facturas": listaObj,
            "links":{
                f"{prevPage}": {
                    "href": f"https://www.tallermecanico.com/api/v1/facturas?page={prevNumber}",
                    "rel": "prevpage"
                },
                "nextPage": {
                    "href": f"https://www.tallermecanico.com/api/v1/facturas?page={int(page)+1}",
                    "rel": "nextpage"
                }
                
                }
            }
    
    def mock_Cliente(id_cliente):
        return True
        return random.choice([True, False])

    def mock_Vehiculo(VIN_coche): 
        return True
        return random.choice([True,False])
    

    def mock_Trabajos(trabajos):
        return True
        return random.choice([True,False])


    def calculoImporte():
        return round(random.uniform(1, 1000), 2)

    def insercion(body):
        idExistente:Factura=Factura.find_byid_factura(body["id_factura"])

        if(idExistente):
            return BadResponses.return400()
        
        if(not FacturasController.mock_Cliente(body["Id_cliente"])):
            return BadResponses.return404Cliente()
        
        if(not FacturasController.mock_Vehiculo(body["VIN_coche"])):
            return BadResponses.return404Vehiculo()

        if(not FacturasController.mock_Trabajos(body["trabajos"])):
            return BadResponses.return404Trabajos()

        importe_Total=FacturasController.calculoImporte()
        

        try:
            
            nuevoObjFactura= Factura(body["id_factura"],body["estado"],body["VIN_coche"],body["Id_cliente"],body["fecha_factura"],importe_Total)
            nuevoObjFactura.save_to_db()
        except Exception as e:
            return{
                "status":None,
                "msg":f"Error {e}"
            }

        for i in body["trabajos"]:
            nuevaRelacion=RelacionFT(body["id_factura"],i)
            nuevaRelacion.save_to_db()
        
        

        
        return{
            "status":201,
            "factura":nuevoObjFactura.json(),
            
        }

    def busqueda_Porid_factura(id_factura):
        respModel:Factura=Factura.find_byid_factura(id_factura)
        if respModel:
            return{"status":200,"factura":respModel.json()}
        else:
            return {"status":404}
        
    def borrar_Porid_factura(id_factura):
        respModel:Factura=Factura.find_byid_factura(id_factura)
        if not respModel:
            return {"status":404}
        respModel.delete_from_db()
        return{"status":204}
    
    def modificarFactura(id_factura,body):
        existeFactura:Factura=Factura.find_byid_factura(id_factura)
        existeNuevoId:Factura=Factura.find_byid_factura(body["id_factura"])
        importe_Total=FacturasController.calculoImporte()
        if not (existeNuevoId )or existeFactura==existeNuevoId:
            existeFactura.delete_from_db()
            facturaModificada=Factura(body["id_factura"],body["estado"],body["VIN_coche"],body["Id_cliente"],body["fecha_factura"],importe_Total)
            facturaModificada.save_to_db()
            for i in body["trabajos"]:
                nuevaRelacion=RelacionFT(body["id_factura"],i)
                nuevaRelacion.save_to_db()
            return {"status":209,"factura":facturaModificada.json()}
        else:
            return{"status":422}