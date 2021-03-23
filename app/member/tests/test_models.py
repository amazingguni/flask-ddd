from app.member.domain.member import Member

def test_member(db_session):
    member = Member(
        name='amazingguni',
        password='password'
    )
    db_session.add(member)
    db_session.commit()