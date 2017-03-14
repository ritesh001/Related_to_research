import glob
import fnmatch
import pathlib
import os

pattern = '*.vasp'
path = '.'

##using os + fnmatch##
print fnmatch.filter(os.listdir(path),pattern)

##using glob##
print glob.glob(pattern)

##using pathlib##
path_ = pathlib.Path('.')
#lookup in current directory
print tuple(path_.glob(pattern))
#lookup recursively
print tuple(path_.rglob(pattern))
