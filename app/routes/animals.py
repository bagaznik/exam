from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.animal import Animal
from app.extensions import db
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from app.models.adoption import AdoptionRequest
from app.extensions import db
from datetime import datetime


bp = Blueprint("animals", __name__, url_prefix="/animals")


@bp.route("/list")
@login_required
def list_animals_user():
    if current_user.is_admin:
        flash("Администраторы не могут просматривать этот раздел", "danger")
        return redirect(url_for("main.index"))

    # Получаем фильтры из запроса
    breed = request.args.get("breed", "").strip()
    age = request.args.get("age", "").strip()
    status = request.args.get("status", "").strip()

    # Строим запрос
    query = Animal.query
    if breed:
        query = query.filter(Animal.breed.ilike(f"%{breed}%"))
    if age:
        query = query.filter(Animal.age == int(age))
    if status:
        query = query.filter(Animal.status == status)

    animals = query.all()
    return render_template("list.html", animals=animals)

@bp.route("/request/<int:animal_id>", methods=["GET", "POST"])
@login_required
def request_adoption(animal_id):
    animal = Animal.query.get_or_404(animal_id)

    if animal.status != "available":
        flash("Это животное уже забронировано или усыновлено", "warning")
        return redirect(url_for("animals.list_animals_user"))

    if request.method == "POST":
        message = request.form.get("message")
        adoption_request = AdoptionRequest(
            user_id=current_user.id,
            animal_id=animal.id,
            message=message,
            status="pending",
            created_at=datetime.now()
        )
        animal.status = "reserved"  # Меняем статус на забронировано
        db.session.add(adoption_request)
        db.session.commit()
        flash("Заявка отправлена, ожидайте ответа админа", "success")
        return redirect(url_for("animals.list_animals_user"))

    return render_template("adoption_form.html", animal=animal)


@bp.route("/book/<int:animal_id>")
@login_required
def book_animal(animal_id):
    """Бронирование животного пользователем"""
    if current_user.is_admin:
        flash("Администраторы не могут бронировать животных", "danger")
        return redirect(url_for("main.index"))

    animal = Animal.query.get_or_404(animal_id)

    if animal.status != "available":
        flash("Это животное уже забронировано или усыновлено", "warning")
        return redirect(url_for("animals.list_animals_user"))

    # Бронирование животного
    animal.status = "reserved"
    animal.user_id = current_user.id  # Если есть поле user_id
    db.session.commit()

    flash(f"Вы забронировали {animal.name}", "success")
    return redirect(url_for("animals.list_animals_user"))
