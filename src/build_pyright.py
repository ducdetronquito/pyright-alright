# pyright: basic
import logging
import subprocess
import sys
import zipfile
from argparse import ArgumentParser
from contextlib import chdir
from http.client import HTTPSConnection
from io import BytesIO
from urllib import request

logger = logging.getLogger("pyright-alright")


def clean_existing_pyright_artifacts():
    logger.info(
        "Clean existing pyright artifacts in the `pyright_alright/pyright` directory"
    )
    return_code = subprocess.call(
        [
            "rm",
            "-rf",
            "./pyright_alright/pyright/dist/",
            "&&",
            "rm",
            "-f",
            "./pyright_alright/pyright/index.js",
        ]
    )
    if return_code != 0:
        logger.error(f"Failed with code {return_code}")
        return sys.exit(return_code)


def get_pyright_archive(pyright_version: str) -> bytes:
    logger.info(f"Get pyright {pyright_version} archive")

    url = (
        f"https://github.com/microsoft/pyright/archive/refs/tags/{pyright_version}.zip"
    )

    with request.urlopen(url) as response:
        return response.read()


def store_pyright_archive_in_temp_directory(
    pyright_version: str, pyright_archive: bytes
):
    logger.info(
        f"Unzip and store pyright {pyright_version} archive in `temp` directory"
    )
    with zipfile.ZipFile(BytesIO(pyright_archive), "r") as zip_ref:
        zip_ref.extractall("./temp")


def install_pyright_dependencies(pyright_version: str):
    logger.info(f"Install pyright {pyright_version} dependencies")

    with chdir(f"./temp/pyright-{pyright_version}"):
        return_code = subprocess.call([sys.executable, "-m", "pybun", "install"])
        if return_code != 0:
            logger.error(f"Failed with code {return_code}")
            return sys.exit(return_code)


def build_pyright(pyright_version: str):
    logger.info(f"Build pyright {pyright_version}")

    with chdir(f"./temp/pyright-{pyright_version}/packages/pyright"):
        return_code = subprocess.call([sys.executable, "-m", "pybun", "run", "build"])
        if return_code != 0:
            logger.error(f"Failed with code {return_code}")
            return sys.exit(return_code)


def move_pyright_artifacts_to_pyright_alright(pyright_version: str):
    logger.info("Move built pyright into the pyright_alright directory")
    return_code = subprocess.call(
        [
            "cp",
            "-R",
            f"./temp/pyright-{pyright_version}/packages/pyright/dist/",
            "./pyright_alright/pyright",
        ]
    )
    if return_code != 0:
        logger.error(f"Failed with code {return_code}")
        return sys.exit(return_code)

    return_code = subprocess.call(
        [
            "cp",
            f"./temp/pyright-{pyright_version}/packages/pyright/index.js",
            "./pyright_alright/pyright",
        ]
    )
    if return_code != 0:
        logger.error(f"Failed with code {return_code}")
        return sys.exit(return_code)


def get_latest_pyright_version() -> str:
    host = "github.com"
    conn = HTTPSConnection(host)
    try:
        conn.request(
            "GET", "/microsoft/pyright/releases/latest", headers={"Host": host}
        )
        response = conn.getresponse()
        location_header = response.headers["location"]
    finally:
        conn.close()

    latest_version = location_header.replace(
        "https://github.com/microsoft/pyright/releases/tag/", ""
    )

    return latest_version


def get_cli_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=__file__, description="Repackage Pyright with bun as Python wheels"
    )
    parser.add_argument(
        "pyright_version",
        help="Pyright version to package",
    )

    return parser


def main():
    cli_args = get_cli_arg_parser().parse_args()

    pyright_version: str = cli_args.pyright_version
    if pyright_version == "latest":
        pyright_version = get_latest_pyright_version()

    logger.info(f"Request to build Pyright {pyright_version}")

    clean_existing_pyright_artifacts()

    pyright_archive = get_pyright_archive(pyright_version)

    store_pyright_archive_in_temp_directory(pyright_version, pyright_archive)

    install_pyright_dependencies(pyright_version)

    build_pyright(pyright_version)

    move_pyright_artifacts_to_pyright_alright(pyright_version)


if __name__ == "__main__":
    logging.basicConfig(handlers=[logging.StreamHandler()], level=logging.INFO)
    main()
