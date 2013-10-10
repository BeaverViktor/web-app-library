from myapp import app
from myapp.library.models import Author, Book
from myapp.search.forms import SearchForm

from flask import render_template, redirect, request, url_for, flash, g
from sqlalchemy import or_

@app.route('/search/', methods = ['POST'])
def search():
    form = SearchForm(request.form)
    if form.validate():
        canon = form.canon.data
        query = form.query.data
        return redirect(url_for('search_results', canon=canon, query=query))
    flash('What are you looking for?')
    return render_template('layout.html')
    
@app.route('/search_results/<canon>/<query>/')
def search_results(canon, query):
    g.search_form.canon.data = canon
    g.search_form.query.data = query
    flash('Search results for: ' + query)
    if canon == 'library':
        results = Book.query.filter(or_(Book.name.like('%' + query + '%'),
            Book.authors.any(Author.name.like('%' + query + '%'))))
    elif canon == 'books':
        results = Book.query.filter(Book.name.like('%' + query + '%'))
    else:
        results = Author.query.filter(Author.name.like('%' + query + '%'))
    return render_template('search/search_results.html', results=results,
                           canon=canon)