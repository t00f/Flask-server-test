# -*- coding: utf-8 -*-

from datetime import datetime
from elixir import Entity, Field, Unicode, Boolean, OneToMany, ManyToOne
from elixir import setup_all, Entity, Field, DateTime, using_options, using_options_defaults, Unicode
from sqlalchemy.sql.expression import func


__all__ = ['Area']


class LoggedEntity(Entity):
    """ This class gives to every class a creation_date and modify_date for the object

        :var cdate: *DateTime* creation of the ressource
        :var mdate: *DateTime* last modification of the ressource
    """
    using_options(abstract=True)
    using_options_defaults(shortnames=True)
    cdate   = Field(DateTime, default=func.now())
    mdate   = Field(DateTime, default=func.now(), onupdate=datetime.now)

    def to_dict(self):
        my_dict = dict()
        my_dict['cdate'] = self.cdate.isoformat()
        my_dict['mdate'] = self.mdate.isoformat()

        return my_dict

class Area(LoggedEntity):
    """ Class Area

        :var id:  *primary_key* id of the area
        :var name: *Unicode(100)* name of the area
        :var comment: *Unicode(100)* comment of the area
        :var rooms: *Room[]* rooms of the area
        :var sanitary_status: *SanitaryStatus[]* sanitary_status of the area

    """

    name            = Field(Unicode(100), nullable=False)
    comment         = Field(Unicode(100), nullable= True)

    def __repr__(self):
        return 'Area : %r %r' % (self.name, self.id)

    def to_dict(self):
        my_dict = LoggedEntity.to_dict(self)
        my_dict['id'] = self.id
        my_dict['name'] = self.name
        my_dict['comment'] = self.comment
        return my_dict

setup_all()