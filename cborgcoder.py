#!/usr/bin/env python
import openai
import os
import sys
import argparse

from utils import get_doc_content, read_file
from cborginteract import CBorgInteract

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="user prompt")
    parser.add_argument("--file", help="file to be attached", required=False)
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    file_content = ""
    if (args.file):
        file_content = read_file(args.file)

        if file_content == None:
            sys.exit()

    cborg = CBorgInteract(model="lbl/cborg-coder:latest")
    messages = [              
            {
                "role": "user",
                "content": args.prompt+"\n"+file_content
            }
        ]

    cborg.get_response(messages=messages, temperature=0.0, stream=True)
    cborg.print_response()
    
if __name__ == "__main__":
    main()
