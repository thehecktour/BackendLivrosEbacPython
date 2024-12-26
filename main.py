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

from fastapi import FastAPI, HTTPException

app = FastAPI()

meus_livrozinhos = {}

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
def post_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse livro já existe, meu parceiro!")
    else:
        meus_livrozinhos[id_livro] = {"nome_livro": nome_livro, "autor_livro": autor_livro, "ano_livro": ano_livro}
        return {"message": "O livro foi criado com sucesso!"}


# Fábrica -> Tênis que precisa ser mudado a cor!
# 1. Quem é o tênis -> Livro -> id_livro
# 2. Pegar o tênis -> Pega o livro -> id_livro
# 3. Processo de pintura para mudar a cor -> Atualização das informações do livro

@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: str):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        if nome_livro:
            meu_livro["nome_livro"] = nome_livro
        if autor_livro:
            meu_livro["autor_livro"] = autor_livro
        if ano_livro:
            meu_livro["ano_livro"] = ano_livro
        
        return {"message": "As informações do seu livro foram atualizadas com sucesso!"}


@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        del meus_livrozinhos[id_livro]

        return {"message": "Seu livro foi deletado com sucesso!"}