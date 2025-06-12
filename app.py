from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Initialize models
classifier = pipeline("sentiment-analysis")
qa_model = pipeline("question-answering")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json(force=True)
    text = data.get("text", "")
    results = classifier(text)
    return jsonify(results)

@app.route("/answer", methods=["POST"])
def answer():
    data = request.get_json(force=True)
    question = data.get("question", "")
    context = data.get("context", "")
    result = qa_model(question=question, context=context)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
