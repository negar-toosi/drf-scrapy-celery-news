import factory
import random

from django.utils import timezone
from technews.utils.test.base import faker
from technews.news.models import News, Tags

class TagsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tags
    name = factory.LazyFunction(lambda: faker.word())

class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News
    title = factory.LazyFunction(lambda: faker.sentence())
    content = factory.LazyFunction(lambda: faker.text())
    summary = factory.LazyFunction(lambda: faker.paragraph())
    source = factory.LazyFunction(lambda: faker.url())
    published_at = factory.LazyFunction(lambda: timezone.make_aware(faker.date_time_between_dates(datetime_start='now')))
    status = factory.LazyFunction(lambda: faker.pybool())
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.tags.add(*extracted)
        else:
            tags = TagsFactory.create_batch(random.randint(1,3))
            self.tags.add(*tags)