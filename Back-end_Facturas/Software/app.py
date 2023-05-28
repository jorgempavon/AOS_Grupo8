import os
from flask import Flask
from database import db
from distutils.log import debug

from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api

from variables_entorno import dtb,puerto
#Importacion del resource
from Facturas.resource_facturas.resource import*

from Facturas.model_facturas.model import *
from Facturas_trabajos.model_relacion.modelRelacion.modeRelacionFT import *

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] =dtb
if 'SQLALCHEMY_DATABASE_URI' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
api = Api(app)

db.init_app(app)



with app.app_context():
    db.create_all()
    

CORS(app)


#Rutas

api.add_resource(RutaFacturas,"/api/v1/facturas")
api.add_resource(RutaID_Factura,"/api/v1/facturas/<id_factura>")








app.config['PORT']=puerto

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=puerto)