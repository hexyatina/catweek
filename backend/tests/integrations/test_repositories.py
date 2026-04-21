def test_schedule_repository_returns_list(app, db_session):
    from src.app.repositories.schedule import ScheduleRepository

    with app.app_context():
        repo = ScheduleRepository(db_session)
        result = repo.get_filtered()
        assert isinstance(result, list)


def test_lookup_repository_returns_list(app, db_session):
    from src.app.services.database import DatabaseService
    from src.app.repositories.lookup import LookupRepository

    with app.app_context():
        DatabaseService.seed_system_data()
        repo = LookupRepository(db_session)
        groups = repo.get_groups()
        assert isinstance(groups, list)
        assert len(groups) > 0
