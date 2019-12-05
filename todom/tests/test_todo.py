from odoo.tests.common import TransactionCase


class TestTodo(TransactionCase):
    def test_create(self):
        """create a simple Todo"""
        Todo = self.env["todo.task"]
        task = Todo.create({'name': 'Test Task'})
        self.assertItemsEqual(task.is_done, False)
