import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from firebase import firebase
from datetime import datetime
from docx2txt import docx2txt

load_dotenv()




client = AzureOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version=os.environ["API_VERSION"],
    azure_endpoint=os.environ["AZURE_ENDPOINT"]
)

# Firebase configuration
firebase = firebase.FirebaseApplication('https://alchemists-ver-1-default-rtdb.firebaseio.com/', None)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")  # Add a secret key for session management


@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return redirect(url_for("login"))

@app.route("/history")
def history():
    if "user" in session:
        return render_template("history.html", user=session["user"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = firebase.get(f'/users/{username}', None)
        if user and user["password"] == password:  # Direct password comparison
            session["user"] = username
            return redirect(url_for("home"))
        return "Invalid username or password"
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = {
            "username": username,
            "password": password,  # Store plain password
            "chatHistory": {}
        }
        firebase.put('/users', username, user_data)
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    user_input = request.form["prompt"]
    if user_input == "":
        file = request.files['prompt-file']
        user_input = docx2txt.process(file)
    convert_to = request.form['options']
    prompt = f"USER: {user_input}\nChatbot: "
    userResponseData = {"timestamp": datetime.utcnow().isoformat(), "chat": user_input, "convert_to": convert_to}

    user = session["user"]
    user_chat_history = firebase.get(f'/users/{user}/chatHistory', None) or []


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt + "change this content to " + convert_to
            },
        ],
    )

    bot_response = response.choices[0].message.content
    aiResponseData = {"timestamp": datetime.utcnow().isoformat(), "chat": bot_response}
    singleChatHistory = {
        "prompt": userResponseData,
        "response":aiResponseData
    }
    user_chat_history.append(singleChatHistory)

    firebase.put(f'/users/{user}', 'chatHistory', user_chat_history)
    previousresult = firebase.get(f'/users/{user}/chatHistory', None)
    return render_template("chatbot.html", chat=singleChatHistory)


@app.route('/get_versions', methods=['GET'])
def get_versions():
    user = session["user"]
    keyword = request.args.get('keyword')
    response = firebase.get(f'/users/{user}/chatHistory',None)
    try:
        chat_history = response
        versions = []
        for item in chat_history:
            items=item['response']
            if keyword.lower() in items['chat'].lower():
                versions.append({
                    'version': f"v{len(versions) + 1}",
                    'timestamp': items['timestamp'],
                    'chat': items['chat']
                })
        return jsonify(versions)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error fetching data from Firebase Realtime Database"}), 500
    except requests.exceptions.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON response from Firebase Realtime Database"}), 400

@app.route("/allResponse")
def allResponse():
    user = session["user"]
    response = firebase.get(f'/users/{user}/chatHistory',None)
    chat_history = response
    return render_template("allResponse.html", chat=chat_history)
    
if __name__ == "__main__":
    app.run(debug=True)
