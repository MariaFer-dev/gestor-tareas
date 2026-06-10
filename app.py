from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    url_for
)
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from config import Config
from models import db, Usuario, Proyecto, Tarea

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def cargar_usuario(user_id):
    return db.session.get(Usuario, int(user_id))

with app.app_context():
    db.create_all()


@app.route("/init")
def init_db():
    """Inicializa la base de datos creando todas las tablas."""
    try:
        with app.app_context():
            db.create_all()
        return {"status": "success", "message": "Tablas creadas correctamente"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@app.route("/")
def inicio():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not nombre or not email or not password:
            flash("Completa todos los campos.", "danger")
            return render_template("register.html")

        existe = Usuario.query.filter_by(email=email).first()

        if existe:
            flash("Ese correo ya está registrado.", "danger")
            return render_template("register.html")

        usuario = Usuario(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(usuario)
        db.session.commit()

        flash("Registro exitoso. Ahora inicia sesión.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not check_password_hash(usuario.password, password):
            flash("Correo o contraseña incorrectos.", "danger")
            return render_template("login.html")

        login_user(usuario)
        flash(f"Bienvenido, {usuario.nombre}.", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():

    total_proyectos = Proyecto.query.count()

    total_tareas = Tarea.query.count()

    completadas = Tarea.query.filter_by(
        estado="Completada"
    ).count()

    pendientes = Tarea.query.filter_by(estado="Pendiente").count()

    en_progreso = Tarea.query.filter_by(estado="En progreso").count()

    ultimas_tareas = Tarea.query.order_by(Tarea.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_proyectos=total_proyectos,
        total_tareas=total_tareas,
        completadas=completadas,
        pendientes=pendientes,
        en_progreso=en_progreso,
        ultimas_tareas=ultimas_tareas
    )


@app.route("/proyectos")
@login_required
def proyectos():

    lista = Proyecto.query.all()

    return render_template(
        "proyectos.html",
        proyectos=lista
    )


@app.route("/proyectos/nuevo",
           methods=["GET", "POST"])
@login_required
def nuevo_proyecto():

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()

        if not nombre or not descripcion:
            flash("Completa todos los campos del proyecto.", "danger")
            return render_template(
                "crear_proyecto.html",
                titulo="Crear Proyecto",
                proyecto=None
            )

        nuevo = Proyecto(
            nombre=nombre,
            descripcion=descripcion
        )

        db.session.add(nuevo)
        db.session.commit()

        flash("Proyecto creado correctamente.", "success")

        return redirect(url_for("proyectos"))

    return render_template(
        "crear_proyecto.html",
        titulo="Crear Proyecto",
        proyecto=None
    )


@app.route("/proyectos/editar/<int:id>",
           methods=["GET", "POST"])
@login_required
def editar_proyecto(id):

    proyecto = Proyecto.query.get_or_404(id)

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()

        if not nombre or not descripcion:
            flash("Completa todos los campos del proyecto.", "danger")
            return render_template(
                "crear_proyecto.html",
                titulo="Editar Proyecto",
                proyecto=proyecto
            )

        proyecto.nombre = nombre

        proyecto.descripcion = descripcion

        db.session.commit()

        flash("Proyecto actualizado correctamente.", "success")

        return redirect(url_for("proyectos"))

    return render_template(
        "crear_proyecto.html",
        titulo="Editar Proyecto",
        proyecto=proyecto
    )


@app.route("/proyectos/eliminar/<int:id>")
@login_required
def eliminar_proyecto(id):

    proyecto = Proyecto.query.get_or_404(id)

    if proyecto.tareas:
        flash("No puedes eliminar un proyecto que todavía tiene tareas.", "danger")
        return redirect(url_for("proyectos"))

    db.session.delete(proyecto)

    db.session.commit()

    flash("Proyecto eliminado.", "info")

    return redirect(url_for("proyectos"))


@app.route("/tareas")
@login_required
def tareas():

    estado = request.args.get("estado", "")
    prioridad = request.args.get("prioridad", "")
    q = request.args.get("q", "").strip()

    consulta = Tarea.query

    if estado:
        consulta = consulta.filter_by(estado=estado)

    if prioridad:
        consulta = consulta.filter_by(prioridad=prioridad)

    if q:
        patron = f"%{q}%"
        consulta = consulta.filter(
            Tarea.titulo.ilike(patron) |
            Tarea.descripcion.ilike(patron)
        )

    lista_tareas = consulta.order_by(Tarea.id.desc()).all()

    return render_template(
        "tareas.html",
        tareas=lista_tareas,
        proyectos=Proyecto.query.order_by(Proyecto.nombre.asc()).all(),
        usuarios=Usuario.query.order_by(Usuario.nombre.asc()).all(),
        estado_actual=estado,
        prioridad_actual=prioridad,
        busqueda=q
    )


@app.route("/tareas/nueva", methods=["GET", "POST"])
@login_required
def nueva_tarea():

    proyectos = Proyecto.query.order_by(Proyecto.nombre.asc()).all()
    usuarios = Usuario.query.order_by(Usuario.nombre.asc()).all()

    if request.method == "POST":

        titulo = request.form["titulo"].strip()
        descripcion = request.form["descripcion"].strip()
        prioridad = request.form["prioridad"]
        estado = request.form["estado"]
        fecha_limite_raw = request.form["fecha_limite"]
        usuario_id = request.form["usuario_id"]
        proyecto_id = request.form["proyecto_id"]

        if not titulo or not descripcion:
            flash("Completa título y descripción.", "danger")
            return render_template(
                "crear_tareas.html",
                tarea=None,
                proyectos=proyectos,
                usuarios=usuarios
            )

        if not usuario_id or not proyecto_id:
            flash("Debes asignar la tarea a un usuario y a un proyecto.", "danger")
            return render_template(
                "crear_tareas.html",
                tarea=None,
                proyectos=proyectos,
                usuarios=usuarios
            )

        fecha_limite = None

        if fecha_limite_raw:
            fecha_limite = datetime.strptime(fecha_limite_raw, "%Y-%m-%d").date()

        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            estado=estado,
            fecha_limite=fecha_limite,
            usuario_id=int(usuario_id),
            proyecto_id=int(proyecto_id)
        )

        db.session.add(tarea)
        db.session.commit()

        flash("Tarea creada correctamente.", "success")
        return redirect(url_for("tareas"))

    return render_template(
        "crear_tareas.html",
        tarea=None,
        proyectos=proyectos,
        usuarios=usuarios
    )


@app.route("/tareas/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_tarea(id):

    tarea = Tarea.query.get_or_404(id)
    proyectos = Proyecto.query.order_by(Proyecto.nombre.asc()).all()
    usuarios = Usuario.query.order_by(Usuario.nombre.asc()).all()

    if request.method == "POST":

        tarea.titulo = request.form["titulo"].strip()
        tarea.descripcion = request.form["descripcion"].strip()
        tarea.prioridad = request.form["prioridad"]
        tarea.estado = request.form["estado"]
        fecha_limite_raw = request.form["fecha_limite"]
        tarea.usuario_id = int(request.form["usuario_id"])
        tarea.proyecto_id = int(request.form["proyecto_id"])

        if fecha_limite_raw:
            tarea.fecha_limite = datetime.strptime(fecha_limite_raw, "%Y-%m-%d").date()
        else:
            tarea.fecha_limite = None

        db.session.commit()
        flash("Tarea actualizada correctamente.", "success")
        return redirect(url_for("tareas"))

    return render_template(
        "crear_tareas.html",
        tarea=tarea,
        proyectos=proyectos,
        usuarios=usuarios
    )


@app.route("/tareas/eliminar/<int:id>")
@login_required
def eliminar_tarea(id):

    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    flash("Tarea eliminada.", "info")
    return redirect(url_for("tareas"))


if __name__ == "__main__":
    app.run(debug=True)