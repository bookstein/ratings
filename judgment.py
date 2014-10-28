from flask import Flask, render_template, redirect, request
import model


app = Flask(__name__)


@app.route("/")
def index():
    # session = model.connect()
    print "hello"
    user_list = session.query(model.User).limit(5).all()
    print user_list
    return render_template("user_list.html", user_list=user_list)


if __name__ == "__main__":
    session = model.connect()
    app.run(debug=True)