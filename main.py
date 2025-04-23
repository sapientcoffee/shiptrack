from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

@app.route('/discovery', methods=['GET'])
def discovery():
    return jsonify({
        "name": "shipping",
        "version": "1.0",
        "owners": ["ameerabb", "lonestar"],
        "team": "genAIs",
        "organization": "acme"
    })

# 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

