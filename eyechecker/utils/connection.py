from os import getenv
from urllib.parse import quote_plus as urlquote

from sqlalchemy import create_engine, Table, MetaData

def connection_url():
    """
    Function that creates a connection url to the Database.
    """
    user = getenv('DATABASE_USER')
    #password = urlquote(getenv('DATABASE_PASSWORD')) #If your database has password uncomment this line.
    host = getenv('DATABASE_HOST')
    name = getenv('DATABASE_NAME')
    #Add the password string between user and the host
    #also add :%s to before the @.
    return 'postgresql://%s@%s/%s' % (user, host, name)

engine = create_engine(connection_url())
meta = MetaData()