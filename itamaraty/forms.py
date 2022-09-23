from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from itamaraty.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Digite um nome de usuário válido")])
    email = StringField('E-mail', validators=[DataRequired(),
                                              Email(message="Digite um endereço de e-mail válido")])
    senha = PasswordField('Senha',
                          validators=[DataRequired(),
                                      Length(6, 20, message="Digite um valor para a senha de 6 a 20 caracteres")])
    confirmacao_senha = PasswordField('Confirmar Senha',
                                      validators=[DataRequired(message="Senha diferente da preenchida anteriormente"),
                                                  EqualTo('senha', message="Senha diferente da preenchida anteriormente")])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado!')


class FormLogin(FlaskForm):
    login_email = StringField('E-mail', validators=[DataRequired(), Email(message="Digite um endereço de e-mail válido")])
    senha = PasswordField('Senha',
                          validators=[DataRequired(),
                                      Length(6, 20, message="Digite um valor para a senha de 6 a 20 caracteres")])
    lembrar_dados = BooleanField('Lembrar-me')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Digite um nome de usuário válido")])
    email = StringField('E-mail', validators=[DataRequired(),
                                              Email(message="Digite um endereço de e-mail válido")])
    foto_perfil = FileField('Atualizar Foto do Perfil', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit_editarperfil = SubmitField('Salvar')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse E-mail.')
