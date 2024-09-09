# pyright: strict
import subprocess
import sys
from os import path


def pyright():
    pyright_alright_directory = path.dirname(path.realpath(__file__))
    pyright_index = path.join(pyright_alright_directory, "pyright/index.js")
    return_code = subprocess.call(["bun", "run", pyright_index, *sys.argv[1:]])

    sys.exit(return_code)


if __name__ == "__main__":
    pyright()
