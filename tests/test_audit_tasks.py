from dataclasses import FrozenInstanceError
import unittest

from audit_tasks import (
    IdentityRequiredError,
    InvalidTitleError,
    TaskService,
    TaskUnavailableError,
)


class TaskServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = TaskService()

    def test_001_create_normalized_distinct_tasks(self):
        first = self.service.create_task(actor_id="actor-a", title="  Revisar informe  ")
        second = self.service.create_task(actor_id="actor-a", title="  Revisar informe  ")
        self.assertNotEqual(first.id, second.id)
        for task in (first, second):
            self.assertEqual(task.title, "Revisar informe")
            self.assertEqual(task.owner_id, "actor-a")
            self.assertEqual(task.status, "PENDING")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [first, second])

    def test_002_invalid_titles_leave_state_unchanged(self):
        existing = self.service.create_task(actor_id="actor-a", title="Existente")
        for title in ("", "   ", "\t\n", None, 123, False, [], {}):
            with self.subTest(title=title):
                with self.assertRaisesRegex(InvalidTitleError, "^Valid title required$"):
                    self.service.create_task(actor_id="actor-a", title=title)
                self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [existing])

    def test_003_list_owned_tasks_in_creation_order(self):
        first = self.service.create_task(actor_id="actor-a", title="Primera")
        other = self.service.create_task(actor_id="actor-b", title="Ajena")
        last = self.service.create_task(actor_id="actor-a", title="Ultima")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [first, last])
        self.assertEqual(self.service.list_tasks(actor_id="actor-b"), [other])
        completed = self.service.complete_task(actor_id="actor-a", task_id=first.id)
        self.assertEqual(completed.status, "COMPLETED")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [completed, last])
        self.assertEqual(self.service.list_tasks(actor_id="actor-b"), [other])

    def test_004_empty_owner_cannot_see_other_tasks(self):
        self.service.create_task(actor_id="actor-b", title="Ajena")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [])

    def test_005_completion_is_idempotent_and_preserves_other_data(self):
        first = self.service.create_task(actor_id="actor-a", title="Primera")
        second = self.service.create_task(actor_id="actor-a", title="Segunda")
        completed = self.service.complete_task(actor_id="actor-a", task_id=first.id)
        repeated = self.service.complete_task(actor_id="actor-a", task_id=first.id)
        self.assertEqual(completed, repeated)
        self.assertEqual(completed.status, "COMPLETED")
        self.assertEqual(
            (completed.id, completed.title, completed.owner_id),
            (first.id, first.title, first.owner_id),
        )
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [completed, second])
        self.assertEqual(second.status, "PENDING")

    def test_006_invalid_identity_rejected_without_mutation(self):
        existing = self.service.create_task(actor_id="actor-a", title="Privada")
        for actor in (None, "", "  ", "\t\n", 0, False, [], {}):
            operations = (
                lambda: self.service.create_task(actor_id=actor, title="Valida"),
                lambda: self.service.list_tasks(actor_id=actor),
                lambda: self.service.create_task(actor_id=actor, title=None),
                lambda: self.service.complete_task(actor_id=actor, task_id=existing.id),
                lambda: self.service.complete_task(actor_id=actor, task_id=[]),
            )
            for index, operation in enumerate(operations):
                with self.subTest(actor=actor, operation=index):
                    with self.assertRaisesRegex(
                        IdentityRequiredError, "^Valid actor identity required$"
                    ):
                        operation()
                    self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [existing])

    def test_006_actor_identifiers_are_compared_exactly(self):
        task = self.service.create_task(actor_id=" actor-a ", title="Propia")
        self.assertEqual(task.owner_id, " actor-a ")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [])
        self.assertEqual(self.service.list_tasks(actor_id=" actor-a "), [task])
        with self.assertRaisesRegex(TaskUnavailableError, "^Task unavailable$"):
            self.service.complete_task(actor_id="actor-a", task_id=task.id)

    def test_007_unavailable_tasks_share_error_without_mutation(self):
        own = self.service.create_task(actor_id="actor-a", title="Propia")
        other = self.service.create_task(actor_id="actor-b", title="Privada de B")
        for task_id in (other.id, 999, 0, -1, True, False, "1", 1.0, None, [], {}):
            with self.subTest(task_id=task_id):
                with self.assertRaises(TaskUnavailableError) as caught:
                    self.service.complete_task(actor_id="actor-a", task_id=task_id)
                self.assertIs(type(caught.exception), TaskUnavailableError)
                self.assertEqual(str(caught.exception), "Task unavailable")
                self.assertEqual(caught.exception.args, ("Task unavailable",))
                self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [own])
                self.assertEqual(self.service.list_tasks(actor_id="actor-b"), [other])

    def test_008_creation_cannot_assign_another_owner(self):
        task = self.service.create_task(actor_id="actor-a", title="Propia")
        self.assertEqual(task.owner_id, "actor-a")
        self.assertEqual(self.service.list_tasks(actor_id="actor-b"), [])
        with self.assertRaises(TypeError):
            self.service.create_task(actor_id="actor-a", title="Otra", owner_id="actor-b")
        with self.assertRaises(TypeError):
            self.service.create_task(title="Sin identidad")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [task])
        self.assertEqual(self.service.list_tasks(actor_id="actor-b"), [])

    def test_010_returned_objects_and_instances_are_isolated(self):
        task = self.service.create_task(actor_id="actor-a", title="Intacta")
        for field, value in (
            ("id", 999), ("title", "Alterada"), ("owner_id", "actor-b"),
            ("status", "COMPLETED"),
        ):
            with self.subTest(field=field):
                with self.assertRaises(FrozenInstanceError):
                    setattr(task, field, value)
        returned = self.service.list_tasks(actor_id="actor-a")
        returned.clear()
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [task])
        separate = TaskService()
        self.assertEqual(separate.list_tasks(actor_id="actor-a"), [])
        separate.create_task(actor_id="actor-a", title="Otra instancia")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [task])

    def test_011_full_local_flow_for_two_actors(self):
        first = self.service.create_task(actor_id="actor-a", title="  Preparar  ")
        private = self.service.create_task(actor_id="actor-b", title="Reservada")
        last = self.service.create_task(actor_id="actor-a", title="Entregar")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [first, last])
        with self.assertRaisesRegex(TaskUnavailableError, "^Task unavailable$"):
            self.service.complete_task(actor_id="actor-a", task_id=private.id)
        completed = self.service.complete_task(actor_id="actor-a", task_id=first.id)
        self.assertEqual(completed.title, "Preparar")
        self.assertEqual(completed.owner_id, "actor-a")
        self.assertEqual(completed.status, "COMPLETED")
        self.assertEqual(self.service.list_tasks(actor_id="actor-a"), [completed, last])
        self.assertEqual(self.service.list_tasks(actor_id="actor-b"), [private])


if __name__ == "__main__":
    unittest.main()
