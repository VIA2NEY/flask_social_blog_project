from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from urllib.parse import urlsplit


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si l'utilisateur est déjà connecté, on le redirige vers l'accueil
    if current_user.is_authenticated:
        return redirect(url_for('index'))   
    
    form = LoginForm()
    if form.validate_on_submit(): # Si le btn submit du formulaire est cliqué
        user = User.query.filter_by(username=form.username.data).first()

        # On vérifie si l'utilisateur existe et si le mot de passe est correct
        if user is None or not user.check_password(form.password.data):
            flash("Nom d'utilisateur ou mot de passe incorrect")
            return redirect(url_for('login'))
        
        # On connecte l'utilisateur
        print(f"\n the form remember me data is {form.remember_me.data} \n")
        login_user(user, remember=form.remember_me.data)

        # On redirige l'utilisateur vers la page d'accueil
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # la fonction urlsplit est de permettre de determiner si l'url 
        # est relative ou absolue c'est à dire si elle commence par http ou pas
        
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)