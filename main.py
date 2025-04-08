# API de Livros
import asyncio
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

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI(
    title="API de Livros",
    description="API para gerenciar catálogo de livros.",
    version="1.0.0",
    contact={
        "name":"Atilio Hector",
        "email":"thehacktour@gmail.com"
    }
)

# Variaveis de ambiente
MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")

security = HTTPBasic()

meus_livrozinhos = {}

class LivroDB(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer)

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

Base.metadata.create_all(bind=engine)


def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Essa função tem a responsabilidade de validar o usuario e senha!
def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuario não autorizado! Credenciais inválidas!!!",
            headers={"WWW-Authenticate": "Basic"}
        )

    return credentials

@app.get("/")
def hello_world():
    return {"Hello": "World!"}
    
@app.get("/livros")
async def get_livros(page: int = 1, limit: int = 10, db: Session = Depends(sessao_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos!!!")

    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()
    await asyncio.sleep(3)
    if not livros:
        return {"message": "Não existe nenhum livro!!"}

    total_livros = db.query(LivroDB).count()

    return {
        "page": page,
        "limit": limit,
        "total": total_livros,
        "livros": [{"id": livro.id, "nome_livro": livro.nome_livro, "autor_livro": livro.autor_livro, "ano_livro": livro.ano_livro} for livro in livros]
    }

# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro


@app.post("/adiciona")
async def post_livros(livro: Livro, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro, LivroDB.autor_livro == livro.autor_livro).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe dentro do banco de dados!!!")

    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    return {"message": "O livro foi criado com sucesso!"}


# Fábrica -> Tênis que precisa ser mudado a cor!
# 1. Quem é o tênis -> Livro -> id_livro
# 2. Pegar o tênis -> Pega o livro -> id_livro
# 3. Processo de pintura para mudar a cor -> Atualização das informações do livro

# Dicionário = HashMap
# Chave -> Valor

@app.put("/atualiza/{id_livro}")
async def put_livros(id_livro: int, livro: Livro, db: Session = Depends(sessao_db),credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado no seu banco de dados!")
    
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro

    db.commit()
    db.refresh(db_livro)

    return {"message": "O livro foi atualizado com sucesso!!!"}

@app.delete("/deletar/{id_livro}")
async def delete_livro(id_livro: int, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()

    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado no seu banco de dados!!!")

    db.delete(db_livro)
    db.commit()

    return {"message": "Seu livro foi deletado com sucesso!"}


# ACID