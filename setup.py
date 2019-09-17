import sys
import os
import shutil

from distutils.command.clean import clean as Clean

from numpy.distutils.command.build_ext import build_ext
from numpy.distutils.misc_util import Configuration
from numpy.distutils.core import setup


sys.argv = ['setup.py', 'build_ext', '-i']

#sys.argv = ['setup.py', 'clean']

import builtins
builtins.__MREX_SETUP__ = True
from mrex._build_utils.openmp_helpers import get_openmp_flag
import mrex
VERSION = mrex.__version__


# Custom clean command to remove build artifacts
class CleanCommand(Clean):

    description = "Remove build artifacts from the source tree"

    def run(self):

        Clean.run(self)

        if os.path.exists('build'):
            shutil.rmtree('build')

        for dirpath, dirnames, filenames in os.walk('mrex'):
            for filename in filenames:
                if any(filename.endswith(suffix) for suffix in
                       (".so", ".pyd", ".dll", ".pyc")):
                    os.unlink(os.path.join(dirpath, filename))
                    continue
                extension = os.path.splitext(filename)[1]
                if extension in ['.c', '.cpp']:
                    pyx_file = str.replace(filename, extension, '.pyx')
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


class build_ext_subclass(build_ext):
    def build_extensions(self):

        if not os.getenv('MREX_NO_OPENMP'):
            openmp_flag = get_openmp_flag(self.compiler)

            for e in self.extensions:
                e.extra_compile_args += openmp_flag
                e.extra_link_args += openmp_flag

        build_ext.build_extensions(self)


cmdclass = {
    'clean': CleanCommand,
    'build_ext': build_ext_subclass,
}


def configuration(parent_package='', top_path=None):

    config = Configuration(None, parent_package, top_path)
    # Avoid non-useful msg:
    # "Ignoring attempt to set 'name' (from ... "
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)
    config.add_subpackage('mrex')
    return config


setup(version=VERSION, cmdclass=cmdclass, configuration=configuration)
