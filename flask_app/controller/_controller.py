# -*- coding: utf-8 -*-
"""

"""

from __future__ import unicode_literals, print_function, absolute_import, \
    division

import os
import re

from flask import render_template, request, make_response
from flask._compat import string_types
from werkzeug.datastructures import CombinedMultiDict, MultiDict
from werkzeug.exceptions import NotImplemented as HTTPNotImplemented
from werkzeug.utils import cached_property
from werkzeug.wrappers import BaseResponse

from .route import ControllerRoute
from .response import *


class Controller(ControllerResponse, ControllerRoute):

    decorators = []

    resource = None

    template_dir = None

    __split_by_capital = re.compile('([A-Z][a-z]+)+')

    @cached_property
    def template_dir(self):
        parts = self.__split_by_capital.split(self.__class__.__name__)
        return os.path.join(*[item.lower() for item in parts])

    def __dummy(self, *args, **kwargs):
        """For internal usage and do nothing

        :param args:
        :param kwargs:
        :return:
        """
        pass

    def _before(self, *args, **kwargs):
        """ Use it when you want to run things before running the class methods

        :param args:
        :param kwargs:
        :return:
        """
        pass

    def _after(self, *args, **kwargs):
        """ Do something before rendering the output.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    def dispatch_request(self, func_name, *args, **kwargs):
        """


        :param func_name:
        :param args:
        :param kwargs:
        :return: :raise HTTPNotImplemented:
        """
        func = getattr(self, func_name, None)
        if not func:
            raise HTTPNotImplemented()

        self._before(*args, **kwargs)
        action = func.__name__
        getattr(self, 'before_' + action, self.__dummy)(*args, **kwargs)
        result = func(*args, **kwargs)
        getattr(self, 'after_' + action, self.__dummy)(*args, **kwargs)
        self._after(*args, **kwargs)

        if not result:
            result = self.response.empty()

        if isinstance(result, BaseResponse):
            return result

        if not isinstance(result, (list, set, tuple)):
            return self.make_response(result)

        return self.make_response(*result)

    def render_view(self, view_name_or_list, view_data, status=200, *args,
                    **kwargs):
        """ Renders view in addition adds controller name in lower case as
        directory where file should be. To disable behavior adding class name
        please use '//' at the beginning of your template name
        for e.g. '//path/some.html' -> 'path/some.html'

        :param name: file name or list of file names for e.g. index.html
        :param view_data: dictionary with data which needed to render view
        :param status: int status code default 200
        :param args:
        :param kwargs:
        :return:
        """

        assert view_name_or_list, "View name must not be empty"

        if isinstance(view_name_or_list, string_types):
            view_name_or_list = [view_name_or_list]
        views = []
        for view_name in view_name_or_list:
            views.append(os.path.join(self.template_dir, view_name))
            views.append(view_name)

        return make_response(
            render_template(views, **view_data),
            status,
            *args,
            **kwargs
        )

    def render_nothing(self):
        """ Will generate valid empty response with 204 http status code

        :return:
        """
        return self.response.empty()

    @cached_property
    def request_values(self):
        """ Get requested query parameters including all GET and POST

        :return: MultiDict
        """
        json_data = request.get_json()
        if not json_data:
            json_data = []

        args = []
        for d in json_data, request.values:
            if not isinstance(d, MultiDict):
                d = MultiDict(d)
            args.append(d)
        return CombinedMultiDict(args)
