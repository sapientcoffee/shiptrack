from flask import Flask, jsonify, request, abort
import json, time


app = Flask(__name__)

@app.route('/discovery')
def discovery():
    return jsonify({
        "name": "shipping",
        "version": "1.0",
        "owners": ["ameerabb", "lonestar"],
        "team": "genAIs",
        "organization": "acme"
    })

# create liveness and readiness endpoints
@app.route('/live')
def live():
    return jsonify({
        'status': 'live',
        'code': 200,
        'timestamp': time.time()
    })


@app.route('/ready')
def ready():
    return jsonify({
        'status': 'ready',
        'code': 200,
        'timestamp': time.time()
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

