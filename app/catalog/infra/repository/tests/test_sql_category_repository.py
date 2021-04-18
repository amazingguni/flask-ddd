from app.catalog.domain.category import Category
from app.catalog.infra.repository.sql_category_repository import SqlCategoryRepository


def test_save(db_session):
    # Given
    category = Category(name='제과')
    # When
    SqlCategoryRepository(db_session).save(category)
    # Then
    assert db_session.query(Category).first().name == '제과'


def test_remove_by_id(db_session):
    # Given
    category = Category(name='제과')
    db_session.add(category)
    db_session.commit()
    assert db_session.query(Category).count() == 1

    # When
    SqlCategoryRepository(db_session).remove_by_id(category.id)

    # Then
    assert db_session.query(Category).count() == 0


def test_find_all(db_session):
    # Given
    for i in range(1, 6):
        db_session.add(Category(name=f'제과 {i}'))
    db_session.commit()

    # When
    result = SqlCategoryRepository(db_session).find_all()

    # Then
    assert len(result) == 5


def test_find_by_id(db_session):
    # Given
    for i in range(1, 6):
        db_session.add(Category(name=f'제과 {i}'))
    db_session.commit()

    # When
    result = SqlCategoryRepository(db_session).find_by_id(2)

    # Then
    assert result.id == 2
    assert result.name == '제과 2'
