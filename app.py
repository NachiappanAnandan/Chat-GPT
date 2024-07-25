from flask import Flask, render_template, request

from openai import OpenAI
import os
from dotenv import load_dotenv
from firebase import firebase
from datetime import datetime
import docx2txt

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://api.aimlapi.com",
)

# First param pass the firebase database link
firebase = firebase.FirebaseApplication('https://contentversioning-c8b60-default-rtdb.firebaseio.com/', None)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["message"]
    if user_input == "":
        file = request.files['prompt-file']
        user_input = docx2txt.process(file)
    convert_to = request.form['options']
    prompt = f"USER: {user_input}\nChatbot: "
    userResponseData = {"timestamp": datetime.utcnow(), "chat": user_input, "convert_to": convert_to}
    firebase.post("/chatHistory", userResponseData)

    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {
                "role": "user",
                "content": prompt + "change this content to" + convert_to
            },
        ],
    )

    bot_response = response.choices[0].message.content
    aiResponseData = {"timestamp": datetime.utcnow(), "chat": bot_response}
    firebase.post("/chatHistory", aiResponseData)
    result = firebase.get('/chatHistory', None)
    return render_template(
        "chatbot.html", chat=result
    )

if __name__ == "__main__":
    app.run(debug=True)