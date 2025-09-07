from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Orm import UF, Municipio, NomeMina, Empreendedor
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="API Barragens", version="1.0", description="API para consultar barragens e empreendedores")

DATABASE_URL = "sqlite:///Dados.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def criar_token(dados: dict):
    dados_copy = dados.copy()
    dados_copy.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(dados_copy, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token obrigatório no header Authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/token")
def get_token():
    token = criar_token({"sub": "12345"})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/all")
def get_all(
    uf: str | None = None,
    municipio: str | None = None,
    empreendedor: str | None = None,
    token: dict = Depends(verificar_token)
):
    db = SessionLocal()
    query = db.query(NomeMina)
    if uf:
        query = query.join(Municipio).join(UF).filter(UF.nome == uf)
    if municipio:
        query = query.join(Municipio).filter(Municipio.nome == municipio)
    if empreendedor:
        query = query.join(Empreendedor).filter(Empreendedor.nome == empreendedor)

    result = []
    for mina in query.all():
        result.append({
            "id": mina.id,
            "nome_mina": mina.nome,
            "latitude": mina.latitude,
            "longitude": mina.longitude,
            "municipio": mina.municipio.nome if mina.municipio else None,
            "uf": mina.municipio.uf.nome if mina.municipio and mina.municipio.uf else None,
            "empreendedor": mina.empreendedor.nome if mina.empreendedor else None
        })
    db.close()
    return result

