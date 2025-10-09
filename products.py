from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from connection import conexaoBanco


class Produto(BaseModel):
    name: str
products_router = APIRouter(prefix='/produtos', tags=("produtos"))

@products_router.get("/")
def get_produtos():
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'select * from produtos'
    cursor.execute(comando_sql)
    resultado_consulta = cursor.fetchall()
    return resultado_consulta

@products_router.post("/")
def post_produtos(item: Produto):
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'INSERT INTO produtos (name) VALUES (%(name)s)'
    cursor.execute(comando_sql, item.model_dump())
    conexaoBanco.commit()
    return cursor.lastrowid


@products_router.patch("/{id}")
def patch_produtos(item: Produto, id: int):
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'select * from produtos where id = %(id)s'
    cursor.execute(comando_sql, { "id": id })
    resultado_consulta = cursor.fetchone()

    if resultado_consulta is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

       
    comando_sql = '''
        UPDATE produtos SET name = %(name)s WHERE id = %(id)s
    '''
    values = item.model_dump()
    values['id'] = id
    cursor.execute(comando_sql, values)
    conexaoBanco.commit()
    return item.model_dump()

@products_router.delete("/{id}")
def delete_produtos(id: int):
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'select * from produtos where id = %(id)s'
    cursor.execute(comando_sql, { "id": id })
    resultado_consulta = cursor.fetchone()

    if resultado_consulta is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    comando_sql = 'DELETE FROM produtos WHERE id = %(id)s'
    cursor.execute(comando_sql, { "id": id })
    conexaoBanco.commit()
    return cursor.lastrowid
