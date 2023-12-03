from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/teori")
def teori():
    return render_template('teori.html')

@app.route("/tentang")
def tentang():
    return render_template('tentang.html')

if __name__ == "__main__":
    app.run(debug=True)
