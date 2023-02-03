import glob
from os.path import basename, dirname, isfile, join

allModules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = allFiles = [basename(f)[:-3] for f in allModules if isfile(
    f) and not f.endswith('__init__.py') and not f.endswith('exampleModule.py')]
