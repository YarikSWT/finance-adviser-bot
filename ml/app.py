from flask import Flask

app = Flask(__name__)

@app.route('/predict')
def index():
    return 'Predicted: true'

if __name__ == '__main__':
    app.run(threaded=True)