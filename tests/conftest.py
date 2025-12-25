import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app()  # ⬅️ НИКАКИХ аргументов

    # ⚠️ включаем тестовый режим ТОЛЬКО для тестов
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
        LOGIN_DISABLED=True,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
@pytest.fixture
def db_session(app):
    """
    Даёт тестам доступ к db.session
    и автоматически откатывает изменения
    """
    with app.app_context():
        yield db.session
        db.session.rollback()