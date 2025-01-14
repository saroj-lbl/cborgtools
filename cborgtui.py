#!/usr/bin/env python
"""
Adopts and extends the textual interface described below
https://textual.textualize.io/blog/2024/09/15/anatomy-of-a-textual-user-interface/
for CBorgApp
"""

from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Input, Header, Footer, Markdown
from textual.containers import VerticalScroll

from cborginteract import CBorgInteract

cborgcoder = CBorgInteract(model="lbl/cborg-coder:latest")

class Prompt(Markdown):
    BORDER_TITLE = "You"

class Response(Markdown):
    BORDER_TITLE = "CBorg"

class CBorgApp(App):
    AUTO_FOCUS = "Input"
    CSS = """
    Prompt {
        background: $primary 10%;
        color: $text;
        margin: 1;
        margin-left: 2;
        padding: 1 1;
    }
    Response {
        border: wide $success;
        background: $success 10%;
        color: $text;
        margin: 1;
        margin-left: 4;
        padding: 1 1;
    }
    """
    conversation = []

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="chat-view"):
            yield Response("CBorg Chat")
        yield Input(placeholder="How can I help you?")
        yield Footer()

    @on(Input.Submitted)
    def on_input(self, event: Input.Submitted) -> None:
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        chat_view.mount(Prompt(event.value))
        chat_view.mount(response := Response())
        response.anchor()
        if event.value == "quit" or event.value == "exit":
            self.exit()
        self.send_prompt(event.value, response)

    @work(thread=True)
    def send_prompt(self, prompt: str, response: Response) -> None:
        response_content = ""
        history = "Coversation history: " + "\n".join(self.conversation)
        cborgcoder.get_response(messages=[{"role": "user", "content": prompt + history}])
        for chunk in cborgcoder.response:
            if chunk.choices[0].delta.content is not None:
                response_chunk = chunk.choices[0].delta.content
                response_content += response_chunk

            self.call_from_thread(response.update, response_content)

        self.conversation.append("User prompt: " + prompt + "\n" + "CBorg Response: " + response_content)
        
if __name__ == "__main__":
    app = CBorgApp()
    app.run()