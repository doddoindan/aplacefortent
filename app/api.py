

### __________API____________
import json
from flask.views import MethodView
from flask import jsonify, Response, request, url_for, make_response
from flask.ext.login import login_required
from app.mod_marker.models import Marker
from app.mod_marker.forms import EditMarkerForm
from app.mod_marker.controllers import formToMarker
from app.mod_auth.models import User
from app import db
from app import app

## ERRORS
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['Error'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

###
### MARKER CLASS
class MakerApi(MethodView):
    decorators = [login_required]

    def get(self, id):
        response = jsonify(status_code=200)
        if id is None:
            response.data = json.dumps([u.as_dict for u in Marker.query.all()])
            return response
        else:
            marker = Marker.query.filter_by(id=id).first()
            if not marker:
                raise InvalidUsage("Wrong id", status_code=410)
            response.data = json.dumps(marker.as_dict)
            return response

    def post(self):
        # create a new Marker
        response = jsonify(status_code=201)
        form = EditMarkerForm.from_json(request.get_json(), csrf_enabled=False)
        if form.validate():
            newMarker = formToMarker(form)
            db.session.add(newMarker)
            db.session.commit()
            response.headers['location'] = url_for("MarkersAPI_PUT", id=newMarker.id)
        else:
            response.status_code = 301
        return response

    def delete(self, id):
        marker = Marker.query.filter_by(id=id).first()
        if marker:
            db.session.delete(marker)
            db.session.commit()
        return jsonify(status_code=200)

    def put(self, id):
        # create a new Marker
        response = jsonify(status_code = 200)
        form = EditMarkerForm.from_json(request.get_json(), csrf_enabled=False)
        if form.validate():
            newMarker = formToMarker(form)
            db.session.add(newMarker)
            db.session.commit()
        else:
            response.data = "Validation error"
            response.status_code = 301
        return response


### UNIVER CLASS
class UniversalApi(MethodView):
    decorators = [login_required]
    _model = None
    _form = None

    @staticmethod
    def _formToModel():
        pass

    def get(self, id):
        response = jsonify(status_code=200)
        if id is None:
            response.data = json.dumps([u.as_dict for u in self._model.query.all()])
            return response
        else:
            result = self._model.query.filter_by(id=id).first()
            if not result:
                raise InvalidUsage("Wrong id", status_code=410)
            response.data = json.dumps(result.as_dict)
            return response

    def post(self):
        # create a new Marker
        response = jsonify(status_code=201)
        form = self._form.from_json(request.get_json(), csrf_enabled=False)
        if form.validate():
            item = self._formToModel(form)
            db.session.add(item)
            db.session.commit()
            response.headers['location'] = url_for("MarkersAPI_PUT", id=item.id)
        else:
            response.status_code = 301
        return response

    def delete(self, id):
        item = self._model.query.filter_by(id=id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
        return jsonify(status_code=200)

    def put(self, id):
        # create a new Marker
        response = jsonify(status_code=200)
        form = self._form.from_json(request.get_json(), csrf_enabled=False)
        if form.validate():
            item = self._formToModel(form)
            db.session.add(item)
            db.session.commit()
        else:
            response.data = "Validation error"
            response.status_code = 301
        return response

class UMarkerApi(UniversalApi):
    _form = EditMarkerForm
    _model = Marker
    def _formToModel(self, form):
        return formToMarker(form)


class UUserApi(UniversalApi):
    _form = None
    _model = User
    def _formToModel(self, form):
        return None