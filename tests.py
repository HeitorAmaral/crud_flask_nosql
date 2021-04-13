import unittest
from app import app, find_by_description, find_by_id


class TestIndex(unittest.TestCase):
    """
    Class to allocate the test methods of index page (/index).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
         instance and Database, makes a GET HTTP request to /index
         endpoint and stores the response in a variable.
        """
        self.app_test = app.test_client()
        db.create_all()
        self.response = self.app_test.get('/')

    def tearDown(self):
        """
        Method that will be executed after tests. Remove the session
         and drop all tables of test database.
        """
        db.session.remove()
        db.drop_all()

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
        Method that will be executed before tests. Creates test
         instance and Database, makes a GET HTTP request to /find-all
         endpoint and stores the response in a variable.
        """
        self.app_test = app.test_client()
        db.create_all()
        self.response = self.app_test.get('/find-all')

    def tearDown(self):
        """
        Method that will be executed after tests.
        """
        db.session.remove()
        db.drop_all()

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

    def test_get_find_by_id_returns_correct_register(self):
        """
        Method to test the method find-by-id returns correct register.
        """
        print("In method", self._testMethodName)
        description = 'TesteFindById'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = find_by_id(1)
        self.assertEqual(description, task.description)

    def test_get_find_by_description_returns_correct_register(self):
        """
        Method to test the method find-by-description returns correct
         register.
        """
        print("In method", self._testMethodName)
        description = 'TesteFindByDescription'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = find_by_description(description)
        self.assertEqual(description, task.description)


class TestInsert(unittest.TestCase):
    """
    Class to allocate the test methods of insert page (/insert).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates test
         instance and Database, makes a GET HTTP request to /insert
         endpoint and stores the response in a variable.
        """
        self.app_test = app.test_client()
        db.create_all()
        self.response = self.app_test.get('/insert')

    def tearDown(self):
        """
        Method that will be executed after tests.
        """
        db.session.remove()
        db.drop_all()

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

    def test_create_register_in_database(self):
        """
        Method to test if the /insert endpoint creates a new register
         in the database.
        """
        print("In method", self._testMethodName)
        description = 'TesteInsert'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = find_by_description(description)

        self.assertEqual(description, task.description)
        self.app_test.delete('/delete-by-id/' + str(task._id))


class TestUpdate(unittest.TestCase):
    """
    Class to allocate the test methods of update page (/update-by-id).
    """
    def setUp(self):
        """
        Method that will be executed before tests. Creates a test
         instance and database.
        """
        self.app_test = app.test_client()
        db.create_all()

    def tearDown(self):
        """
        Method that will be executed after tests.
        """
        db.session.remove()
        db.drop_all()

    def test_update_register_in_database(self):
        """
        Method to test if the /update-by-id endpoint updates an
         existing register in the database.
        """
        print("In method", self._testMethodName)
        description = 'TesteUpdate'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = find_by_description(description)

        description = 'TesteUpdateUpdated'
        self.app_test.put('/update-by-id/' + str(task._id),
                          data=dict(description=description))
        task = find_by_description(description)

        self.assertEqual(description, task.description)
        self.app_test.delete('/delete-by-id/' + str(task._id))

    def test_update_status_of_register_in_database(self):
        """
        Method to test if the /change-status-by-id endpoint changes the
         status of an existing register in the database.
        """
        print("In method", self._testMethodName)
        description = 'TesteUpdateStatus'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = find_by_description(description)
        self.app_test.put('/change-status-by-id/' + str(task._id))
        task = find_by_id(task._id)

        self.assertEqual(True, task.status)
        self.app_test.delete('/delete-by-id/' + str(task._id))


class TestDelete(unittest.TestCase):
    """
    Class to allocate the test methods of delete page (/delete-by-id).
    """
    def setUp(self):
        """
        Method that will be executed before tests.
        """
        self.app_test = app.test_client()
        db.create_all()

    def tearDown(self):
        """
        Method that will be executed after tests.
        """
        db.session.remove()
        db.drop_all()

    def test_delete_register_in_database(self):
        """
        Method to test if the /delete-by-id endpoint deletes an
         existing register in the database.
        """
        print("In method", self._testMethodName)
        description = 'TesteDelete'
        status = False
        self.app_test.post('/insert', data=dict(description=description,
                                                status=status))
        task = find_by_description(description)

        self.app_test.delete('/delete-by-id/' + str(task._id))
        task = find_by_description(description)

        self.assertEqual(None, task)


if __name__ == '__main__':
    unittest.main()
