from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import request_to_GPT

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/write-history", methods=["GET"])
def write_history():
    args = request.args

    try:
        request_to_GPT.history_to_bd(args['mainCharacter'], args['mood'], args['settingStory'])
    except Exception as e:
        print(e)
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5623)
