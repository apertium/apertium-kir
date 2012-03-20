STAMP=$(shell date)
DATE=$(shell date +%Y-%m-%d.%H:%M)
LOG=history.log
SRC=src.1000.txt
REF=ref.1000.txt
TST=tst.1000.txt.$(DATE)
all:
	cat $(SRC) | hfst-proc -w ../kir.automorf.hfst > $(TST)
	echo -ne $(STAMP)"\t" >> $(LOG)
	python3 evaluate-morph.py $(TST) $(REF) 2>> $(LOG)
