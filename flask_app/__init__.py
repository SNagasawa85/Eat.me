from flask import Flask
app=Flask(__name__)

app.secret_key="fooAppPassword"

DATABASE = 'eat_me_db'
