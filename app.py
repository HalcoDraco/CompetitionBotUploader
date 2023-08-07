from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/update_code')
def update_code():
    return render_template('update_code.html')

if __name__ == '__main__':
    app.run()
