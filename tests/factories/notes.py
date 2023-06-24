import factory

from app.config import Note
from tests.factories.boards import BoardFactory


class NoteFactory(factory.Factory):
    class Meta:
        model = Note

    text = factory.faker.Faker("pystr")
    board = factory.SubFactory(BoardFactory)
    views_count = factory.faker.Faker("pyint")
    created_at = factory.faker.Faker("date_time")
    modified_at = factory.faker.Faker("date_time")
