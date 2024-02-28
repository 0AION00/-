from services import app
from flask import render_template

@app.route('/')
@app.route('/index')
def home():
    index = render_template('index.html')
    return index

if __name__ == '__main__':
    app.run(host = 'localhost', port = 7983)