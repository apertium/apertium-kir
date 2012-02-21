###############################################################################
## Makefile for Kyrgyz
###############################################################################

VERSION=0.2.0
LANG=kir

BASENAME=apertium-$(LANG)

SUBDIRS = .

TARGETS_COMMON = $(LANG).autogen.hfst $(LANG).automorf.hfst

###############################################################################
## Kyrgyz transducer
###############################################################################

.deps/kir.lexc.morf.hfst-debug: apertium-$(LANG).lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	cat $< | grep -v -e 'Dir/RL' -e 'Use/Circ' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
#	rm $@tmp $@.foma

.deps/kir.lexc.gen.hfst-debug: apertium-$(LANG).lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	cat $< | grep -v -e 'Dir/LR' -e 'Use/Circ' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
#	rm $@tmp $@.foma

.deps/kir.lexc.morf.hfst: $(BASENAME).lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	cat $< | grep -v 'Dir/RL' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
#	rm $@tmp $@.foma

.deps/kir.lexc.gen.hfst: $(BASENAME).lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	cat $< | grep -v 'Dir/LR' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
#	rm $@tmp $@.foma

.deps/kir.twol.hfst: $(BASENAME).twol
	hfst-twolc -R -i $(BASENAME).twol -o $@

# kir generator:
.deps/$(LANG).autogen.hfst: .deps/kir.lexc.gen.hfst .deps/kir.twol.hfst
	hfst-compose-intersect -1 .deps/kir.lexc.gen.hfst -2 .deps/kir.twol.hfst -o $@

$(LANG).autogen.hfst: .deps/$(LANG).autogen.hfst
	hfst-fst2fst -w -i $< -o $@

# kir analyser:
.deps/$(LANG).automorf.hfst: .deps/kir.lexc.morf.hfst .deps/kir.twol.hfst
	hfst-compose-intersect -1 .deps/kir.lexc.morf.hfst -2 .deps/kir.twol.hfst -o $@tmp
	hfst-invert -i $@tmp -o $@
	rm $@tmp

$(LANG).automorf.hfst: .deps/$(LANG).automorf.hfst
	hfst-fst2fst -w -i $< -o $@

# debug stuff:
.deps/$(LANG).automorf.hfst-debug: .deps/kir.lexc.morf.hfst-debug .deps/kir.twol.hfst
	hfst-compose-intersect -1 .deps/kir.lexc.morf.hfst-debug -2 .deps/kir.twol.hfst | hfst-invert -o $@

.deps/$(LANG).autogen.hfst-debug: .deps/kir.lexc.gen.hfst-debug .deps/kir.twol.hfst
	hfst-compose-intersect -1 .deps/kir.lexc.gen.hfst-debug -2 .deps/kir.twol.hfst -o $@

EXTRA_DIST=$(BASENAME).lexc $(BASENAME).twol

apertium_kir_DATA=$(LANG).automorf.hfst $(LANG).autogen.hfst
apertium_kirdir=$(prefix)/share/apertium/$(BASENAME)/


CLEANFILES = -r $(TARGETS_COMMON) .deps/
