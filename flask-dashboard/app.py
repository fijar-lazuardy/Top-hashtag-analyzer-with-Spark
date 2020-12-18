from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    data = {}
    # Fetch data from mongodb here

    return render_template('index.html', data=data)

@app.route('/fetch-data')
def fetch_data():
    return 0

if __name__ == "__main__":
    app.run(port=5000)