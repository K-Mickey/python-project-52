from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class TaskModelTest(TaskTestCase):
    def task_creation_test(self):
        data = self.test_task["create"]["valid"]

        task = Task.objects.create(
            name=data["name"],
            description=data["description"],
            status=self.status,
            executor=self.user2,
            author=self.user1,
            date_created=data["date_created"],
        )
        task.labels.add(self.label)

        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.name, data["name"])
        self.assertEqual(task.description, data["description"])
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.date_created, data["date_created"])
        self.assertEqual(task.labels.count(), 1)
