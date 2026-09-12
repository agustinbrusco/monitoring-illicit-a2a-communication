TEX = apart-template

all: $(TEX).pdf

$(TEX).pdf: $(TEX).tex
	pdflatex -interaction=nonstopmode $(TEX).tex
	pdflatex -interaction=nonstopmode $(TEX).tex

# live rebuild on save (needs latexmk)
watch:
	latexmk -pdf -pvc -interaction=nonstopmode $(TEX).tex

clean:
	rm -f $(TEX).aux $(TEX).log $(TEX).out $(TEX).toc $(TEX).fls $(TEX).fdb_latexmk

distclean: clean
	rm -f $(TEX).pdf

.PHONY: all watch clean distclean
