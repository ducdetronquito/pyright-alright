# pyright: basic
import logging
import subprocess
import sys
import zipfile
from contextlib import chdir
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
        return


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
            return


def build_pyright(pyright_version: str):
    logger.info(f"Build pyright {pyright_version}")

    with chdir(f"./temp/pyright-{pyright_version}/packages/pyright"):
        return_code = subprocess.call([sys.executable, "-m", "pybun", "run", "build"])
        if return_code != 0:
            logger.error(f"Failed with code {return_code}")
            return


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
        return

    return_code = subprocess.call(
        [
            "cp",
            f"./temp/pyright-{pyright_version}/packages/pyright/index.js",
            "./pyright_alright/pyright",
        ]
    )
    if return_code != 0:
        logger.error(f"Failed with code {return_code}")
        return


def main():
    clean_existing_pyright_artifacts()

    pyright_version = "1.1.378"

    pyright_archive = get_pyright_archive(pyright_version)

    store_pyright_archive_in_temp_directory(pyright_version, pyright_archive)

    install_pyright_dependencies(pyright_version)

    build_pyright(pyright_version)

    move_pyright_artifacts_to_pyright_alright(pyright_version)


if __name__ == "__main__":
    logging.basicConfig(handlers=[logging.StreamHandler()], level=logging.INFO)
    main()
