from os import getenv
from urllib import quote_plus as urlquote

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

def connection_url():
    user = getenv('DATABASE_USER')
    password = urlquote(getenv('DATABASE_PASSWORD'))
    host = getenv('DATABASE_HOST')
    name = getenv('DATABASE_NAME')
    return 'postgresql://%s:%s@%s/%s' % (user, password, host, name)

engine = create_engine(connection_url())
meta = MetaData()