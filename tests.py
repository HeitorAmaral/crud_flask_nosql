"""
Unit Tests
"""
import unittest
from src import app
from src.repository.task_repository import TaskRepository
from src.controller.task_controller import find_next_available_id

app.config['TESTING'] = True


class TestIndex(unittest.TestCase):
    """
    Class to allocate the test methods of index page (/index).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
        instance and mock Database, makes a GET HTTP request to /index
        endpoint and stores the response in a variable.
        """
        self.app_test = app.test_client()
        self.db = TaskRepository(app)
        self.response = self.app_test.get('/')

    def tearDown(self):
        """
        Method to be executed when test finish. Drop the mock database.
        """
        self.db.drop_mongo_connection()

    def test_get_index_returns_200(self):
        """
        Method to test if the /index endpoint returns 200 in HTTP
        status code.
        """
        print("In method", self._testMethodName)
        self.assertEqual(200, self.response.status_code)

    def test_get_index_renders_html(self):
        """
        Method to test if the /index endpoint returns HTML.
        """
        print("In method", self._testMethodName)
        self.assertIn('text/html', self.response.content_type)

    def test_get_index_renders_title_html(self):
        """
        Method to test if the /index endpoint returns a HTML tag with
        title of the page.
        """
        print("In method", self._testMethodName)
        response_decoded = self.response.data.decode('utf-8')
        self.assertIn('<title>Página Inícial</title>', response_decoded)


class TestFindAll(unittest.TestCase):
    """
    Class to allocate the test methods of list page (/find-all).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
        instance and mock Database with register. Makes a GET HTTP
        request to /find-all endpoint and stores the response in a
        variable.
        """
        self.app_test = app.test_client()
        self.db = TaskRepository(app)

        self.mock_task_id = 1
        self.mock_task_description = "MockData"
        self.mock_task_status = False

        self.db.insert_one(self.mock_task_id, self.mock_task_description,
                           self.mock_task_status)

        self.response = self.app_test.get('/find-all')

    def tearDown(self):
        """
        Method to be executed when test finish. Drop the mock database.
        """
        self.db.drop_mongo_connection()

    def test_get_find_all_returns_200(self):
        """
        Method to test if the /find-all endpoint returns 200 in HTTP
        status code.
        """
        print("In method", self._testMethodName)
        self.assertEqual(200, self.response.status_code)

    def test_get_find_all_renders_html(self):
        """
        Method to test if the /find-all endpoint returns HTML.
        """
        print("In method", self._testMethodName)
        self.assertIn('text/html', self.response.content_type)

    def test_get_find_all_renders_title_html(self):
        """
        Method to test if the /find-all endpoint returns a HTML tag
        with title of the page.
        """
        print("In method", self._testMethodName)
        response_decoded = self.response.data.decode('utf-8')
        self.assertIn('<title>Lista de Tarefas</title>', response_decoded)

    def test_find_next_available_id_returns_2(self):
        """
        Method to test if the method find_next_available_id returns the
        correct available id.
        """
        print("In method", self._testMethodName)
        self.assertEqual(2, find_next_available_id())


class TestInsert(unittest.TestCase):
    """
    Class to allocate the test methods of insert page (/insert).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
        instance and mock Database. Makes a GET HTTP request to /insert
        endpoint and stores the response in a variable.
        """
        self.app_test = app.test_client()
        self.db = TaskRepository(app)
        self.response = self.app_test.get('/insert')

    def tearDown(self):
        """
        Method to be executed when test finish. Drop the mock database.
        """
        self.db.drop_mongo_connection()

    def test_get_insert_returns_200(self):
        """
        Method to test if the /insert endpoint returns 200 in HTTP
        status code.
        """
        print("In method", self._testMethodName)
        self.assertEqual(200, self.response.status_code)

    def test_get_insert_renders_html(self):
        """
        Method to test if the /insert endpoint returns HTML.
        """
        print("In method", self._testMethodName)
        self.assertIn('text/html', self.response.content_type)

    def test_get_insert_renders_title_html(self):
        """
        Method to test if the /insert endpoint returns a HTML tag with
        title of the page.
        """
        print("In method", self._testMethodName)
        response_decoded = self.response.data.decode('utf-8')
        self.assertIn('<title>Criar nova Tarefa</title>', response_decoded)

    def test_route_insert(self):
        """
        Method to test if the /insert endpoint creates a new register
        in the database.
        """
        print("In method", self._testMethodName)
        description = 'TesteInsert'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = self.db.find_one({"description": description})

        self.assertEqual(description, task.get('description'))


class TestUpdate(unittest.TestCase):
    """
    Class to allocate the test methods of update page (/update-by-id).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
        instance and mock Database. Makes a GET HTTP request to
        /update-by-id endpoint and stores the response in a variable.
        """
        self.app_test = app.test_client()
        self.db = TaskRepository(app)
        self.response = self.app_test.get('/update-by-id/1')

    def tearDown(self):
        """
        Method to be executed when test finish. Drop the mock database.
        """
        self.db.drop_mongo_connection()

    def test_get_update_by_id_returns_200(self):
        """
        Method to test if the /update-by-id endpoint returns 200 in
        HTTP status code.
        """
        print("In method", self._testMethodName)
        self.assertEqual(200, self.response.status_code)

    def test_get_update_by_id_renders_html(self):
        """
        Method to test if the /update-by-id endpoint returns HTML.
        """
        print("In method", self._testMethodName)
        self.assertIn('text/html', self.response.content_type)

    def test_get_update_by_id_renders_title_html(self):
        """
        Method to test if the /update-by-id endpoint returns a HTML tag
        with title of the page.
        """
        print("In method", self._testMethodName)
        response_decoded = self.response.data.decode('utf-8')
        self.assertIn('<title>Atualizar Tarefa</title>', response_decoded)

    def test_route_update_by_id(self):
        """
        Method to test if the /update-by-id endpoint updates an
        existing register in the database.
        """
        print("In method", self._testMethodName)
        description = 'TesteUpdate'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = self.db.find_one({"description": description})

        description = 'TesteUpdateUpdated'
        self.app_test.put('/update-by-id/' + str(task.get('_id')),
                          data=dict(description=description))
        task = self.db.find_one({"description": description})

        self.assertEqual(description, task.get('description'))

    def test_route_change_status_by_id(self):
        """
        Method to test if the /change-status-by-id endpoint changes the
        status of an existing register in the database.
        """
        print("In method", self._testMethodName)
        description = 'TesteUpdateStatus'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = self.db.find_one({"description": description})
        self.app_test.put('/change-status-by-id/' + str(task.get('_id')))
        task = self.db.find_one({"_id": task.get('_id')})

        self.assertEqual(True, task.get('status'))


class TestDelete(unittest.TestCase):
    """
    Class to allocate the test methods of delete page (/delete-by-id).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
        instance and mock Database with register.
        """
        self.app_test = app.test_client()
        self.db = TaskRepository(app)

        self.mock_task_id = 1
        self.mock_task_description = "MockData"
        self.mock_task_status = False

        self.db.insert_one(self.mock_task_id, self.mock_task_description,
                           self.mock_task_status)

    def tearDown(self):
        """
        Method to be executed when test finish. Drop the mock database.
        """
        self.db.drop_mongo_connection()

    def test_route_delete_by_id(self):
        """
        Method to test if the /delete-by-id endpoint deletes an
        existing register in the database.
        """
        print("In method", self._testMethodName)
        task = self.db.find_one({"description": self.mock_task_description})

        self.app_test.delete('/delete-by-id/' + str(task.get('_id')))
        task = self.db.find_one({"description": self.mock_task_description})

        self.assertEqual(None, task)


class TestRepository(unittest.TestCase):
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
        instance and mock Database with register.
        """
        self.app_test = app.test_client()
        self.db = TaskRepository(app)

        self.mock_task_id = 1
        self.mock_task_description = "MockData"
        self.mock_task_status = False

        self.db.insert_one(self.mock_task_id, self.mock_task_description,
                           self.mock_task_status)

    def tearDown(self):
        """
        Method to be executed when test finish. Drop the mock database.
        """
        self.db.drop_mongo_connection()

    def test_find_returns_2(self):
        """
        Method to test if find, returns the correct amount of objects.
        """
        print("In method", self._testMethodName)
        self.db.insert_one(2, "TesteFind", True)
        query = self.db.find({}, {})
        tasks = []
        for task in query:
            tasks.append(task)
        self.assertEqual(2, len(tasks))

    def test_find_with_constraints_returns_object_2(self):
        """
        Method to test if find using description as constraint, returns
        the correct object.
        """
        print("In method", self._testMethodName)
        self.db.insert_one(2, "TestFindWithConstraints", True)
        query = self.db.find({"description": "TestFindWithConstraints"}, {})
        tasks = []
        for task in query:
            tasks.append(task)
        self.assertEqual(2, tasks[0].get('_id'))

    def test_find_with_fields_returns_all_fields(self):
        """
        Method to test if find passing the required fields, returns the
        correct object.
        """
        print("In method", self._testMethodName)
        query = self.db.find({}, {"_id": True, "description": True,
                                  "status": True})
        tasks = []
        for task in query:
            tasks.append(task)
        self.assertEqual(self.mock_task_description,
                         tasks[0].get('description'))

    def test_find_with_constraints_and_fields_returns_all_object_2(self):
        """
        Method to test if find using description as constraint, and
        passing the required fields, returns the correct object.
        """
        print("In method", self._testMethodName)
        self.db.insert_one(2, "TestFindWithConstraintsAndFields", True)
        query = \
            self.db.find({"description": "TestFindWithConstraintsAndFields"},
                         {"_id": True, "description": True,
                          "status": True})
        tasks = []
        for task in query:
            tasks.append(task)
        self.assertEqual("TestFindWithConstraintsAndFields",
                         tasks[0].get('description'))

    def test_find_one_by_id_returns_correct_object(self):
        """
        Method to test if find_one using id as constraint, returns
        the correct object.
        """
        print("In method", self._testMethodName)
        task = self.db.find_one({"_id": self.mock_task_id})
        self.assertEqual(self.mock_task_description, task.get('description'))

    def test_find_one_by_description_returns_correct_object(self):
        """
        Method to test if find_one using description as constraint,
        returns the correct object.
        """
        print("In method", self._testMethodName)
        self.db.insert_one(2, "TestFindOneByDescription", True)
        task = self.db.find_one({"description": "TestFindOneByDescription"})
        self.assertEqual("TestFindOneByDescription", task.get('description'))

    def test_insert_one(self):
        """
        Method to test if insert_one really insert the register in
        database.
        """
        print("In method", self._testMethodName)
        self.db.insert_one(2, "TesteInsert", True)
        task = self.db.find_one({"_id": 2})
        self.assertEqual("TesteInsert", task.get('description'))

    def test_update_one_by_id(self):
        """
        Method to test if update_one really update the register in
        database.
        """
        print("In method", self._testMethodName)
        self.db.update_one({"_id": self.mock_task_id},
                           {"description": "TesteUpdate"})
        task = self.db.find_one({"_id": self.mock_task_id})
        self.assertEqual("TesteUpdate", task.get('description'))

    def test_delete_one_by_id(self):
        """
        Method to test if delete_one really delete the register in
        database.
        """
        print("In method", self._testMethodName)
        self.db.delete_one({"_id": self.mock_task_id})
        task = self.db.find_one({"_id": self.mock_task_id})
        self.assertEqual(None, task)


if __name__ == '__main__':
    unittest.main()
