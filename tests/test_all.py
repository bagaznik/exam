import pytest
from app import create_app
from app.extensions import db
from app.models.animal import Animal
from app.models.user import User
from app.models.adoption import AdoptionRequest

@pytest.fixture
def app_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

# ----------------------- ANIMAL TESTS -----------------------
def test_create_animal(app_client):
    with app_client.application.app_context():
        animal = Animal(name="Buddy", breed="Golden Retriever", age=3, status="available")
        db.session.add(animal)git init
        db.session.commit()
        fetched = Animal.query.filter_by(name="Buddy").first()
        assert fetched is not None
        assert fetched.age == 3

def test_read_animal(app_client):
    with app_client.application.app_context():
        animal = Animal(name="Max", breed="Beagle", age=2, status="available")
        db.session.add(animal)
        db.session.commit()
        fetched = Animal.query.get(animal.id)
        assert fetched.name == "Max"

def test_update_animal_status(app_client):
    with app_client.application.app_context():
        animal = Animal(name="Lucy", breed="Bulldog", age=4, status="available")
        db.session.add(animal)
        db.session.commit()
        animal.status = "adopted"
        db.session.commit()
        assert Animal.query.get(animal.id).status == "adopted"

def test_delete_animal(app_client):
    with app_client.application.app_context():
        animal = Animal(name="Charlie", breed="Poodle", age=1, status="available")
        db.session.add(animal)
        db.session.commit()
        db.session.delete(animal)
        db.session.commit()
        assert Animal.query.get(animal.id) is None

def test_animal_breed_saved(app_client):
    with app_client.application.app_context():
        animal = Animal(name="Bella", breed="Husky", age=3, status="available")
        db.session.add(animal)
        db.session.commit()
        assert Animal.query.get(animal.id).breed == "Husky"

def test_multiple_animals(app_client):
    with app_client.application.app_context():
        animals = [
            Animal(name="A", breed="Breed1", age=1, status="available"),
            Animal(name="B", breed="Breed2", age=2, status="available"),
        ]
        db.session.add_all(animals)
        db.session.commit()
        assert Animal.query.count() == 2

def test_filter_available_animals(app_client):
    with app_client.application.app_context():
        a1 = Animal(name="Free", breed="BreedA", age=1, status="available")
        a2 = Animal(name="Taken", breed="BreedB", age=2, status="adopted")
        db.session.add_all([a1, a2])
        db.session.commit()
        available = Animal.query.filter_by(status="available").all()
        assert len(available) == 1
        assert available[0].name == "Free"

def test_animal_repr(app_client):
    with app_client.application.app_context():
        animal = Animal(name="NiceDog", breed="Mix", age=3, status="available")
        db.session.add(animal)
        db.session.commit()
        # проверяем, что repr содержит id
        assert str(animal.id) in repr(animal)

# ----------------------- USER TESTS -----------------------
def test_create_user(app_client):
    with app_client.application.app_context():
        user = User(username="john", email="john@example.com")
        db.session.add(user)
        db.session.commit()
        fetched = User.query.filter_by(username="john").first()
        assert fetched is not None

def test_read_user(app_client):
    with app_client.application.app_context():
        user = User(username="anna", email="anna@example.com")
        db.session.add(user)
        db.session.commit()
        fetched = User.query.get(user.id)
        assert fetched.username == "anna"

def test_update_user_email(app_client):
    with app_client.application.app_context():
        user = User(username="mike", email="old@example.com")
        db.session.add(user)
        db.session.commit()
        user.email = "new@example.com"
        db.session.commit()
        assert User.query.get(user.id).email == "new@example.com"

def test_delete_user(app_client):
    with app_client.application.app_context():
        user = User(username="kate", email="kate@example.com")
        db.session.add(user)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        assert User.query.get(user.id) is None

# ----------------------- ADOPTION REQUEST TESTS -----------------------
def test_create_adoption_request(app_client):
    with app_client.application.app_context():
        user = User(username="tom", email="tom@example.com")
        animal = Animal(name="Doggo", breed="Shepherd", age=3, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        request = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(request)
        db.session.commit()
        fetched = AdoptionRequest.query.first()
        assert fetched.status == "pending"

def test_read_adoption_request(app_client):
    with app_client.application.app_context():
        user = User(username="lucy", email="lucy@example.com")
        animal = Animal(name="Catty", breed="Siamese", age=2, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        request = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(request)
        db.session.commit()
        fetched = AdoptionRequest.query.get(request.id)
        assert fetched.animal.name == "Catty"

def test_update_request_status(app_client):
    with app_client.application.app_context():
        user = User(username="leo", email="leo@example.com")
        animal = Animal(name="Kitty", breed="Persian", age=1, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(req)
        db.session.commit()
        req.status = "approved"
        db.session.commit()
        assert AdoptionRequest.query.get(req.id).status == "approved"

def test_delete_request(app_client):
    with app_client.application.app_context():
        user = User(username="nina", email="nina@example.com")
        animal = Animal(name="Doggy", breed="Mix", age=4, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(req)
        db.session.commit()
        db.session.delete(req)
        db.session.commit()
        assert AdoptionRequest.query.get(req.id) is None

def test_request_links_user(app_client):
    with app_client.application.app_context():
        user = User(username="sam", email="sam@example.com")
        animal = Animal(name="Lucky", breed="Mix", age=2, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(req)
        db.session.commit()
        assert req.user.username == "sam"

def test_request_links_animal(app_client):
    with app_client.application.app_context():
        user = User(username="amy", email="amy@example.com")
        animal = Animal(name="Shadow", breed="Husky", age=3, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(req)
        db.session.commit()
        assert req.animal.name == "Shadow"

def test_pending_requests_count(app_client):
    with app_client.application.app_context():
        user = User(username="peter", email="peter@example.com")
        animal1 = Animal(name="A1", breed="B1", age=1, status="available")
        animal2 = Animal(name="A2", breed="B2", age=2, status="available")
        db.session.add_all([user, animal1, animal2])
        db.session.commit()
        req1 = AdoptionRequest(user_id=user.id, animal_id=animal1.id, status="pending")
        req2 = AdoptionRequest(user_id=user.id, animal_id=animal2.id, status="approved")
        db.session.add_all([req1, req2])
        db.session.commit()
        pending = AdoptionRequest.query.filter_by(status="pending").count()
        assert pending == 1

def test_request_repr(app_client):
    with app_client.application.app_context():
        user = User(username="ella", email="ella@example.com")
        animal = Animal(name="Snow", breed="Siamese", age=2, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(req)
        db.session.commit()
        # проверяем, что repr содержит id
        assert str(req.id) in repr(req)

def test_adopted_animal_status_change(app_client):
    with app_client.application.app_context():
        user = User(username="alex", email="alex@example.com")
        animal = Animal(name="Tommy", breed="Mix", age=2, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="approved")
        db.session.add(req)
        db.session.commit()
        animal.status = "adopted"
        db.session.commit()
        assert Animal.query.get(animal.id).status == "adopted"

def test_user_has_requests(app_client):
    with app_client.application.app_context():
        user = User(username="lily", email="lily@example.com")
        animal = Animal(name="Milo", breed="Mix", age=3, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(req)
        db.session.commit()
        assert len(user.adoption_requests) == 1

def test_animal_has_requests(app_client):
    with app_client.application.app_context():
        user = User(username="jack", email="jack@example.com")
        animal = Animal(name="Rocky", breed="Mix", age=4, status="available")
        db.session.add_all([user, animal])
        db.session.commit()
        req = AdoptionRequest(user_id=user.id, animal_id=animal.id, status="pending")
        db.session.add(req)
        db.session.commit()
        assert len(animal.adoption_requests) == 1
