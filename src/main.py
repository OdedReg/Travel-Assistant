import gradio as gr

from src.travel_assistant import chat_with_agent

with gr.Blocks(
        title="Travel Agent Chat",
        theme=gr.themes.Soft(
            primary_hue="green",
            secondary_hue="blue",
        )
) as demo:
    gr.Markdown("<h1 style='text-align: center;'>🌍 Travel Agent Chat</h1>")
    gr.Markdown(
        """
        Ask me anything about travel! I can help you with:
        - Weather information for destinations
        - Currency exchange rates
        - Local attractions and points of interest
        - Travel recommendations
        - And much more!
        """
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask me about travel...",
            container=False,
            scale=7,
            show_label=False
        )
        submit_btn = gr.Button("Send", scale=1, variant="primary")
        clear_btn = gr.Button("Clear", scale=1, variant="secondary")

    chatbot = gr.Chatbot(
        height=500,
        show_label=False,
        container=True,
        show_copy_button=False,
        avatar_images=("https://cdn-icons-png.flaticon.com/512/1077/1077012.png",
                       "https://cdn-icons-png.flaticon.com/512/684/684908.png"),
    )

    # Event handlers
    def clear_chat():
        return "", []

    def submit_message(message, chatbot):
        return "", chatbot + [[message, None]]

    # Connect the events
    msg.submit(
        submit_message,
        [msg, chatbot],
        [msg, chatbot],
        queue=False
    ).then(
        chat_with_agent,
        [chatbot],
        [chatbot]
    )

    submit_btn.click(
        submit_message,
        [msg, chatbot],
        [msg, chatbot],
        queue=False
    ).then(
        chat_with_agent,
        [chatbot],
        [chatbot]
    )

    clear_btn.click(clear_chat, outputs=[msg, chatbot])

    # Add some example queries
    gr.Examples(
        examples=[
            "Help me build a packing suggestions for a business trip to Paris in October",
            "What are the most famous water parks near Tel Aviv?",
            "What are the top attractions in Tokyo?",
            "Tell me about local currency in Thailand"
        ],
        inputs=msg,
        label="Try these examples:"
    )

# Launch the app
if __name__ == "__main__":
    demo.queue(max_size=20)  # Enable queuing for streaming
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,  # Default Gradio port
        share=False,  # Set to True if you want a public link
        debug=True  # Enable debug mode
    )