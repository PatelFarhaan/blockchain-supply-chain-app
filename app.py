from project import app, port

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True, use_reloader=True)
