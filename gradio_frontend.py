import gradio as gr
import requests

API_URL = "http://localhost:5000"


def classify_text(text):
    response = requests.post(f"{API_URL}/classify", json={"text": text})
    if response.ok:
        data = response.json()
        return data[0]["label"]
    return "Error"


def answer_question(context, question):
    response = requests.post(f"{API_URL}/answer", json={"context": context, "question": question})
    if response.ok:
        data = response.json()
        return data.get("answer", "")
    return "Error"


with gr.Blocks() as demo:
    gr.Markdown("# NLP Demo")
    with gr.Tab("Classification"):
        inp = gr.Textbox(label="Text")
        out = gr.Textbox(label="Label")
        btn = gr.Button("Classify")
        btn.click(classify_text, inputs=inp, outputs=out)
    with gr.Tab("Question Answering"):
        ctx = gr.Textbox(label="Context")
        ques = gr.Textbox(label="Question")
        out_ans = gr.Textbox(label="Answer")
        btn2 = gr.Button("Answer")
        btn2.click(answer_question, inputs=[ctx, ques], outputs=out_ans)


demo.launch(server_name="0.0.0.0")
