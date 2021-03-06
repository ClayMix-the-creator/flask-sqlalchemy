from flask import Flask, render_template
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
import os.path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    if os.path.exists('db/blogs.sqlite') is False:
        db_session.global_init("db/blogs.sqlite")
        app.run()
        user = User()
        user.name = "Пользователь 1"
        user.about = "биография пользователя 1"
        user.email = "email@email.ru"
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
    else:
        if input('This DB already exists, recreate it?? (Y/N)\n') == 'Y':
            os.remove('db/blogs.sqlite')
            db_session.global_init("db/blogs.sqlite")
            app.run()
            user = User()
            user.name = "Пользователь 1"
            user.about = "биография пользователя 1"
            user.email = "email@email.ru"
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
        else:
            pass


if __name__ == '__main__':
    main()
