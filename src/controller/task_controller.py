"""
Controller/View methods and operations
"""
from flask import render_template, request, url_for, redirect
from src import app
from src.repository.task_repository import TaskRepository


db = TaskRepository(app)


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    """
    Returns the initial HTML page of application.

    :return: Renders the index.html file.
    :rtype: html
    """
    return render_template('index.html')


@app.route('/find-all', methods=['GET'])
def find_all():
    """
    Method that query all the registers in the database and returns all
    the data.

    :return: Renders the page with the list of all Tasks stored in the
    database.
    :rtype: html
    """

    tasks = db.find({}, {"_id": True, "description": True,
                         "status": True}).sort("_id", 1)
    return render_template('list.html', tasks=tasks)


def find_next_available_id():
    """
    Method that returns the next Identifier available to be used.
    Query the max Identifier in the Database, and increase one more.

    :return: Integer Identifier available to be use.
    :rtype: int
    """
    query = db.find({}, {"_id": True}).sort("_id", -1).limit(1)

    for obj in query:
        return obj.get('_id') + 1
    else:
        return 1


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    """
    Method that creates a new Task, or update it if the Description
    already exists and returns or redirect the HTML page.

    :return: If a POST HTTP request called it, and no validation error
    happens, returns the page with all registers. If not, renders the
    page of insert a new Task.
    :rtype: html
    """
    if request.method == 'POST':
        description = request.form.get('description')
        status = request.form.get('status')

        if status is None or status == 'False':
            status = False
        elif status == 'on' or status == 'True':
            status = True

        if description:
            task_exists = db.find_one({"description": description})
            if task_exists:
                db.update_one({"_id": task_exists.get('_id')},
                              {"status": status})
            else:
                db.insert_one(find_next_available_id(), description,
                              status)
        else:
            return render_template('insert.html',
                                   message='É necessário preencher a'
                                           ' Descrição da Tarefa.'
                                           '  Preencha o campo'
                                           ' Descrição.')

        return redirect(url_for('find_all'))
    else:
        return render_template('insert.html')


@app.route('/delete-by-id/<int:task_id>', methods=['GET', 'DELETE'])
def delete_by_id(task_id):
    """
    Method that deletes a register of Task by identifier, and returns a
    HTML page with the list of all Tasks.

    :param task_id: Identifier of the Task.
    :type task_id: int
    :return: HTML page with the list all Tasks.
    :rtype: html
    """

    db.delete_one({"_id": task_id})
    return redirect(url_for('find_all'))


@app.route('/update-by-id/<int:task_id>', methods=['GET', 'POST', 'PUT'])
def update_by_id(task_id):
    """
    Method that updates a Task by Identifier and returns or redirect
    the HTML page.

    :param task_id: Identifier of the Task.
    :type task_id: int
    :return: If a POST or PUT HTTP method request called the method,
    and the process is executed with success, renders the HTML page
    with the list of all Tasks. If not, returns the HTML page with
    the form to update, with validation messages or not.
    :rtype: html
    """
    task = db.find_one({"_id": task_id})
    description = request.form.get('description')

    if request.method == 'POST' or request.method == 'PUT':
        if description:
            task_exists = db.find_one({"description": description})
            if task_exists and (task_exists.get('_id') != task.get('_id')):
                return \
                    render_template('update.html', task=task,
                                    message='Já existe um registro de Tarefa'
                                            ' com a descrição '
                                            + task_exists.get('description')
                                            + ' criado. Escolha outra '
                                              ' Descrição.')
            else:
                db.update_one({"_id": task_id}, {"description": description})
        else:
            return render_template('update.html', task=task,
                                   message='É necessário preencher a'
                                           ' Descrição da Tarefa.'
                                           ' Preencha o campo'
                                           ' Descrição.')
        return redirect(url_for('find_all'))
    return render_template('update.html', task=task)


@app.route('/change-status-by-id/<int:task_id>', methods=['GET', 'PUT'])
def change_status_by_id(task_id):
    """
    Method that change the status of a Task by Identifier, and returns
    a HTML page with the list of all Tasks.

    :param task_id: Identifier of the Task
    :type task_id: int
    :return: Renders the HTML page with the list of all Tasks.
    :rtype: html
    """
    task = db.find_one({"_id": task_id})
    task_id = task.get('_id')
    task_status = task.get('status')

    if task_status:
        task_status = False
    else:
        task_status = True

    db.update_one({"_id": task_id}, {"status": task_status})

    return redirect(url_for('find_all'))
