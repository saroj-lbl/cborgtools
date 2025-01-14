import os
import openai

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

class CBorgInteract:
    def __init__(self, model="lbl/cborg-coder:latest", local=False):
        self.model = model
        self.api_key: str = os.environ.get('CBORG_API_KEY')
        if local:
            self.api_url: str = "https://api-local.cborg.lbl.gov"
        else:
            self.api_url: str = "https://api.cborg.lbl.gov"
        self.console: Console = Console()
        self._create_api_client()

    def _create_api_client(self):
        if not self.api_key:
            self.console.print("Error: API key not set. Please set the environment variable CBORG_API_KEY \n An API key can be requested at https://cborg.lbl.gov/api_request/")
            return None
        
        self.client = openai.OpenAI(
            api_key=self.api_key, base_url=self.api_url
        )

    def get_response(self, messages=[{"role": "user", "content": "Hello"}],
                     temperature=0.0,
                     stream=True):
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=stream
        )
        self.stream = stream
        return self.response

    def print_response(self):
        answer = ""
        panel = Panel("")

        with Live(panel, refresh_per_second=4) as live:
            if self.stream:
                for chunk in self.response:
                    if chunk.choices[0].delta.content is not None:
                        answer_chunk = chunk.choices[0].delta.content
                        answer = answer + answer_chunk    
                    panel.renderable=Markdown(answer)
            else:
                answer = self.response.choices[-1].message.content
                panel.renderable=Markdown(answer)
                print (self.response.usage)

