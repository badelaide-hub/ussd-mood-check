import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store session step per session ID
sessions = {}

@app.route("/ussd", methods=["POST"])
def ussd():
    data = request.get_json(silent=True) or {}

    user_id = data.get("USERID", "Adelle22")
    msisdn = data.get("MSISDN", "")
    user_data = str(data.get("USERDATA", "")).strip()
    msg_type = data.get("MSGTYPE", True)
    session_id = data.get("SESSIONID", msisdn)

    # First dial (MSGTYPE is True or 1)
    if msg_type is True or str(msg_type) == "1":
        sessions[session_id] = 1
        msg = "Hello! How are you feeling today?\n"
        msg += "1. Feeling fine\n"
        msg += "2. Feeling sad\n"
        msg += "3. Feeling frisky"
        continue_session = True

    else:
        step = sessions.get(session_id, 1)

        # Screen 2 based on Screen 1 input
        if step == 1:
            if user_data == "1":
                sessions[session_id] = 2
                msg = "Glad you're good! Any issues on your mind?\n"
                msg += "1. Relationship issues\n"
                msg += "2. Money problems\n"
                msg += "3. Family Issues"
                continue_session = True
            elif user_data == "2":
                sessions[session_id] = 2
                msg = "Sorry you're down. What's going on?\n"
                msg += "1. Relationship issues\n"
                msg += "2. Money problems\n"
                msg += "3. Family Issues"
                continue_session = True
            elif user_data == "3":
                sessions[session_id] = 2
                msg = "Someone is in a mood! What's up?\n"
                msg += "1. Relationship issues\n"
                msg += "2. Money problems\n"
                msg += "3. Family Issues"
                continue_session = True
            else:
                sessions.pop(session_id, None)
                msg = "Invalid option. Please dial again."
                continue_session = False

        # Final screen after Screen 2 selection
        elif step == 2:
            sessions.pop(session_id, None)
            if user_data == "1":
                msg = "Noted: Relationship issues. Take time to talk things through."
            elif user_data == "2":
                msg = "Noted: Money problems. Keep pushing, things will balance out."
            elif user_data == "3":
                msg = "Noted: Family Issues. Stay patient and communicate calmly."
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
        "MSG": msg,
        "MSGTYPE": continue_session
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)