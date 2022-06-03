from website import create_app
from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return Flask.render_template('login.html')

if __name__ == "__main__":
    app = create_app()
    #app.run(debug=True)
    print("== Running in debug mode ==")
    app.run(host='0.0.0.0', port=5014, debug=True)
