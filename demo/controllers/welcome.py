# -*- coding: utf-8 -*-
"""

"""

from __future__ import unicode_literals, print_function, absolute_import, \
    division

from flask_app.controller import Controller, route, post_method, http_method, JsonResponse, \
    XmlResponse, get_method
from functools import wraps
from pydoc import render_doc, doc, plain
from flask import current_app, Response, request, session
from werkzeug.utils import redirect
from flask_app.helpers.url import build_url


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if session.get('auth'):
            return f(*args, **kwargs)
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        session['auth'] = auth
        return f(*args, **kwargs)
    return decorated

class Welcome(Controller):

    ROUTE_BASE = ''

    def _before(self, *args, **kwargs):
        print(args)

    @http_method('/<int:ddd>')
    def post(self, ddd=0):
        """

        :param ddd:
        :return:
        """
        return XmlResponse({'asa': 'dfd'}, 200)

    @http_method('/', defaults={'ddd': None})
    @http_method('/<int:ddd>')
    def get(self, ddd):
        return {}, 200

    @http_method('/<int:ddd>')
    def prepost(self, ddd):
        return {}, 200

    @route('/welcome')
    @route('/')
    def index(self):
        """

        :return:
        """
        return redirect(build_url('Welcome:about_us'))
        #return self.render_view('index.html', {'title': "Index"})

    @post_method('/post')
    def some_function(self):
        return self.response.empty()  # .as_requested({}, 200)

    @route('/about-us')
    def about_us(self):
        #['docs.html', 'index.html']
        return self.render_view(['//docs.html', 'index.html'], {'title': "About US"})

    @requires_auth
    @get_method('/docs/')
    def docs(self):
        print(build_url('test.Test:index'))
        def routes():
            for key, view_function in current_app.view_functions.items():
                yield (key, plain(render_doc(view_function, title="%s")))

        return self.render_view('docs.html', {'gen_docs': routes()})