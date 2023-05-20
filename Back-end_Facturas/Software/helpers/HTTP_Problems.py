

class BadResponses():

    def return422():
        return {
            "type": "https://httpstatuses.com/422",
            "title": "UNPROCESSABLE ENTITY",
            "status": 422,
            "detail": "Falta alguno de los atributos obligatorios o contiene un valor no admitido",
            "instance": "about:blank"}
    
    def return400():
        return  {"type": "https://httpstatuses.com/400",
                "title": "UNPROCESSABLE ENTITY",
                "status": 400,
                "detail": "El id único de la factura ya existe",
                "instance": "about:blank"}
    
    def return404():
        return  {
            "type": "https://httpstatuses.com/404",
            "title": "NOT FOUND",
            "status": 404,
            "detail": "El recurso solicitado no está disponible.",
            "instance": "about:blank"
            }
    
    def return404Cliente():
        return  {
            "type": "https://httpstatuses.com/404",
            "title": "NOT FOUND",
            "status": 404,
            "detail": "El id del cliente no existe.",
            "instance": "about:blank"
            }
    
    def return404Vehiculo():
        return  {
            "type": "https://httpstatuses.com/404",
            "title": "NOT FOUND",
            "status": 404,
            "detail": "El Vehiculo referenciado no existe.",
            "instance": "about:blank"
            }
    
    def return404Trabajos():
        return  {
            "type": "https://httpstatuses.com/404",
            "title": "NOT FOUND",
            "status": 404,
            "detail": "Algunos de los trabajos referenciados no existen.",
            "instance": "about:blank"
            }
    
    def return412():
        return  {"type": "https://httpstatuses.com/412",
                "title": "PRECONDITION FAILED",
                "status": 412,
                "detail": "El ETag proporcionado no está actualizado",
                "instance": "about:blank"}