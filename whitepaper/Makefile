DOCNAME=report

all: report

.PHONY: clean

report:
	pdflatex $(DOCNAME).tex
	bibtex $(DOCNAME).aux
	pdflatex $(DOCNAME).tex
	pdflatex $(DOCNAME).tex

aspell: report
	aspell -c -t $(DOCNAME).tex -d en

view: report
	open $(DOCNAME).pdf

clean:
	rm -rf ${DOCNAME}.pdf *.bak *.blg *.bbl *.aux *.log *.out *.fdb_latexmk *.cut *.fls .DS_Store

