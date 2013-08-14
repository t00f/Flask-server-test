# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from __init__ import app

from models import Area
from elixir import session, create_all, drop_all

from datetime import datetime

manager = Manager(app)

@manager.command
def install():
    """ Install database an default values """

    # Drop tables
    print("Dropping all tables...")
    drop_all()

    # Create tables
    print("Creating all tables...")
    create_all()

    # Add fixtures
    print("Adding default values...")
    for i in range (0, 10000):
        Area(id=i, name=u"Area" + str(i), comment="")

    session.commit()

    # Installation finished
    print("Installation success !")

if __name__ == "__main__":
    manager.run()
