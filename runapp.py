import os
from app import create_app

config_name = os.environ.get('APP_SETTINGS')
app = create_app(config_name)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('', port=port)
