# `cborgtools`
cli and tui tools for cborg

## `cborghelp`
Requires `scienceit-docs` folder to be present as it sends the markdown files from the documentation as context.
Examples:
```
python cborghelp.py "How much does it cost to run 24 hours on 3 lr6 nodes?"
python cborghelp.py "What is wrong with my slurm script? Error message says module not found." --file script.sh
```

## `cborgtui`
Very basic chat app based on: https://textual.textualize.io/blog/2024/09/15/anatomy-of-a-textual-user-interface/

We should be able to get some ideas from `oterm` and add features to `cborgtui` or make `oterm` work with cborg.
