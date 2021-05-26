from datetime import date
from models.base import Session, engine, Base
from models.user import User

##Base.metadata.create_all(engine)

session = Session()

user10 = User("user10", "user10@user.com")
user11 = User("user11", "user11@user.com")

session.add(user10)
session.add(user11)

session.commit()
session.close()