import os
from app import create_app


config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

print(config_name)
print(os.getenv('DATABASE_URL'))

if __name__ == '__main__':
    app.run()