from myapp import app
from myapp.decorators import login_required
from myapp.library.models import Author, Book
from myapp.library.forms import AuthorForm, BookForm
from myapp.database import db_session

from flask import render_template, redirect, request, url_for, flash

@app.route('/')
def index():
    books_amount = Book.query.count()
    authors_amount = Author.query.count()
    return render_template('library/index.html', books_amount=books_amount,
                           authors_amount=authors_amount)

@app.route('/books/<id>/')
@app.route('/books/')
def view_book(id=None):
    error = None
    if id:
        book = Book.query.get(id)
        if not book:
            error = 'Sorry, we don\'t have the book with id {0}.'.format(id)
        return render_template('library/view_book.html', book=book, error=error)
    books = Book.query.all()
    return render_template('library/list_books.html', books=books)

@app.route('/authors/<id>/')
@app.route('/authors/')
def view_author(id=None):
    error = None
    if id:
        author = Author.query.get(id)
        if not author:
            error = 'Sorry, we don\'t have the author with id {0}.'.format(id)
        return render_template('library/view_author.html', author=author,
                               error=error)
    authors = sorted(Author.query.all(),
                     key=lambda author: author.name.split()[-1])
    return render_template('library/list_authors.html', authors=authors)

@app.route('/authors/add/', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AuthorForm(request.form)
    if request.method == 'POST' and form.validate():
        author = Author(form.name.data)
        db_session.add(author)
        db_session.commit()
        flash('The author was added to the Library.')
        return redirect(url_for('view_author', id=author.id))
    return render_template('library/add_author.html', form=form)

@app.route('/authors/<id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_author(id):
    error = None
    author = Author.query.get(id)
    if not author:
        error = 'Sorry, we don\'t have the author with id {0}.'.format(id)
    form = AuthorForm(request.form, obj=author)
    if request.method == 'POST' and form.validate():
        form.populate_obj(author)
        db_session.add(author)
        db_session.commit()
        return redirect(url_for('view_author', id=author.id))
    return render_template('library/edit_author.html', form=form, author=author,
                           error=error)

@app.route('/authors/<id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_author(id):
    error = None
    author = Author.query.get(id)
    if not author:
        error = 'Sorry, we don\'t have the author with id {0}.'.format(id)
    if request.method == 'POST':
        db_session.delete(author)
        db_session.commit()
        flash('The author and his books were deleted.')
        return redirect(url_for('view_author'))
    return render_template('library/delete_author.html', author=author,
                           error=error)

@app.route('/books/add/', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm(request.form)
    form.authors.choices = sorted([(a.id, a.name) for a in Author.query.all()],
        key=lambda author: author[1].split()[-1])
    if request.method == 'POST' and form.validate():
        book = Book(form.name.data)
        for id in form.authors.data:
            book.authors.append(Author.query.get(id))
        db_session.add(book)
        db_session.commit()
        flash('The book was added to the Library.')
        return redirect(url_for('view_book', id=book.id))
    return render_template('library/add_book.html', form=form)

@app.route('/books/<id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    error = None
    book = Book.query.get(id)
    if not book:
        error = 'Sorry, we don\'t have the book with id {0}.'.format(id)
    form = BookForm(request.form, obj=book)
    form.authors.choices = sorted([(a.id, a.name) for a in Author.query.all()],
        key=lambda author: author[1].split()[-1])
    if request.method == 'POST' and form.validate():
        book.name = form.name.data
        book.authors = []
        for id in form.authors.data:
            book.authors.append(Author.query.get(id))
        db_session.add(book)
        db_session.commit()
        return redirect(url_for('view_book', id=book.id))
    form.authors.data = [a.id for a in book.authors]
    return render_template('library/edit_book.html', form=form, book=book,
                           error=error)

@app.route('/books/<id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_book(id):
    error = None
    book = Book.query.get(id)
    if not book:
        error = 'Sorry, we don\'t have the book with id {0}.'.format(id)
    if request.method == 'POST':
        db_session.delete(book)
        db_session.commit()
        flash('The book was deleted.')
        return redirect(url_for('view_book'))
    return render_template('library/delete_book.html', book=book, error=error)