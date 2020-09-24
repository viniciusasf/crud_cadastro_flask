from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliente.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)


class Pessoa(db.Model):
    __tablename__='cliente'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email


class User(db.Model):
    __tablename__= 'user'
    _id = db.Column (db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    login = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)

    def __init__(self, nome, login, senha):
        self.nome=nome
        self.login=login
        self.senha=senha


db.create_all()


#@app.route('/')
#@app.route('/home')
#def home():
#    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome=request.form.get('nome')
        login=request.form.get['login']
        senha=request.form.get['senha']

        user=User(nome, login, senha)

        db.session.add(user)
        db.session.commit()

    return render_template(url_for('register.html'))



#@app.route('/login', methods=['GET', 'POST'])
#def login():
    #    if request.method == 'POST':
    #    login=request.form['login']
    #   senha = request.form['senha']

    #   user = User.query.filter_by (login=login).first()

    #   if not user or not user.verify_password(senha):
    #       return redirect(url_for('login'))

    #   login_user(user)

    #   return render_template('home')

#    return render_template('login.html')



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/cadastros')
def cadastros():
    return render_template('cadastro.html')



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome=request.form['nome']
        login=request.form['login']
        senha=request.form['senha']

        user=User(nome, login, senha)

        db.session.add(user)
        db.session.commit()

        return render_template(url_for('registro.html'))



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/cadastros')
def cadastro():
    return render_template('cadastro.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        if nome and telefone and email:
            p = Pessoa(nome, telefone, email)
            db.session.add(p)
            db.session.commit()
    return redirect(url_for('index'))


@app.route('/lista')
def lista():
    pessoas = Pessoa.query.all()
    return render_template('lista.html', pessoas=pessoas)


@app.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoa = Pessoa.query.all()
    return render_template('lista.html', pessoas=pessoa)


@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        if nome and telefone and email:
            pessoa.nome=nome
            pessoa.telefone=telefone
            pessoa.email=email

            db.session.commit()
            return redirect(url_for('lista'))

    return render_template('atualizar.html', pessoa=pessoa)



if __name__ == '__main__':
    app.run(debug=True)