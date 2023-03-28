import nox


@nox.session(venv_backend="none")
def format(s: nox.Session) -> None:
    s.run("isort", ".")
    s.run("black", ".")


@nox.session(venv_backend="none")
def format_check(s: nox.Session) -> None:
    s.run("isort", "--check", ".")
    s.run("black", "--check", ".")


@nox.session(venv_backend="none")
def lint(s: nox.Session) -> None:
    s.run("pflake8", "--color", "always")


@nox.session(venv_backend="none")
def type_check(s: nox.Session) -> None:
    s.run("mypy", "src", "noxfile.py")
