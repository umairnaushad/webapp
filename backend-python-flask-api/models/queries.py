from models.base import Session
from models.user import User


session = Session()
users = session.query(User).all()

print(f'UserName \t Email')
for user in users:
    print(f'{user.username} \t {user.email}')
print('')