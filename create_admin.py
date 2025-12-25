from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()  # создаем таблицы, если их еще нет

    if User.query.count() == 0:  # если пользователей нет
        admin = User(username="admin", email="admin@example.com", is_admin=True)
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()
        print("Админ создан")
    else:
        print("Пользователи уже есть")
