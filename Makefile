all: build/main.pdf

## hier Python-Skripte:
#build/plot.pdf: plot.py matplotlibrc header-matplotlib.tex | build
#	TEXINPUTS=$$(pwd): python plot.py
#

## hier weitere Abhängigkeiten für build/main.pdf deklarieren:

plots/hvR10B.pdf: python/hv.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python3 python/hv.py

plots/threshR20.pdf: python/thresh.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python3 python/thresh.py

plots/delay.pdf: python/delay.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python3 python/delay.py	
plots/tdc0.pdf:	 python/tdc.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python3 python/tdc.py
plots/p0.pdf:	 python/analysis.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python3 python/analysis.py	
		

build/main.pdf: plots/hvR10B.pdf plots/threshR20.pdf plots/delay.pdf  plots/tdc0.pdf plots/p0.pdf


build/main.pdf: FORCE | build
	  TEXINPUTS=build: \
	  BIBINPUTS=build: \
	  max_print_line=1048576 \
	latexmk \
	  --lualatex \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	main.tex


build:
	mkdir -p build
	mkdir -p plots
	
clean:
	rm -rf build

FORCE:

.PHONY: all clean
