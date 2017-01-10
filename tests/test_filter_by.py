from subconscious.model import RedisModel, Column
from uuid import uuid1
from .base import BaseTestCase
import enum


class StatusEnum(enum.Enum):
    ACTIVE = 'active'


class TestUser(RedisModel):
    id = Column(primary_key=True)
    name = Column(index=True)
    age = Column(index=True, type=int)
    locale = Column(index=True, type=int, required=False)
    status = Column(type=str, enum=StatusEnum, index=True)


class TestFilterBy(BaseTestCase):
    def setUp(self):
        super(TestFilterBy, self).setUp()
        for i in range(9):
            user = TestUser(id=str(uuid1()), name='name-{}'.format(i), age=i, locale=i+10, status='active')
            self.loop.run_until_complete(user.save(self.db))

    def test_filter_by(self):
        users = self.loop.run_until_complete(TestUser.filter_by(self.db, age=1))
        self.assertEqual(1, len(users))

        users = self.loop.run_until_complete(TestUser.filter_by(self.db, age=[1, 2]))
        self.assertEqual(2, len(users))

        users = self.loop.run_until_complete(TestUser.filter_by(self.db, status='active'))
        self.assertEqual(9, len(users))




