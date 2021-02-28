import glob
import os

from invoke import task


@task
def test(ctx, nocov=False):
    import pytest

    args = ["tests"]

    if not nocov:
        args.append("--cov=pushbullet_cli")

    pytest.main(args)


@task
def format(ctx):
    ctx.run("black .")


@task
def install_hooks(ctx):
    ctx.run("pre-commit install")
