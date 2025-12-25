from flask import Flask
from flask_login import LoginManager
from app.extensions import db
from app.models.user import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"  # редирект, если не авторизован

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)

    # регистрация блюпринтов
    from app.routes import main, auth, animals, admin as admin_routes
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(animals.bp)
    app.register_blueprint(admin_routes.bp)

    with app.app_context():
        db.create_all()

        # создаем администратора, если его нет
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                email="admin@example.com",  # теперь обязательно
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Администратор создан: admin / admin123")

    return app

# Flask-Login: загружает пользователя по id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
