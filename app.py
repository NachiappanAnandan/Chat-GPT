
from flask import Flask, render_template, request

from openai import OpenAI
import os
from dotenv import load_dotenv
from firebase import firebase
from datetime import datetime
from docx2txt import docx2txt


load_dotenv()

"https://alchemists8203364901.openai.azure.com/openai/deployments/gpt-4o/models/gpt-4o/2024-02-15-preview"

import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    api_version=os.environ["API_VERSION"],
    azure_endpoint=os.environ["AZURE_ENDPOINT"]
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
    # firebase.post("/chatHistory", userResponseData)
    response = client.chat.completions.create(
        model="gpt-4o",
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