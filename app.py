from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://chatbottest2.local"])  # needs to change to actual site

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Key needs to be set as environmental variable in server

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # can also use "gpt-4" or other models
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": data["message"]}
            ]
        )
        
        return jsonify({
            "reply": response.choices[0].message.content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
