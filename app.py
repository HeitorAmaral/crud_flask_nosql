from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
todo_db = client['todo']
task_collection = todo_db['task']


@app.route('/test')
def test_mongo_query():
    returned = find_next_id()
    print(returned)
    return returned


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    """
    Returns the initial HTML page of application.

    :return: Render the initial page. The index.html file.
    """
    return render_template('index.html')


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    """
    Method that creates a new Task in the database, or update it if the
     Description already exists and returns or redirect the HTML page.

    :return: If a POST HTTP request called it, returns the
     page with all registers. If not, renders the page of insert a new
      Task.
    """
    if request.method == 'POST':
        description = request.form.get('description')
        status = request.form.get('status')

        if status is None or status == 'False':
            status = False
        elif status == 'on' or status == 'True':
            status = True

        if description:
            task_exists = find_by_description(description)
            if task_exists:
                task_collection.update_one({"_id": task_exists.get('_id')}, {"$set": {"status": status}})
            else:
                task = task_collection.insert_one({"_id": find_next_id(), "description": description, "status": status})
                print(task.inserted_id)
        return redirect(url_for('find_all'))
    else:
        return render_template('insert.html')


@app.route('/find-all', methods=['GET'])
def find_all():
    """
    Method that query all the registers in the database and returns all
     the data.

    :return: Renders the page with the list of all Tasks stored in
     the database.
    """
    tasks = task_collection.find()
    return render_template('list.html', tasks=tasks)


@app.route('/delete-by-id/<int:task_id>', methods=['GET', 'DELETE'])
def delete_by_id(task_id):
    """
    Method that deletes a register of Task by identifier.

    :param task_id: (Integer) Identifier of the Task.
    :return: After deletion in database, renders the HTML page with the
     list of all Tasks.
    """
    task = find_by_id(task_id)
    task_collection.delete_one({"_id": task.get('_id')})
    return redirect(url_for('find_all'))


@app.route('/change-status-by-id/<int:task_id>', methods=['GET',
                                                          'PUT'])
def change_status_by_id(task_id):
    """
    Method that change the status of a Task by Identifier.

    :param task_id: (Integer) Identifier of the Task.
    :return: After update in database, renders the HTML page with the
     list of all Tasks.
    """
    task = find_by_id(task_id)
    task_id = task.get('_id')
    task_status = task.get('status')

    if task_status:
        task_status = False
    else:
        task_status = True

    task_collection.update_one({"_id": task_id}, {"$set": {"status": task_status}})

    return redirect(url_for('find_all'))


@app.route('/update-by-id/<int:task_id>', methods=['GET', 'POST', 'PUT'])
def update_by_id(task_id):
    """
    Method that updates a Task in the database by Identifier.

    :param task_id: (Integer) Identifier of the Task.
    :return: If a POST or PUT HTTP method request called the method,
     and the process is executed with success, renders the HTML page
     with the list of all Tasks. If not, returns the HTML page with
     the form to update, with validation messages or not.
    """
    task = find_by_id(task_id)
    description = request.form.get('description')

    if request.method == 'POST' or request.method == 'PUT':
        if description:
            task_exists = find_by_description(description)
            if task_exists:
                return render_template('update.html', task=task,
                                       message='Já existe um registro com'
                                               ' essa descrição criado.'
                                               ' Escolha outra descricão.')
            else:
                task_collection.update_one({"_id": task.get('_id')}, {"$set": {"description": description}})
        return redirect(url_for('find_all'))
    return render_template('update.html', task=task)


def find_by_id(task_id):
    """
    Method that query a Task in the Database by Identifier.

    :param task_id: (Integer) Identifier of the Task.
    :return: Returns a Task.
    """

    return task_collection.find_one({"_id": task_id})


def find_by_description(description):
    """
    Method that query a Task in the Database by Description.

    :param description: (String) Description of the Task.
    :return: Returns a Task.
    """
    return task_collection.find_one({"description": description})


def find_next_id():
    """
    Method that returns the next Identifier available to be used.
     Querys the max Identifier in the Database, and sums one more.

    :return: Returns the Integer Identifier to be used.
    """
    query = task_collection.find({}, {"_id": 1}).sort("_id", -1).limit(1)

    for obj in query:
        return obj.get('_id') + 1
    else:
        return 1


if __name__ == '__main__':
    app.run(host='0.0.0.0')
