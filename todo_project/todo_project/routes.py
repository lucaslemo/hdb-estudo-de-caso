from flask import render_template, url_for, flash, redirect, request

from todo_project import app, db, bcrypt, metrics

# Import the forms
from todo_project.forms import (LoginForm, RegistrationForm, UpdateUserInfoForm, 
                                UpdateUserPassword, TaskForm, UpdateTaskForm)

# Import the Models
from todo_project.models import User, Task

# Import 
from flask_login import login_required, current_user, login_user, logout_user

metrics.register_default(
    metrics.summary(
        'request_processing_seconds', 
        'Time spent processing request', 
        labels={'route': lambda: request.endpoint}
    )
)

@app.errorhandler(404)
def error_404(error):
    return (render_template('errors/404.html'), 404)

@app.errorhandler(403)
def error_403(error):
    return (render_template('errors/403.html'), 403)

@app.errorhandler(500)
def error_500(error):
    return (render_template('errors/500.html'), 500)


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['POST', 'GET'])
@metrics.counter('login_requests', 'Número de requisições de login', labels={'status': lambda: request.method})
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))

    form = LoginForm()
    # After you submit the form
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check if the user exists and the password is valid
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            task_form = TaskForm()
            flash('Login Successful', 'success')
            app.logger.info(f'Sucesso no login para o usuário: {form.username.data}')
            return redirect(url_for('all_tasks'))
        else:
            app.logger.warning(f'Falha na tentativa de login para o usuário: {form.username.data}. Erro: Credenciais não correspondem')
            flash('Login Unsuccessful. Please check Username Or Password', 'danger')
    elif request.method == 'POST':
        app.logger.warning(f'Falha na tentativa de login para o usuário: {form.username.data}. Erro: {form.errors}')

    return render_template('login.html', title='Login', form=form)
    

@app.route("/logout")
@metrics.counter('logout_requests_total', 'Número de requisições de logout', labels={'method': lambda: request.method})
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=['POST', 'GET'])
@metrics.counter('register_requests_total', 'Número de requisições de cadastro', labels={'method': lambda: request.method, 'status': lambda: request.method})
def register():
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}', 'success')
        app.logger.info(f'Sucesso no cadastro do usuário: {form.username.data}')
        return redirect(url_for('login'))
    
    elif request.method == 'POST':
        app.logger.warning(f'Falha na tentativa de cadastro do usuário: {form.username.data}. Erro: {form.errors}')

    return render_template('register.html', title='Register', form=form)


@app.route("/all_tasks")
@login_required
@metrics.counter('all_tasks_requests_total', 'Número de requisições para visualização de todas as tarefas', labels={'method': lambda: request.method})
def all_tasks():
    tasks = User.query.filter_by(username=current_user.username).first().tasks
    app.logger.info(f'Visualização das lista de tarefas do usuário: {current_user.username}')
    return render_template('all_tasks.html', title='All Tasks', tasks=tasks)


@app.route("/add_task", methods=['POST', 'GET'])
@login_required
@metrics.counter('add_task_requests_total', 'Número de requisições para adicionar tarefa', labels={'method': lambda: request.method, 'status': lambda: request.method})
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(content=form.task_name.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task Created', 'success')
        app.logger.info(f'Sucesso na criação da tarefa: {form.task_name.data}, pelo usuário: {current_user.username}')
        return redirect(url_for('add_task'))
    
    elif request.method == 'POST':
        app.logger.warning(f'Falha na criação da tarefa: {form.task_name.data}, pelo usuário: {current_user.username}. Erro: {form.errors}')

    return render_template('add_task.html', form=form, title='Add Task')


@app.route("/all_tasks/<int:task_id>/update_task", methods=['GET', 'POST'])
@login_required
@metrics.counter('update_task_requests_total', 'Número de requisições para atualizar tarefa', labels={'method': lambda: request.method, 'status': lambda: request.method})
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = UpdateTaskForm()
    if form.validate_on_submit():
        if form.task_name.data != task.content:
            task.content = form.task_name.data
            db.session.commit()
            flash('Task Updated', 'success')
            app.logger.info(f'Sucesso na atualização da tarefa: {form.task_name.data}, pelo usuário: {current_user.username}')
            return redirect(url_for('all_tasks'))
        else:
            flash('No Changes Made', 'warning')
            return redirect(url_for('all_tasks'))
        
    elif request.method == 'POST':
        app.logger.warning(f'Falha na atualização da tarefa: {form.task_name.data}, pelo usuário: {current_user.username}. Erro: {form.errors}')

    elif request.method == 'GET':
        form.task_name.data = task.content

    return render_template('add_task.html', title='Update Task', form=form)


@app.route("/all_tasks/<int:task_id>/delete_task")
@login_required
@metrics.counter('delete_task_requests_total', 'Número de requisições para deletar tarefa', labels={'method': lambda: request.method, 'status': lambda: request.method})
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_name = task.content
    db.session.delete(task)
    db.session.commit()
    flash('Task Deleted', 'info')
    app.logger.info(f'Sucesso na exclusão da tarefa: {task_name}, pelo usuário: {current_user.username}')
    return redirect(url_for('all_tasks'))


@app.route("/account", methods=['POST', 'GET'])
@login_required
@metrics.counter('account_requests_total', 'Número de requisições para visualização/atualização de conta', labels={'method': lambda: request.method, 'status': lambda: request.method})
def account():
    form = UpdateUserInfoForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:
            old_name = current_user.username
            current_user.username = form.username.data
            db.session.commit()
            flash('Username Updated Successfully', 'success')
            app.logger.info(f'Sucesso na atualização do usuário: {old_name} para: {current_user.username}')
            return redirect(url_for('account'))
        
    elif request.method == 'POST':
        app.logger.warning(f'Falha na atualização do usuário: {current_user.username} para: {form.username.data}. Erro: {form.errors}')

    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', title='Account Settings', form=form)


@app.route("/account/change_password", methods=['POST', 'GET'])
@login_required
@metrics.counter('change_password_requests_total', 'Número de requisições para mudança de senha', labels={'method': lambda: request.method, 'status': lambda: request.method})
def change_password():
    form = UpdateUserPassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password Changed Successfully', 'success')
            app.logger.info(f'Sucesso na atualização da senha do usuário: {current_user.username}')
            redirect(url_for('account'))
        else:
            flash('Please Enter Correct Password', 'danger')
            app.logger.warning(f'Falha na atualização da senha do usuário: {current_user.username}. Erro: Senha antiga incorreta')
    elif request.method == 'POST':
            app.logger.warning(f'Falha na atualização da senha do usuário: {current_user.username}. Erro: {form.errors}')
    return render_template('change_password.html', title='Change Password', form=form)

