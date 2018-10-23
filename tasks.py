import glob
import os

from invoke import task


@task
def format(ctx, noimports=False, nostyle=False):
    if not noimports:
        from isort import SortImports

    if not nostyle:
        from yapf.yapflib.yapf_api import FormatFile

    for filename in glob.glob('**/*.py', recursive=True):
        if not noimports:
            SortImports(filename)
        if not nostyle:
            FormatFile(filename, in_place=True)


@task
def install_hooks(ctx):
    ctx.run('pre-commit install')
