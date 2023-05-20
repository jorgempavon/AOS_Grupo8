import datetime
import hashlib
import json
import re
#Importaciones de flask
from flask import request,Response,make_response
from flask_restful import Resource
#Importacion del controller
from Facturas.controller_facturas.controller import *
#Importacion de HTTP Problems
from helpers.HTTP_Problems import *


class RutaFacturas(Resource):
    def get(self):
        if(request.args.get("estado factura")):
            estado=request.args.get("estado factura")
        else:
            estado=None
        if(request.args.get("VIN_coche")):
            VIN_coche=request.args.get("VIN_coche")
        else:
            VIN_coche=None
        if(request.args.get("fecha factura")):
            fecha_factura=request.args.get("fecha factura")
        else:
            fecha_factura=None
        if(request.args.get("ID cliente")):
            Id_cliente=request.args.get("ID cliente")
        else:
            Id_cliente=None
        if(request.args.get("trabajos")):
            trabajos=request.args.get("trabajos")
        else:
            trabajos=None
        if(request.args.get("intervalo inferior")):
            intervalo_inferior=request.args.get("intervalo inferior")
        else:
            intervalo_inferior=None
        if(request.args.get("intervalo superior")):
            intervalo_superior=request.args.get("intervalo superior")
        else:
            intervalo_superior=None
        if(request.args.get("order")):
            order=request.args.get("order")
        else:
            order=None
        if(request.args.get("ordering")):
            ordering=request.args.get("ordering")
        else:
            ordering=None
        if(request.args.get("page")):
            page=request.args.get("page")
        else:
            page=None
        respContr=FacturasController.busqueda(estado,VIN_coche,fecha_factura,Id_cliente,trabajos,intervalo_inferior,intervalo_superior,order,ordering,page)

        if(respContr["facturas"]==[]):
            return BadResponses.return404(),404
        else:
            response=make_response(respContr)
            etag= hashlib.sha256(response.get_data()).hexdigest()
            response.headers["Access-Control-Expose-Headers"] = "ETag"
            response.set_etag(etag)
            response.status_code=200
            return response
            
    
    def options(self):
        response=make_response('')
        response.headers['Allow'] ="GET,POST,OPTIONS"
        response.headers["Access-Control-Expose-Headers"] = "Allow"
        response.status_code=204
        return response
    
    def existeElementoVacio(data):
        listaTrabajos=data["trabajos"]
        #Comprobamos que la lista de trabajos no esta vacia
        if(len(listaTrabajos)==0):
            return True
        #Comprobamos que los elementos de la lista de trabajos no sean vacíos
        for i in listaTrabajos:
            if i=="" or i.isspace()or i==None:
                return True
        #Comprobamos que los demás elementos pasados en el body no sean nulos
        lista=[data["id_factura"],data["estado"],data["VIN_coche"],data["Id_cliente"],data["fecha_factura"]]
        for i in lista:
            if i=="" or i.isspace() or i==None:
                return True
        
        return False
        
        
    def eliminarEspacios(data):
        data["id_factura"]=data["id_factura"].strip()
        data["estado"]=data["estado"].strip()
        data["VIN_coche"]=data["VIN_coche"].strip()
        data["Id_cliente"]=data["Id_cliente"].strip()
        data["fecha_factura"]=data["fecha_factura"].strip()
        lista=[]
        for i in data["trabajos"]:
            lista.append(i.strip())
        data["trabajos"]=lista
        return data
    
    def comprobarPatrones(data):
        valoresEstado=["Emitida","Pagada"]
        correctos=True
        if(not re.match("^[0-9]{4}-[0-9]{4}$", data["id_factura"])):
            return False
        if not(data["estado"]in valoresEstado):
            return False
        if(not re.match("^[A-HJ-NPR-Za-hj-npr-z\\d]{8}[\\dX][A-HJ-NPR-Za-hj-npr-z\\d]{2}\\d{6}$", data["VIN_coche"])):
            return False
        if(not re.match("^[XYZ]?\d{7,8}[A-Z]$", data["Id_cliente"])):
            return False
        if( not re.match("^\d{4}-\d{2}-\d{2}$", data["fecha_factura"])):
            return False
        
        for i in data["trabajos"]:
            if( not re.match("^T[0-9]{3}$", i)):
                return False
        
        return correctos
    
    def atributosNoPresentes(data):
        noPresentes=False
        required_attributes = ["id_factura", "estado", "VIN_coche", "Id_cliente", "trabajos", "fecha_factura"]
        
        for i in required_attributes:
            print(i)
            if i not in data:
                return True
        return noPresentes

    def post(self):
        data=request.json
        
        
        #Comprobamos si los elementos estan presentes o si son vacios

        if(RutaFacturas.atributosNoPresentes(data) or RutaFacturas.existeElementoVacio(data)):
            return BadResponses.return422(),422
        #Una vez comprobado que los datos no son vacíos, eliminamos espacios innecesarios
        data=RutaFacturas.eliminarEspacios(data)
        if(not RutaFacturas.comprobarPatrones(data)):
            return BadResponses.return422(),422
        
        
        respController=FacturasController.insercion(data)


        if(respController["status"]==400):
            return respController,400
        elif(respController["status"]==201):
            response=make_response(respController)
            response.headers['Localization'] = f'http://127.0.0.1:5000/api/v1/facturas/{data["id_factura"]}'
            response.headers["Access-Control-Expose-Headers"] = "Localization"
            response.status_code=201
            return response
        elif(respController["status"]==404):
            return respController,404
        return respController
    
        
class RutaID_Factura(Resource):
    
    def get(self,id_factura):
        
        respController=FacturasController.busqueda_Porid_factura(id_factura)
        if respController["status"]==404:
            return BadResponses.return404(),404
        else:
            response=make_response(respController["factura"])
            
            etag= hashlib.sha256(response.get_data()).hexdigest()
            response.set_etag(etag)
            response.headers["Access-Control-Expose-Headers"] = "ETag"
            response.status_code=200
            return response
    
    def options(self,id_factura):
        response=make_response('')
        response.headers['Allow']='GET,PUT,DELETE,OPTIONS'
        response.headers["Access-Control-Expose-Headers"] = "Allow"
        response.status_code=204
        return response
    
    def delete(self,id_factura):
        respController=FacturasController.borrar_Porid_factura(id_factura)
        if respController["status"]==404:
            return BadResponses.return404(),404
        else:
            response=make_response('')
            response.status_code=204
            return response
    
    def put(self,id_factura):
        data=request.json
        #Comprobamos si los elementos estan presentes o si son vacios

        if(RutaFacturas.atributosNoPresentes(data) or RutaFacturas.existeElementoVacio(data)):
            return BadResponses.return422(),422
        #Una vez comprobado que los datos no son vacíos, eliminamos espacios innecesarios
        data=RutaFacturas.eliminarEspacios(data)
        if(not RutaFacturas.comprobarPatrones(data)):
            return BadResponses.return422(),422
        
        etagCliente=request.headers.get("If-Match")
        existeRecurso=FacturasController.busqueda_Porid_factura(id_factura)
        if existeRecurso["status"]==404:
            return BadResponses.return404(),404
        recursoAmodificar=make_response(existeRecurso["factura"])
        etagRecurso=hashlib.sha256(recursoAmodificar.get_data()).hexdigest()
        if etagCliente!=etagRecurso:
            return BadResponses.return412(),412
        respContr=FacturasController.modificarFactura(id_factura,data)
        if respContr["status"]==209:
            return respContr,209
        else:
            return BadResponses.return422(),422
