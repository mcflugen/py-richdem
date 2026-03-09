import os
import sys

import nox

ROOT = os.path.dirname(os.path.abspath(__file__))


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(name="build-richdem", python=None)
def build_richdem(session: nox.Session) -> None:
    inst_dir = _build_richdem(session, session.posargs[0] if session.posargs else None)
    session.log(inst_dir)


def _build_richdem(session: nox.Session, inst_dir=None) -> str:
    inst_dir = os.path.abspath(session.create_tmp() if inst_dir is None else inst_dir)
    build_dir = os.path.join(session.create_tmp(), "richdem")

    src_dir = os.path.join(ROOT, "vendor", "cmake")

    session.run(
        "cmake",
        *("-S", src_dir),
        *("-B", build_dir),
        f"-DCMAKE_INSTALL_PREFIX={inst_dir}",
        "-DCMAKE_INSTALL_LIBDIR=lib",
        "-DBUILD_SHARED_LIBS=OFF",
        "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_INSTALL_LIBDIR=lib",
        external=True,
    )
    session.run("cmake", "--build", build_dir, "--config", "Release", external=True)
    session.run("cmake", "--install", build_dir, "--config", "Release", external=True)

    return inst_dir


@nox.session(python=None)
def install(session: nox.Session) -> None:
    _install_editable(
        session,
        richdem_prefix=os.environ.get("RICHDEM_PREFIX"),
        openmp_prefix=os.environ.get("OPENMP_PREFIX"),
    )


def _install_editable(
    session: nox.Session, richdem_prefix=None, openmp_prefix=None
) -> None:
    if richdem_prefix is None:
        richdem_prefix = _build_richdem(session)

    env = {"RICHDEM_PREFIX": richdem_prefix}
    if openmp_prefix:
        env["OPENMP_PREFIX"] = openmp_prefix

    if sys.platform == "darwin" and not openmp_prefix:
        session.warn("OPENMP_PREFIX is not set")

    for k, v in env.items():
        session.log(f"{k} = {v}")

    session.run("python", "-m", "pip", "install", "-e", ".", env=env)

    return richdem_prefix
