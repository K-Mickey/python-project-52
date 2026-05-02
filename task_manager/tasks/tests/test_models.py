from task_manager.tasks.tests.testcase import TaskTestCase


class TaskModelTest(TaskTestCase):
    def task_creation_test(self):
        data = self.test_task["create"]["valid"]

        task = Task.objects.create(
            ...
        )