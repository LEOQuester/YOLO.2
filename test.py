from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return 'Hello, GET request received!'
    elif request.method == 'POST':
        data = request.get_data(as_text=True)
        return f'Hello, POST request received with data: {data}'

if __name__ == '__main__':
    app.run(debug=True)
