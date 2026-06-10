from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    tareas = db.relationship(
        "Tarea",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


class Proyecto(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    tareas = db.relationship(
        "Tarea",
        back_populates="proyecto",
        cascade="all, delete-orphan"
    )


class Tarea(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(100)
    )

    descripcion = db.Column(
        db.Text
    )

    prioridad = db.Column(
        db.String(20)
    )

    estado = db.Column(
        db.String(20)
    )

    fecha_limite = db.Column(
        db.Date,
        nullable=True,
        default=date.today
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    proyecto_id = db.Column(
        db.Integer,
        db.ForeignKey("proyecto.id"),
        nullable=False
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="tareas"
    )

    proyecto = db.relationship(
        "Proyecto",
        back_populates="tareas"
    )