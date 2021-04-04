from app.user.domain.user import User


def test_user(db_session):
    user = User(
        username='amazingguni',
        password='password'
    )
    db_session.add(user)
    db_session.commit()
