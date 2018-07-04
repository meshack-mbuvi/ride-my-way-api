import os
from werkzeug.contrib.fixers import ProxyFix  # fix no spec in heroku
from application import create_app


if __name__ == '__main__':
    app = create_app('development')
    app.wsgi_app = ProxyFix(app.wsgi_app)
    port = int(os.environ.get("PORT", 5432))
    app.run(debug=True)

#  port=port,host='0.0.0.0', 