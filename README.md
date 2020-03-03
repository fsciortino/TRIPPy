TRIPPy
======

Toroidal Radiation Inversion Protocol (Python)

Originally written by I.Fast, updated to Python 3 by F.Sciortino.

TRIPPy couples some C routines with Python code using f2py. To create the shared object library _bean.so run
f2py -c _beam.pyf _beam.c      # Python 2.7
or
f2py3 -c _beam.pyf _beam.c     # Python 3+

The rest of the package should be compatible with both Python 2.7 and Python 3+.
