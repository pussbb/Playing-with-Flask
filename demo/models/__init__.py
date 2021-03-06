# -*- coding: utf-8 -*-
"""

"""

from __future__ import unicode_literals, print_function, absolute_import, \
    division

from .. import DB
from flask_app.model import BaseModel, BaseReadOnlyModel


class DbModel(BaseModel, DB.Model):
    __abstract__ = True

class ReadOnly(DbModel, BaseReadOnlyModel):
    __abstract__ = True
