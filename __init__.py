
from config import LocalConfig
from elixir import metadata, session
from flask import Flask, g

app = Flask(__name__)
app.config.from_object(LocalConfig)
# DB configuration
metadata.bind = app.config['SQLALCHEMY_DATABASE_URI']
metadata.echo = True

session.configure(autoflush=False)

from flask import Response
from flask import json, send_file, request, request_started

## REQUESTS

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    set_pagination_infos(request.values)

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        h['Access-Control-Max-Age'] = "10"  # "21600"

        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    h['Pragma'] = 'no-cache'
    h['Cache-Control'] = 'no-cache, no-store'

    return resp


## UTILS

def jsonify(data):
    """ We redefine the Flask jsonify function to be able to use list as primary structure
    """
    return app.response_class(json.dumps(data,
        indent=None if request.is_xhr else 2), mimetype='application/json')


def merge_params(sender, **extra):

    if request.json != None:
        from werkzeug.utils import CombinedMultiDict
        request.values = CombinedMultiDict([request.values, request.json])

request_started.connect(merge_params, app)


def query_with_pagination(query, req):
    from math import ceil

    # Get the total count of objects
    count = query.count()

    # Query with pagination
    #objects = query.limit(req['page_limit']).offset(req['page_offset']).all()
    objects = query.all()

    # Create a result dictionary
    results = dict()
    results['objects'] = objects
    results['page_offset'] = req['page_offset']
    results['page_limit'] = req['page_limit']
    results['count'] = count
    results['page_count'] = int(ceil(count / req['page_limit']))

    return results

def set_pagination_infos(values):
    """ Set pagination to the global g variable"""
    g.pagination = None

    if 'page_limit' in values and 'page_offset' in values:
        g.pagination = dict()
        g.pagination['page_limit'] = values['page_limit']
        g.pagination['page_offset'] = values['page_offset']

#Change names to :
#page
#num_results

from sqlalchemy import event
from sqlalchemy.sql.expression import Select

def before_execute(conn, clauseelement, multiparams, params):
    print "Received statement: %s" % clauseelement
    if isinstance(clauseelement, Select) and g.pagination is not None and 'isrunning' not in g.pagination:
        # Set critical area
        g.pagination['isrunning'] = True

        from math import ceil

        # Get count (another Select request!)
        g.pagination['count'] = conn.execute(clauseelement.count()).fetchone()[0]
        g.pagination['page_count'] = int(ceil(g.pagination['count'] / int(g.pagination['page_limit'])))

        # Get information
        clauseelement = clauseelement.limit(g.pagination['page_limit']).offset(g.pagination['page_offset'])

    # Clean critical area
    if g.pagination is not None and 'isrunning' in g.pagination:
        g.pagination.pop('isrunning')

    return (clauseelement, multiparams, params)

event.listen(metadata.bind, "before_execute", before_execute, retval=True)


## ROUTES

@app.route("/areas")
def areas_list():
    """ return list of areas """
    # Create your own query as you wish
    from models import Area
    q = Area.query.filter(Area.name.contains('Area'))

    # This part should be the request.values dictionary
    #req = dict()
    #req['page_limit'] = 10
    #req['page_offset']= 100

    # Query results with pagination
    #results = query_with_pagination(q, req)
    results = q.all()

    print g.pagination

    return str(results)

@app.route("/")
def home():
    """ Home page """
    return "Welcome to my Flask Demo Server !"

@app.route("/image")
def image():
    """ Test for images """

    image = open('5323.jpg', 'rb')
    stream = image.read()

    image.close()

    img = "data:image/jpeg;base64," + stream.encode('base64')

    #return img
    return Response(img, mimetype='text/plain')

@app.route("/modules")
def modules():
    """ Returns a list of modules """

    modules = list()

    moduleA = dict()
    moduleA['name'] = 'moduleA'
    moduleA['target'] = 'mouse-actions'
    moduleA['action'] = '/moduleA/action'
    moduleA['label'] = 'Module A Action'
    moduleA['controller'] = 'MouseTestCtrlA'
    moduleA['dependencies'] = ['js/modules/moduleA.js']
    modules.append(moduleA)

    moduleB = dict()
    moduleB['name'] = 'moduleB'
    moduleB['target'] = 'mouse-actions'
    moduleB['action'] = '/moduleB/action'
    moduleB['label'] = 'Module B Action'
    moduleB['controller'] = 'MouseTestCtrlB'
    moduleB['dependencies'] = ['js/modules/moduleB.js']
    modules.append(moduleB)

    moduleC = dict()
    moduleC['name'] = 'moduleC'
    moduleC['target'] = 'mouse-screen'
    moduleC['action'] = '/moduleC/action'
    moduleC['label'] = 'Module C Action'
    moduleC['dependencies'] = []
    modules.append(moduleC)

    moduleD = dict()
    moduleD['name'] = 'moduleD'
    moduleD['target'] = 'mouse-list'
    moduleD['action'] = '/moduleD/action'
    moduleD['label'] = 'Module D Action'
    moduleD['dependencies'] = []
    modules.append(moduleD)

    if "interested_in" in request.values:
        results = list()
        for module in modules:
            if module['target'] == request.values['interested_in']:
                results.append(module)
        modules = results

    return jsonify(modules)


if __name__ == "__main__":
    app.run(debug=True)