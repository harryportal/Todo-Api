from api_package import create_app
from api_package.config import Config


app = create_app(Config)
if __name__ == "__main__":
    app.run(debug=True)