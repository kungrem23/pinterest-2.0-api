from flask import Flask
from bcrypt import gensalt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
salt = gensalt()
app.config['SECRET_KEY'] = '1e2e7d7f-2289-4612-ba06-1036dc86e887'
pg_host = os.getenv('PG_HOST')
