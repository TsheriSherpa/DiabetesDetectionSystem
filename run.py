from app import app, db
import os

port = int(os.environ.get('PORT', 6000))
print(port)
if __name__ == '__main__':
    app.run(debug = True, port=port, host = '0.0.0.0')