from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def appgoeshere():
    pass






if __name__=="__main__":
    app.run()