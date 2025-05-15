import gradio as gr
from chatbot import main

with open("custom_styles.css", "r", encoding="utf-8") as f:
    custom_css = f.read()

def respond(message, chat_history):
    chat_history = chat_history or []
    res = main(message)
    chat_history.append((message, res))
    return chat_history

def run():
    with gr.Blocks(css=custom_css) as app:
        with gr.Group():
            with gr.Column(elem_classes="container"):
                with gr.Row(elem_classes="top"):
                    gr.Button(elem_classes='profile', icon='./img/gpt_icon.png',value='챗봇')
                    gr.HTML('<span class="top-settings">🔍 📞 🎥 ≡</span>')

    
                chatbot = gr.Chatbot(elem_classes='middle', show_label=False)

      
                with gr.Column(elem_classes="bottom"):
                    msg = gr.Textbox(placeholder='메시지 입력', show_label=False, container=False)
                    with gr.Row():
                        gr.Image(
                            value='./img/toolbar.png',
                            show_label=False,
                            show_download_button=False,
                            show_fullscreen_button=False,
                            container=False,
                            height=50, width=50,
                            scale=10
                        )
                        send_btn = gr.Button(value='전송', elem_classes="button", scale=1, min_width=1)
                        send_btn.click(fn=respond, inputs=[msg, chatbot], outputs=chatbot)

    return app

if __name__ == '__main__':
    app = run()
    app.launch()