from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Certificado(db.Model):
    __tablename__ = 'certificados'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nacionalidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    data_conclusao = db.Column(db.Date, nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)
    data_emissao = db.Column(db.Date, nullable=False)
    nome_assinatura = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    caminho = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Certificado {self.nome}>"