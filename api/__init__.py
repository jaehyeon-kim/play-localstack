from datetime import datetime
from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS

from .namespace import api
from . import db

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.config.from_mapping(
    DB_CONNECT="postgresql://testuser:testpass@localhost:6000/testdb"
)
app.json_encoder=CustomJSONEncoder
app.url_map.strict_slashes=False
cors = CORS(app, resources={"*": {"origins": "*"}})
app.config.setdefault('RESTPLUS_MASK_HEADER', 'X-Fields')
app.config.setdefault('RESTPLUS_MASK_SWAGGER', False)



api.init_app(app)
db.init_app(app)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
