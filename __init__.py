from flask import Flask
app = Flask(__name__)

from flask import Response
from flask import json, send_file, request, request_started


## REQUESTS

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

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



## ROUTES

@app.route("/")
def home():
    """ Home page """
    return "Welcome to my Flask Demo Server !"

@app.route("/image")
def image():
    """ Test for images """

    image = open('5323.jpg', 'rb')
    print image
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