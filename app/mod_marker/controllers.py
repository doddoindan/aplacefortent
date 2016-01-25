from flask import Blueprint, request, render_template, g, jsonify, json, Response, url_for
from flask.ext.login import login_required
from app import db
import time
from app.mod_marker.models import Marker
from app.mod_marker.forms import EditMarkerForm

from datetime import datetime


mod_marker = Blueprint('marker', __name__, url_prefix='/marker')


# GET_MARKERS
@mod_marker.route('/load', methods=['GET', 'POST'])
@login_required
def load():
    respJson = json.dumps([u.as_dict for u in Marker.query.all()])
    return Response(respJson, mimetype='application/json')

##GET FORM MARKER
@mod_marker.route('/editform')
@mod_marker.route('/editform/<int:id>')
def editform(id=None):

    formReadonly = False
    if id != None:
        marker = Marker.query.filter_by(id=id).first()
        formReadonly = marker.user_id != g.user.id
        form = EditMarkerForm(obj=marker)
    else:
        form = EditMarkerForm()

    return render_template("editmarker_.html",
                             editMarkerForm=form,
                             formReadonly = formReadonly
                             )



@mod_marker.route('/delete', methods=['POST'])
def delete():
    id = int(request.form['id'])
    marker = Marker.query.filter_by(id=id).first()
    print marker.user_id
    if marker.user_id != g.user.id:
        return jsonify({'status': 'ERR'})
    db.session.delete(marker)
    db.session.commit()
    return jsonify({'status': 'OK'})

##save form to marker
def formToMarker(form):

    newMarker = Marker.query.filter_by(id=(form.id.data if form.id.data else -1)).first()
    if newMarker is None:
      newMarker = Marker()
    newMarker.latt = form.latt.data
    newMarker.long = form.long.data
    newMarker.description=form.description.data
    newMarker.water=form.water.data
    newMarker.potable=form.potable.data
    newMarker.campfire=form.campfire.data
    newMarker.shop=form.shop.data
    newMarker.maxtentcount=form.maxtentcount.data
    newMarker.owner=g.user
    return newMarker

## SAVE MARKER
@mod_marker.route('/save', methods=['POST'])
@login_required
def save():

    form = EditMarkerForm(request.form)
    print form.data

    if form.validate():
        print "VAAAAAAAAALID"
    else:
        print "NOOOOOOO________"
        print form.errors
        return jsonify({'status': 'ERR'})

    newMarker = Marker.query.filter_by(id=(form.id.data if form.id.data else -1)).first()

    if newMarker is None:
        newMarker = Marker()

    newMarker.latt = form.latt.data
    newMarker.long = form.long.data
    newMarker.description=form.description.data
    newMarker.water=form.water.data
    newMarker.potable=form.potable.data
    newMarker.campfire=form.campfire.data
    newMarker.shop=form.shop.data
    newMarker.maxtentcount=form.maxtentcount.data
    newMarker.owner=g.user

    db.session.add(newMarker)
    db.session.commit()
    print newMarker.id
    return jsonify({'status': 'OK', 'id': newMarker.id});



