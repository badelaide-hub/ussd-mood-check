import os
from flask import Flask, request, jsonify

app = Flask(__name__)
sessions = {}

@app.route("/", methods=["GET"])
def home():
    return "USSD service is running", 200

@app.route("/ussd", methods=["POST"])
def ussd():
    data = request.get_json(silent=True) or {}

    user_id = data.get("USERID", "Adelle22")
    msisdn = data.get("MSISDN", "")
    user_data = str(data.get("USERDATA", "")).strip()
    msg_type = data.get("MSGTYPE", True)
    session_id = data.get("SESSIONID", msisdn)

    if msg_type is True:
        sessions[session_id] = 1
        msg = "Welcome to AAAB mood checker! How are you feeling today?\n1. Feeling fine\n2. Feeling sad\n3. Feeling frisky"
        continue_session = True
    else:
        step = sessions.get(session_id, 1)

        if step == 1:
            if user_data == "1":
                sessions[session_id] = 2
                msg = "Glad you're good! Any issues on your mind?\n1. Relationship issues\n2. Money problems\n3. Family Issues"
                continue_session = True
            elif user_data == "2":
                sessions[session_id] = 2
                msg = "Sorry you're down. What's going on?\n1. Relationship issues\n2. Money problems\n3. Family Issues"
                continue_session = True
            elif user_data == "3":
                sessions[session_id] = 2
                msg = "Someone is in a mood! What's up?\n1. Relationship issues\n2. Money problems\n3. Family Issues"
                continue_session = True
            else:
                sessions.pop(session_id, None)
                msg = "Invalid option. Please dial again."
                continue_session = False

        elif step == 2:
            sessions.pop(session_id, None)
            if user_data == "1":
                msg = "Noted: Relationship issues. Communication is key."
            elif user_data == "2":
                msg = "Noted: Money problems. Keep pushing, things will work out."
            elif user_data == "3":
                msg = "Noted: Family Issues. Stay patient and put across your intentions."
            else:
                msg = "Invalid selection."
            continue_session = False

        else:
            sessions.pop(session_id, None)
            msg = "Session expired. Please dial again."
            continue_session = False

    return jsonify({
        "USERID": user_id,
        "MSISDN": msisdn,
        "USERDATA": user_data,
        "MSG": msg,
        "MSGTYPE": continue_session
    }), 200

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)