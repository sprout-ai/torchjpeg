# setup.py
import subprocess
import pathlib
from setuptools import setup
from setuptools.command.build_ext import build_ext
from torch.utils.cpp_extension import BuildExtension, CppExtension

# Path to your libjpeg folder
libjpeg_dir = pathlib.Path(__file__).resolve().parent / "src" / "libjpeg"

class CustomBuildExt(BuildExtension):
    """Run libjpeg's configure/make before building our C++ extension."""
    def run(self):
        # 1) Build the static libjpeg library:
        subprocess.check_call(
            "cd src/libjpeg && ./configure --enable-static --with-pic && make",
            shell=True
        )
        # 2) Let the normal PyTorch C++ extension build happen:
        super().run()

ext_modules = [
    CppExtension(
        "torchjpeg.codec._codec_ops",
        [
            "src/torchjpeg/codec/codec_ops.cpp",
        ],
        include_dirs=[str(libjpeg_dir)],
        extra_objects=[str(libjpeg_dir / ".libs" / "libjpeg.a")],
        extra_compile_args=["-std=c++17"],
    ),
]

setup(
    # Most metadata is read from pyproject.toml (PEP 621),
    # but you define your extension modules & custom command here:
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},
)
