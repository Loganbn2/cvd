from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def member_portal():
    return render_template('member_portal.html')

@app.route('/reset_password.html')
def reset_password():
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
