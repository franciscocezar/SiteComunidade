from flask import render_template, redirect, url_for, request, flash
from itamaraty import app, database, bcrypt
from itamaraty.forms import FormLogin, FormCriarConta, FormEditarPerfil
from itamaraty.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required

lista_usuarios = ['Francisco', 'Pedro', 'Nathalia', 'Ana', 'Ian']


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
@login_required
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if 'botao_submit_login' in request.form:
        if form_login.validate_on_submit():
            usuario = Usuario.query.filter_by(email=form_login.login_email.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario, remember=form_login.lembrar_dados.data)
                flash(f'Login feito com sucesso! {usuario.username}', 'alert-success')
                redirects_seguros = ['/', '/contato', '/usuarios', '/perfil', '/login', '/post/criar', '/perfil/editar']
                par_next = request.args.get('next')
                if par_next in redirects_seguros:
                    return redirect(par_next)
                else:
                    return redirect(url_for('home'))
            else:
                flash(f'E-mail ou Senha Incorreto!', 'alert-danger')

    if 'botao_submit_criarconta' in request.form:
        if form_criarconta.validate_on_submit():
            senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
            usuario = Usuario(username=form_criarconta.username.data,
                              email=form_criarconta.email.data, senha=senha_cript)
            database.session.add(usuario)
            database.session.commit()
            flash(f'Conta criada com sucesso! {form_criarconta.email.data}', 'alert-success')
            return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')


@app.route('/perfil/editar', methods=['GET', 'POST'])  # páginas que têm formulário precisa do methods=['GET','POST']
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        database.session.commit()
        flash(f'Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)
