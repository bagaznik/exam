from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.animal import Animal
from app.extensions import db
from functools import wraps

bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash("Доступ запрещен", "danger")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)
    return decorated_view

# routes/admin.py
@bp.route("/adoptions")
@login_required
@admin_required
def list_adoptions():
    from app.models.adoption import AdoptionRequest
    adoptions = AdoptionRequest.query.all()
    return render_template("admin/list_adoptions.html", adoptions=adoptions)


@bp.route("/adoptions/approve/<int:request_id>")
@login_required
@admin_required
def approve_adoption(request_id):
    from app.models.adoption import AdoptionRequest
    req = AdoptionRequest.query.get_or_404(request_id)
    req.status = "approved"
    req.animal.status = "adopted"
    db.session.commit()
    flash(f"Заявка на {req.animal.name} подтверждена", "success")
    return redirect(url_for("admin.list_adoptions"))

@bp.route("/adoptions/reject/<int:request_id>")
@login_required
@admin_required
def reject_adoption(request_id):
    from app.models.adoption import AdoptionRequest
    req = AdoptionRequest.query.get_or_404(request_id)
    req.status = "rejected"
    db.session.commit()
    flash(f"Заявка на {req.animal.name} отклонена", "info")
    return redirect(url_for("admin.list_adoptions"))


@bp.route("/animals")
@login_required
@admin_required
def list_animals():
    """Список животных для админа"""
    animals = Animal.query.all()
    return render_template("admin/list_animals.html", animals=animals)


@bp.route("/animals/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_animal():
    if request.method == "POST":
        name = request.form["name"]
        breed = request.form["breed"]
        age = int(request.form["age"])
        status = request.form.get("status", "available")
        animal = Animal(name=name, breed=breed, age=age, status=status)
        db.session.add(animal)
        db.session.commit()
        flash("Животное добавлено", "success")
        return redirect(url_for("admin.list_animals"))
    return render_template("admin/add_animal.html")


@bp.route("/animals/edit/<int:animal_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    if request.method == "POST":
        animal.name = request.form["name"]
        animal.breed = request.form["breed"]
        animal.age = int(request.form["age"])
        animal.status = request.form["status"]
        db.session.commit()
        flash("Животное обновлено", "success")
        return redirect(url_for("admin.list_animals"))
    return render_template("admin/edit_animal.html", animal=animal)


@bp.route("/animals/delete/<int:animal_id>")
@login_required
@admin_required
def delete_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)
    db.session.commit()
    flash("Животное удалено", "info")
    return redirect(url_for("admin.list_animals"))


@bp.route("/stats")
@login_required
@admin_required
def stats():
    from sqlalchemy import func
    stats = db.session.query(Animal.breed, func.count(Animal.id)).group_by(Animal.breed).all()
    stats_dict = dict(stats)
    return render_template("admin/stats.html", stats=stats_dict)
