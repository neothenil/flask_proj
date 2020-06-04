from random import choice, randint
from faker import Faker

fake = Faker()
states = ["PENDING", "STARTED", "FAILURE", "SUCCESS"]


class DummyTask:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def fake_tasks(num=5):
    tasks = []
    for i in range(num):
        name = fake.name()
        progress = refint = randint(0, 100)
        if refint >= 80:
            progress = 100
        status = choose_status(progress)
        id = randint(10000, 99999)
        task = DummyTask(name=name, progress=progress, status=status, id=id)
        tasks.append(task)
    return tasks


def choose_status(progress):
    if progress == 0:
        return states[0]
    if progress == 100:
        return states[-1]
    return choice(states[1:3])
