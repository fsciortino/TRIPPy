# Usage:
# make           # generate TRIPPy shared-object library
# make clean     # delete previous versions of the TRIPPy shared-object library

.PHONY: all trippy clean

flags="-fast"
fcompiler=intelem
#flags=
#fcompiler=gnu95


############

all: trippy

trippy : 
	@echo "Generating TRIPPy shared-object library"
	@echo "Intel compiler flags: " ${flags}
	f2py3 -c --compiler=intelem _beam.pyf _beam.c --opt=${flags}

#f2py3 -c --fcompiler=${fcompiler} -m _beam _beam.c --opt=${flags} 


clean : 
	@echo "Eliminating TRIPPy shared-object library"
	rm _beam.cpython-36m-x86_64-linux-gnu.so

#rm *.so
