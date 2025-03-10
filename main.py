import gradio as gr
import requests
from vector_db import retrieve_near
import logging

logging.basicConfig(level=logging.INFO)


def generate_text(prompt, retrieve_context):
    if retrieve_context:
        logging.info("Lets retrieve context")
        context = retrieve_near(prompt)

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "deepseek-r1:8b",
            "prompt": (
                (f"This is the context: {context} \n\n\n" if retrieve_context else "")
                + f"This is the prompt: {prompt}\n\n"
                + "Generate a response to the prompt."
            ),
            "stream": False,
        },
    )

    return response.json()["response"].split("think>\n\n")[-1]


interface = gr.Interface(
    fn=generate_text,
    inputs=[gr.Textbox(label="Prompt"), gr.Checkbox(label="Retrieve Context")],
    outputs="text",
    title="vLLM Model Interface",
)

interface.launch(server_name="0.0.0.0", server_port=7860)
