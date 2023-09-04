"""
This project uses Invoke (pyinvoke.org) for task management.
Install it via:

```
pip install invoke
```

And then run:

```
inv --list
```

If you do not wish to use invoke you can simply delete this file.
"""


import platform
import re
import shutil
from pathlib import Path
from typing import List, Optional

from invoke import Context, Result, task

# Extract supported python versions from the pyproject.toml classifiers key
SUPPORTED_PYTHON_VERSIONS = [
    line.split("::")[-1].strip().replace('"', "").replace(",", "")
    for line in Path("pyproject.toml").read_text().splitlines()
    if "Programming Language :: Python ::" in line
]

NOT_WINDOWS = platform.system() != "Windows"


def echo_header(msg: str):
    print(f"\n--- {msg} ---")


class MsgType:
    # Emojis have to be encoded as bytes to not break the terminal on Windows
    @property
    def DOING(self) -> str:
        return b"\xf0\x9f\xa4\x96".decode() if NOT_WINDOWS else "DOING:"

    @property
    def GOOD(self) -> str:
        return b"\xe2\x9c\x85".decode() if NOT_WINDOWS else "DONE:"

    @property
    def FAIL(self) -> str:
        return b"\xf0\x9f\x9a\xa8".decode() if NOT_WINDOWS else "FAILED:"

    @property
    def WARN(self) -> str:
        return b"\xf0\x9f\x9a\xa7".decode() if NOT_WINDOWS else "WARNING:"

    @property
    def SYNC(self) -> str:
        return b"\xf0\x9f\x9a\x82".decode() if NOT_WINDOWS else "SYNCING:"

    @property
    def PY(self) -> str:
        return b"\xf0\x9f\x90\x8d".decode() if NOT_WINDOWS else ""

    @property
    def CLEAN(self) -> str:
        return b"\xf0\x9f\xa7\xb9".decode() if NOT_WINDOWS else "CLEANING:"

    @property
    def TEST(self) -> str:
        return b"\xf0\x9f\xa7\xaa".decode() if NOT_WINDOWS else "TESTING:"

    @property
    def COMMUNICATE(self) -> str:
        return b"\xf0\x9f\x93\xa3".decode() if NOT_WINDOWS else "COMMUNICATING:"

    @property
    def EXAMINE(self) -> str:
        return b"\xf0\x9f\x94\x8d".decode() if NOT_WINDOWS else "VIEWING:"


msg_type = MsgType()


def git_init(c: Context, branch: str = "main"):
    """Initialize a git repository if it does not exist yet."""
    # If no .git directory exits
    if not Path(".git").exists():
        echo_header(f"{msg_type.DOING} Initializing Git repository")
        c.run(f"git init -b {branch}")
        c.run("git add .")
        c.run("git commit -m 'Init'")
        print(f"{msg_type.GOOD} Git repository initialized")
    else:
        print(f"{msg_type.GOOD} Git repository already initialized")


def setup_venv(
    c: Context,
    python_path: str,
    venv_name: Optional[str] = None,
) -> str:
    """Create a virtual environment if it does not exist yet.

    Args:
        c: The invoke context.
        python_path: The python executable to use.
        venv_name: The name of the virtual environment. Defaults to ".venv".
    """
    if venv_name is None:
        venv_name = ".venv"

    if not Path(venv_name).exists():
        echo_header(
            f"{msg_type.DOING} Creating virtual environment using {msg_type.PY}:{python_path}",
        )
        c.run(f"{python_path} -m venv {venv_name}")
        print(f"{msg_type.GOOD} Virtual environment created")
    else:
        print(f"{msg_type.GOOD} Virtual environment already exists")
    return venv_name


def _add_commit(c: Context, msg: Optional[str] = None):
    print(f"{msg_type.DOING} Adding and committing changes")
    c.run("git add .")

    if msg is None:
        msg = input("Commit message: ")

    c.run(f'git commit -m "{msg}"', pty=NOT_WINDOWS, hide=True)
    print(f"{msg_type.GOOD} Changes added and committed")


def is_uncommitted_changes(c: Context) -> bool:
    git_status_result: Result = c.run(
        "git status --porcelain",
        pty=NOT_WINDOWS,
        hide=True,
    )

    uncommitted_changes = git_status_result.stdout != ""
    return uncommitted_changes


def add_and_commit(c: Context, msg: Optional[str] = None):
    """Add and commit all changes."""
    if is_uncommitted_changes(c):
        uncommitted_changes_descr = c.run(
            "git status --porcelain",
            pty=NOT_WINDOWS,
            hide=True,
        ).stdout

        echo_header(
            f"{msg_type.WARN} Uncommitted changes detected",
        )

        for line in uncommitted_changes_descr.splitlines():
            print(f"    {line.strip()}")
        print("\n")
        _add_commit(c, msg=msg)


def branch_exists_on_remote(c: Context) -> bool:
    branch_name = Path(".git/HEAD").read_text().split("/")[-1].strip()

    branch_exists_result: Result = c.run(
        f"git ls-remote --heads origin {branch_name}",
        hide=True,
    )

    return branch_name in branch_exists_result.stdout


def update_branch(c: Context):
    echo_header(f"{msg_type.SYNC} Syncing branch with remote")

    if not branch_exists_on_remote(c):
        c.run("git push --set-upstream origin HEAD")
    else:
        print("Pulling")
        c.run("git pull")
        print("Pushing")
        c.run("git push")


def create_pr(c: Context):
    c.run(
        "gh pr create --web",
        pty=NOT_WINDOWS,
    )


def update_pr(c: Context):
    echo_header(f"{msg_type.COMMUNICATE} Syncing PR")
    # Get current branch name
    branch_name = Path(".git/HEAD").read_text().split("/")[-1].strip()
    pr_result: Result = c.run(
        "gh pr list --state OPEN",
        pty=False,
        hide=True,
    )

    if branch_name not in pr_result.stdout:
        create_pr(c)
    else:
        open_web = input("Open in browser? [y/n] ")
        if "y" in open_web.lower():
            c.run("gh pr view --web", pty=NOT_WINDOWS)


def exit_if_error_in_stdout(result: Result):
    # Find N remaining using regex

    if "error" in result.stdout:
        errors_remaining = re.findall(r"\d+(?=( remaining))", result.stdout)[
            0
        ]  # testing
        if errors_remaining != "0":
            exit(0)


def pre_commit(c: Context, auto_fix: bool):
    """Run pre-commit checks."""

    # Essential to have a clean working directory before pre-commit to avoid committing
    # heterogenous files under a "style: linting" commit
    if is_uncommitted_changes(c):
        print(
            f"{msg_type.WARN} Your git working directory is not clean. Stash or commit before running pre-commit.",
        )
        exit(1)

    echo_header(f"{msg_type.CLEAN} Running pre-commit checks")
    pre_commit_cmd = "pre-commit run --all-files"
    result = c.run(pre_commit_cmd, pty=NOT_WINDOWS, warn=True)

    exit_if_error_in_stdout(result)

    if ("fixed" in result.stdout or "reformatted" in result.stdout) and auto_fix:
        _add_commit(c, msg="style: Auto-fixes from pre-commit")

        print(f"{msg_type.DOING} Fixed errors, re-running pre-commit checks")
        second_result = c.run(pre_commit_cmd, pty=NOT_WINDOWS, warn=True)
        exit_if_error_in_stdout(second_result)
    else:
        if result.return_code != 0:
            print(f"{msg_type.FAIL} Pre-commit checks failed")
            exit(1)


@task
def static_type_checks(c: Context):
    echo_header(f"{msg_type.CLEAN} Running static type checks")
    c.run("tox -e type", pty=NOT_WINDOWS)


@task
def install(
    c: Context,
    pip_args: str = "",
    msg: bool = True,
    venv_path: Optional[str] = None,
):
    """Install the project in editable mode using pip install"""
    if msg:
        echo_header(f"{msg_type.DOING} Installing project")

    extras = ".[dev,tests,docs]" if NOT_WINDOWS else ".[dev,tests,docs]"
    install_cmd = f"pip install -e {extras} {pip_args}"

    if venv_path is not None and NOT_WINDOWS:
        with c.prefix(f"source {venv_path}/bin/activate"):
            c.run(install_cmd)
            return

    c.run(install_cmd)


def get_python_path(preferred_version: str) -> Optional[str]:
    """Get path to python executable."""
    preferred_version_path = shutil.which(f"python{preferred_version}")

    if preferred_version_path is not None:
        return preferred_version_path

    print(
        f"{msg_type.WARN}: python{preferred_version} not found, continuing with default python version",
    )
    return shutil.which("python")


@task
def setup(c: Context, python_path: Optional[str] = None):
    """Confirm that a git repo exists and setup a virtual environment.

    Args:
        c: Invoke context
        python_path: Path to the python executable to use for the virtual environment. Uses the return value of `which python` if not provided.
    """
    git_init(c)

    if python_path is None:
        # get path to python executable
        python_path = get_python_path(preferred_version="3.9")
        if not python_path:
            print(f"{msg_type.FAIL} Python executable not found")
            exit(1)
    venv_name = setup_venv(c, python_path=python_path)

    install(c, pip_args="--upgrade", msg=False, venv_path=venv_name)

    if venv_name is not None:
        print(
            f"{msg_type.DOING} Activate your virtual environment by running: \n\n\t\t source {venv_name}/bin/activate \n",
        )


@task
def update(c: Context):
    """Update dependencies."""
    echo_header(f"{msg_type.DOING} Updating project")
    install(c, pip_args="--upgrade", msg=False)


@task(iterable="pytest_args")
def test(
    c: Context,
    python_versions: List[str] = (SUPPORTED_PYTHON_VERSIONS[0],),  # noqa # type: ignore
    pytest_args: List[str] = [],  # noqa
):
    """Run tests"""
    # Invoke requires lists as type hints, but does not support lists as default arguments.
    # Hence this super weird type hint and default argument for the python_versions arg.
    echo_header(f"{msg_type.TEST} Running tests")

    python_version_strings = [f"py{v.replace('.', '')}" for v in python_versions]
    python_version_arg_string = ",".join(python_version_strings)

    if not pytest_args:
        pytest_args = [
            "tests",
            "-n auto",
            "-rfE",
            "--failed-first",
            "-p no:cov",
            "--disable-warnings",
            "-q",
        ]

    pytest_arg_str = " ".join(pytest_args)

    test_result: Result = c.run(
        f"tox -e {python_version_arg_string} -- {pytest_arg_str}",
        warn=True,
        pty=NOT_WINDOWS,
    )

    # If "failed" in the pytest results
    failed_tests = [line for line in test_result.stdout if line.startswith("FAILED")]

    if len(failed_tests) > 0:
        print("\n\n\n")
        echo_header("Failed tests")
        print("\n\n\n")
        echo_header("Failed tests")

        for line in failed_tests:
            # Remove from start of line until /test_
            line_sans_prefix = line[line.find("test_") :]

            # Keep only that after ::
            line_sans_suffix = line_sans_prefix[line_sans_prefix.find("::") + 2 :]
            print(f"FAILED {msg_type.FAIL} #{line_sans_suffix}     ")

    if test_result.return_code != 0:
        exit(test_result.return_code)


def test_for_rej():
    # Get all paths in current directory or subdirectories that end in .rej
    rej_files = list(Path(".").rglob("*.rej"))

    if len(rej_files) > 0:
        print(f"\n{msg_type.FAIL} Found .rej files leftover from cruft update.\n")
        for file in rej_files:
            print(f"    /{file}")
        print("\nResolve the conflicts and try again. \n")
        exit(1)


@task
def lint(c: Context, auto_fix: bool = False):
    """Lint the project."""
    test_for_rej()
    pre_commit(c=c, auto_fix=auto_fix)
    static_type_checks(c)


@task
def pr(c: Context, auto_fix: bool = False):
    """Run all checks and update the PR."""
    add_and_commit(c)
    lint(c, auto_fix=auto_fix)
    test(c, python_versions=SUPPORTED_PYTHON_VERSIONS)
    update_branch(c)
    update_pr(c)


@task
def docs(c: Context, view: bool = False, view_only: bool = False):
    """
    Build and view docs. If neither build or view are specified, both are run.
    """
    if not view_only:
        echo_header(f"{msg_type.DOING}: Building docs")
        c.run("tox -e docs")

    if view or view_only:
        echo_header(f"{msg_type.EXAMINE}: Opening docs in browser")
        # check the OS and open the docs in the browser
        if platform.system() == "Windows":
            c.run("start docs/_build/html/index.html")
        else:
            c.run("open docs/_build/html/index.html")
