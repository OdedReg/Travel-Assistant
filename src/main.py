from typing import Tuple, List

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
        - Local attractions and points of interest
        - Travel recommendations
        - Packing list
        - Weather information for destinations
        - Currency exchange rates
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
    def clear_chat() -> Tuple[str, List[List[str]]]:
        """
        Clears the chat by returning an empty message and an empty chat history.

        Returns:
            A tuple with an empty string for the message and an empty list for the chat history.
        """
        return "", []


    def submit_message(message: str, chatbot: List[List[str]]) -> Tuple[str, List[List[str]]]:
        """
        Handles the submission of a message, adding it to the chat history.

        Args:
            message (str): The message sent by the user.
            chatbot (List[List[str]]): The current chat history.

        Returns:
            A tuple with an empty string for the input message and the updated chat history.
        """
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
            "What are the top attractions in Tokyo?",
            "Create a packing list for a business trip to Paris in October",
            "Tell me about local currency in Thailand",
            "Recommended destinations for a beach vacation in October",
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
        share=False,
        debug=True
    )
