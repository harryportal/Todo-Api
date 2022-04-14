from api_package import create_app
from api_package.config import ProductionConfig


app = create_app(ProductionConfig)
if __name__ == "__main__":
    app.run(debug=True)