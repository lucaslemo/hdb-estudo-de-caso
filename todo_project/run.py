import os
from todo_project import app

if __name__ == '__main__':
    host = os.getenv('APP_HOST')
    port = int(os.getenv('APP_PORT'))
    
    app.run(host=host, port=port)
