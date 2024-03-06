from flask import Flask, request, jsonify
from flask_cors import CORS

import decision_history

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/write-decision-history-1", methods=["GET"])
def write_decision_history1():
    args = request.args

    try:
        return str(decision_history.create_history_part1(args['mainCharacter'], args['mood'], args['settingStory']))
    except Exception as e:
        print(e)
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/write-decision-history-2", methods=["GET"])
def write_decision_history2():
    args = request.args
    print(args)
    try:
        decision_history.create_history_part2(args['id_history'], args['choice'])
        return jsonify({'message': 'Решение истории успешно записано'})
    except Exception as e:
        print(e)
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5623)
