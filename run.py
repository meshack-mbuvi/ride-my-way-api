from application import create_app


if __name__ == '__main__':
    app = create_app('production')
    app.run(host='0.0.0.0')
