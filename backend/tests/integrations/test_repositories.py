from app.repositories import LookupRepository


def test_get_days_returns_seeded(db_session, day):
    repo = LookupRepository(session=db_session)
    result = repo.get_days()
    assert any(d.id == day.id for d in result)
