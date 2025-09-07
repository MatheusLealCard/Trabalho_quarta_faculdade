from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import csv

DATABASE_URL = "sqlite:///Dados.db"
engine = create_engine(DATABASE_URL)  
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class UF(Base):
    __tablename__ = "ufs"
    id = Column(Integer, primary_key=True)
    nome = Column(String, index=True)
    sigla = Column(String(2), index=True)
    municipios = relationship("Municipio", back_populates="uf")

class Municipio(Base):
    __tablename__ = "municipios"
    id = Column(Integer, primary_key=True)
    nome = Column(String, index=True)
    uf_id = Column(Integer, ForeignKey("ufs.id"))
    uf = relationship("UF", back_populates="municipios")
    minas = relationship("NomeMina", back_populates="municipio")

class NomeMina(Base):
    __tablename__ = "minas"
    id = Column(Integer, primary_key=True)
    nome = Column(String, index=True)
    latitude = Column(String)
    longitude = Column(String)
    municipio_id = Column(Integer, ForeignKey("municipios.id"))
    municipio = relationship("Municipio", back_populates="minas")
    empreendedor_id = Column(Integer, ForeignKey("empreendedores.id"))
    empreendedor = relationship("Empreendedor", back_populates="minas")

class Empreendedor(Base):
    __tablename__ = "empreendedores"
    id = Column(Integer, primary_key=True)
    nome = Column(String, index=True)
    cpf_cnpj = Column(String, index=True)
    minas = relationship("NomeMina", back_populates="empreendedor")

Base.metadata.create_all(engine)

db = SessionLocal()
with open("dataset/Barragens.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        uf = UF(nome=row["UF"], sigla=row.get("Sigla", ""))
        municipio = Municipio(nome=row["Municipio"], uf=uf)
        empreendedor = Empreendedor(nome=row["Empreendedor"], cpf_cnpj=row["CPF_CNPJ"])
        mina = NomeMina(
            nome=row["Nome_da_mina"],
            latitude=str(row["Latitude"]),
            longitude=str(row["Longitude"]),
            municipio=municipio,
            empreendedor=empreendedor
        )
        db.add_all([uf, municipio, empreendedor, mina])

db.commit()
db.close()

