from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

run(host="10.50.19.51", port=9001, debug=True)
