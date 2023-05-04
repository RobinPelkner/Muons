# Muons
## Report on the experiment regarding the Lifetime of Muons at UniBo.

HOW TO COMPILE:
Im using `LUALATEX`. Use `MAKE` to compile automatically
The Latex file can also be compiled with: 
```
latexmk \
	  --lualatex \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	main.tex
```
The python script however need to compile first.
Please consult the makefile on how to compile the python scripts.
