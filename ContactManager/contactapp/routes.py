import secrets
import os
from contactapp import app
from flask import flash, render_template, url_for, redirect, request, abort
from contactapp.forms.login import Login
from contactapp.forms.account import AccountForm
from contactapp.forms.book_form import BookForm
from contactapp.models import User, Book
from contactapp import db, bcrypt
from contactapp.forms.register import RegisterationForm
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required

library_books = []

#Home comment
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title="Home", message="This message should display in home page")

@app.route('/manager')
@login_required
def book_manager():
    books = Book.query.paginate(per_page=1)
    return render_template('manager.html', title="Book Manager", books=books)

@app.route('/about')
def about_page():
    return render_template('about.html', title="About Us", message="This about message should display in about page")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect((url_for('home')))

    form = RegisterationForm()
    if form.is_submitted():
        if form.validate_on_submit():
            enc_password = bcrypt.generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=enc_password)
            db.session.add(user)
            db.session.commit()
            flash(f"Account is successfully created for {form.username.data}. Please login.", "success")
            return redirect(url_for('login'))
        else:
            flash(f"Account is not created for {form.username.data}", "danger")
    return render_template('register.html', title="Register Page", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect((url_for('home')))
    login_form = Login()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if (user and bcrypt.check_password_hash(user.password, login_form.password.data)):
            login_user(user, remember=login_form.remember_me.data)
            flash(f"Welcome {user.username}", 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Incorrect Username / Password", 'danger')
    return render_template('login.html', title='Login Page', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    account_form = AccountForm()
    if request.method == 'GET':
        account_form.username.data = current_user.username
    elif request.method == 'POST':
        if account_form.validate_on_submit():
            random_text = secrets.token_hex(8)
            profile_file = account_form.profile_picture.data

            _, file_ext = os.path.splitext(profile_file.filename)
            profile_picture_to_be_uploaded = random_text + file_ext
            picture_path = app.root_path + '/static/images/profile_images/' + profile_picture_to_be_uploaded

            img = Image.open(profile_file)
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(picture_path)

            current_user.profile_image = profile_picture_to_be_uploaded
            current_user.username = account_form.username.data
            db.session.commit()
            flash(f"Account updated.")
    return render_template('account.html', title='Account Page', form=account_form)

@app.route('/book/register', methods=['GET', 'POST'])
def add_book():
    add_book_form = BookForm()
    if add_book_form.validate_on_submit():
        book = Book(name=add_book_form.book_name.data, author=add_book_form.book_author.data, user_id=current_user.id)
        db.session.add(book)
        db.session.commit()
        flash(f"Book successfully added.")
    return render_template('book/book.html', title="Add Book", form=add_book_form)

@app.route('/book/<int:book_id>/update', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if current_user != book.user:
        abort(403)
        flash(f"You don't have access to edit this")
        return redirect(url_for('book_manager'))
    update_book_form = BookForm()
    update_book_form.submit.label.text = 'Update Book'
    if update_book_form.validate_on_submit():
        book.name = update_book_form.book_name.data
        book.author = update_book_form.book_author.data
        db.session.commit()
        flash(f"Book successfully updated.")
        return redirect(url_for('book_manager'))
    else:
        update_book_form.book_name.data = book.name
        update_book_form.book_author.data = book.author
    return render_template('book/book.html', title="Update Book", form=update_book_form)

@app.route('/book/<int:book_id>/delete')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if current_user != book.user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book_manager'))

@app.route('/book/<int:book_id>/delete/confirmation')
def delete_book_confirmation(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book/delete_confirmation.html', title="Update Book", book = book )
