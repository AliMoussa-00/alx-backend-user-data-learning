#!/usr/bin/env python3
'''Sessions in database'''


from models.base import Base


class UserSession(Base):
    '''class to store session Ids'''

    def __init__(self, *args: list, **kwargs: dict):
        '''initializing the instance'''
        super().__init__(*args, **kwargs)

        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
