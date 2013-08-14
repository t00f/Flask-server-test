# -*- coding: utf-8 -*-

__all__ = ['LocalConfig']

class LocalConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'