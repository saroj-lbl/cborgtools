# `cborgtools`
cli and tui tools for cborg

## `cborghelp`
Requires `scienceit-docs` folder to be present as it sends the markdown files from the documentation as context.

Use `git clone --recurse-submodules git@github.com:saroj-lbl/cborgtools.git` to clone the documentation included as a submodule.

Examples:

```
python cborghelp.py "How much does it cost to run 24 hours on 3 lr6 nodes?"
```

## `cborgtui`
Very basic chat app based on: https://textual.textualize.io/blog/2024/09/15/anatomy-of-a-textual-user-interface/

We should be able to get some ideas from `oterm` and add features to `cborgtui` or make `oterm` work with cborg.
