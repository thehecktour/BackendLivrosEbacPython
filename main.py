# API de Livros

# GET, POST, PUT, DELETE

# POST - Adicionar novos Livros (Create)
# GET - Buscar os dados dos Livros (Read)
# PUT - Atualizar informações dos livros (Update)
# DELETE - Deletar informações dos livros (Delete)

# CRUD

# Create
# Read
# Update
# Delete

# Vamos acessar nosso ENDPOINT
# E vamos acessar os PATH's desse 

# Path ou Rota
# Query Strings

# 200 300 400 500

# Fábrica -> Lojista -> Consumidor

# Documentação Swagger -> Documentar os endpoints da nossa aplicação (da nossa API)

# Olha, acessa minha documentação swagger nesse endpoint -> http://endpointdelivros/docs/

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API de Livros",
    description="API para gerenciar catálogo de livros.",
    version="1.0.0",
    contact={
        "name":"Atilio Hector",
        "email":"thehacktour@gmail.com"
    }
)

meus_livrozinhos = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

@app.get("/")
def hello_world():
    return {"Hello": "World!"}

@app.get("/livros")
def get_livros():
    if not meus_livrozinhos:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"livros": meus_livrozinhos}


# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro


@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse livro já existe, meu parceiro!")
    else:
        meus_livrozinhos[id_livro] = livro.dict()
        return {"message": "O livro foi criado com sucesso!"}


# Fábrica -> Tênis que precisa ser mudado a cor!
# 1. Quem é o tênis -> Livro -> id_livro
# 2. Pegar o tênis -> Pega o livro -> id_livro
# 3. Processo de pintura para mudar a cor -> Atualização das informações do livro

# Dicionário = HashMap
# Chave -> Valor

@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        # Eu jogo essa informação dentro do meu antigo dicionário (que é o meus_livrozinhos)
        # E NÃOOOOO dentro da REFERENCIA do antigo dicionário
        # Antigo dicionário != Referencia do antigo dicionário
        meus_livrozinhos[id_livro] = livro.dict()
        return {"message": "As informações do seu livro foram atualizadas com sucesso!"}


@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        del meus_livrozinhos[id_livro]
        return {"message": "Seu livro foi deletado com sucesso!"}