from flask import Flask, request, render_template, jsonify
import os
import json
from difflib import SequenceMatcher

app = Flask(__name__)

BLOCKCHAIN_DIR = os.path.join(os.path.dirname(__file__), "blocks") + "/"

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def read_answer_based_on_question(user_query):
    block_files = os.listdir(BLOCKCHAIN_DIR)
    block_files.sort(key=lambda x: int(x.split('.')[0]))

    found = False
    for file_name in block_files:
        try:
            with open(os.path.join(BLOCKCHAIN_DIR, file_name), 'r') as file:
                block_data = json.load(file)
                question_and_answer = block_data.get('text').split(', ')
                if len(question_and_answer) == 2:
                    question, answer = question_and_answer
                    similarity = similar(user_query, question)
                    if similarity > 0.7:  # Adjust the similarity threshold as needed
                        return answer  # Return the answer if a match is found
        except Exception as e:
            print(f"Error reading block {file_name}: {e}")

    return "No matching answer found for the given question."

@app.route('/ride')
def chat():
    return render_template('ride.html')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        if len(text) < 1:
            return redirect(url_for("index"))

        make_proof = request.form.get("make_proof", False)
        blockchain.write_block(text, make_proof)
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def integrity():
    results = blockchain.check_blocks_integrity()
    if request.method == "POST":
        return render_template("index.html", results=results)
    return render_template("index.html")


@app.route("/mining", methods=["POST"])
def mining():
    if request.method == "POST":
        max_index = int(blockchain.get_next_block())

        for i in range(2, max_index):
            blockchain.get_POW(i)
        return render_template("index.html", querry=max_index)
    return render_template("index.html")



@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/get_response')
def get_response():
    user_message = request.args.get('message')
    bot_response = read_answer_based_on_question(user_message)
    return jsonify({"botMessage": bot_response if bot_response else "An error occurred or no answer found."})

if __name__ == '__main__':
    app.run(debug=True)