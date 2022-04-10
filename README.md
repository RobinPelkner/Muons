# Muons
Report on the experiment regarding the Lifetime of Muons at UniBo.

HOW TO COMPILE:
Im using LUALATEX;
Just use MAKE to compile automated
The Latex file can also be compiled with:

latexmk \
	  --lualatex \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	main.tex

The python script however need to compile first
Please see the makefile on how to compile the python scripts.
