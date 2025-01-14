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

    documentation = get_doc_content(location="scienceit-docs/docs/")

    cborg = CBorgInteract(model="lbl/cborg-vision:latest", local=True)
    messages = [              
            {
                "role": "system",
                "content": """
                You are lrchelp, a helpful assistant for Lawrencium High Performance Computing resources users at the Lawrence Berkeley National Laboratory (LBNL). The Lawrencium system has the following environment variables set that give user-specific paths: $HOME can be used for getting a user home directory, $SCRATCH can be used to obtain a user's scratch directory. `module` command can be used to get the available software modules to load and unload. `sbatch` command is used for submitting batch jobs to the slurm scheduler. There are several partitions and usually the quality of service `--qos` option is required in the job submission script (not for `etna` and `etna_gpu` partitions). You are being run from the command line. So, there is no chat window. The syntax to call lrchelp is lrchelp followed by a user propmt in quotes with the --file followed by filename being optional to include the contents from the file. Note that the documentation may contain relative hyperlinks to files with extension .md such as ../accounts/mfa.md; please do not direct users to go to these links in your answers. Also do not include {:target="_blank"} {{ ext }} html tag in your response.
                """
            },
            {
                "role": "user",
                "content": args.prompt+"\n"+file_content+"\n"+" using the following relevant information: " + documentation
            }
        ]

    cborg.get_response(messages=messages, temperature=0.0, stream=True)
    cborg.print_response()
    
if __name__ == "__main__":
    main()
