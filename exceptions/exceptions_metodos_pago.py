class MetodoPagoExistenteException(Exception):
    pass

class MetodoPagoNoExistenteException(Exception):
    pass

if not resultado:
        raise HTTPException(status_code=400,detail="El metodo ya fue creado")
    return resultado

@router.put('/{metodo_id}',response_model=MetodoPagoResponder)
def actualizar_metodos_pago(metodo_id:str,metodo_actualizar:MetodoPagoBase,db:Session=Depends(get_db)):
    resultado = actualizar_metodo_pago(metodo_id,metodo_actualizar,db)
    if not resultado:
        raise HTTPException(status_code=404,detail="Metodo de pago no encontrado")
    return resultado