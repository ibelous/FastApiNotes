import factory

from app.config import Board


class BoardFactory(factory.Factory):
    class Meta:
        model = Board

    title = factory.faker.Faker("pystr")
    created_at = factory.faker.Faker("date_time")
    modified_at = factory.faker.Faker("date_time")


