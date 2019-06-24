from flask import Flask
app = Flask(__name__)

# ------------------------------------------------------------------
@app.route("/")
def hello():
    str_out = "<h2>Hello World!</h2>"
    str_out += "こんにちは。<p />"
    str_out += "Nov/09/2018 PM 16:51<p />"
    return str_out

# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run()
