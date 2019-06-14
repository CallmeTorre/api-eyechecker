"""
Module for containing all required initialization logic.

It exposes a function that should ALWAYS be indepotent,
which means that it can be called one or possible multiple
times without creating fatal errors (other than those originated
by latency.)
"""
import sys
import logging
import logging.config
import os
from os.path import join, dirname
from dotenv import load_dotenv

ALWAYS_REQUIRED = {'DATABASE_USER',
                   'DATABASE_PASSWORD',
                   'DATABASE_HOST',
                   'DATABASE_NAME',
                   'ENV_SELECTOR',
                   'FLASK_ENV'}

def load():
    """Load and check all the necessary configuration options"""
    # Load environment variables from envfile if present
    ENVFILE_PATH = join(dirname(__file__), '..', '.env')
    load_dotenv(ENVFILE_PATH)

    # Load logging setup
    LOGFILE_PATH = join(dirname(__file__), 'logging.conf')
    logging.config.fileConfig(LOGFILE_PATH)

    reqs = set()

    if os.getenv('ENV_SELECTOR') == 'dev':
        required = reqs.union(ALWAYS_REQUIRED)
    else:
        required = reqs.union(ALWAYS_REQUIRED)

    real = set(os.environ.keys())

    bad = False
    diff = required - real
    if len(diff) > 0:
        bad = True
        logging.error('Missing environment variables: %s', ', '.join(diff))

    if bad:
        sys.exit(1)
    else:
        logging.info('All environment variables are valid.')