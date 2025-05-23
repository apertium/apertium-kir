###############################################################################
## Makefile for apertium-kir
###############################################################################

LANG1=kir
BASENAME=apertium-$(LANG1)

TARGETS_COMMON = $(LANG1).automorf.hfst $(LANG1).autogen.hfst \
	$(LANG1).autopgen.bin \
	$(LANG1).automorf.bin $(LANG1).autogen.bin \
	$(LANG1).automorf.att.gz $(LANG1).autogen.att.gz \
	$(LANG1).autoseg.hfst $(LANG1).seggen.hfst \
        $(LANG1).rlx.bin \
		  .deps/$(LANG1).lexc.hfst

# This include defines goals for install-modes, .deps/.d and .mode files:
@ap_include@

###############################################################################
## Kyrgyz transducer
###############################################################################

.deps/$(LANG1).twol.hfst: $(BASENAME).$(LANG1).twol .deps/.d
	hfst-twolc $< -o $@

.deps/$(LANG1).twoc.hfst: $(BASENAME).$(LANG1).twoc .deps/.d
	hfst-twolc $< -o $@

.deps/$(LANG1).RL.lexc: $(BASENAME).$(LANG1).lexc .deps/.d
	cat $< | grep -v 'Dir/LR' | grep -v 'Use/MT' > $@

.deps/$(LANG1).LR.lexc: $(BASENAME).$(LANG1).lexc .deps/.d
	cat $< | grep -v 'Dir/RL' | grep -v 'Use/MT' > $@

.deps/$(LANG1).RL.lexc.hfst: .deps/$(LANG1).RL.lexc
	hfst-lexc -W -v $< -o $@

.deps/$(LANG1).LR.lexc.hfst: .deps/$(LANG1).LR.lexc
	hfst-lexc -W -v $< -o $@

.deps/$(LANG1).RL.hfst: .deps/$(LANG1).RL.lexc.hfst .deps/$(LANG1).twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).RL.lexc.hfst -2 .deps/$(LANG1).twol.hfst | hfst-invert -o $@

.deps/$(LANG1).LR.hfst: .deps/$(LANG1).LR.lexc.hfst .deps/$(LANG1).twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).LR.lexc.hfst -2 .deps/$(LANG1).twol.hfst | hfst-invert -o $@

$(LANG1).autogen.hfst: .deps/$(LANG1).RL.hfst .deps/$(LANG1).twoc.hfst
	hfst-compose-intersect -1 $< -2 .deps/$(LANG1).twoc.hfst | hfst-invert | hfst-fst2fst -w -o $@

$(LANG1).automorf.hfst: .deps/$(LANG1).LR.hfst .deps/$(LANG1).twoc.hfst dev/ortho/$(LANG1)-CYR.spellrelax.hfst
	hfst-compose-intersect -1 $< -2 .deps/$(LANG1).twoc.hfst | hfst-invert | hfst-compose-intersect -1 - -2 dev/ortho/$(LANG1)-CYR.spellrelax.hfst | hfst-invert | hfst-fst2fst -w -o $@

$(LANG1).autogen.att.gz: $(LANG1).autogen.hfst
	hfst-fst2txt $< | gzip -9 -c -n > $@

$(LANG1).automorf.att.gz: $(LANG1).automorf.hfst
	hfst-fst2txt $< | gzip -9 -c -n > $@

$(LANG1).autogen.bin: $(LANG1).autogen.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).autogen.att
	lt-comp lr .deps/$(LANG1).autogen.att $@

$(LANG1).automorf.bin: $(LANG1).automorf.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).automorf.att
	lt-comp lr .deps/$(LANG1).automorf.att $@

###############################################################################
## Segmenter
###############################################################################
# Segmenter generation:
# ^китеп<n><pl><px1pl><abl>/китеп\>тер\>ибиз\>ден$
#
# Auto segmenter:
# ^китептерибизден/китеп\>тер\>ибиз\>ден$

.deps/$(LANG1).seg.twol.hfst: $(BASENAME).$(LANG1)-seg.twol
	hfst-twolc $< -o $@

# segmentor generator
.deps/$(LANG1).RL-seg.hfst: .deps/$(LANG1).RL.lexc.hfst .deps/$(LANG1).seg.twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).RL.lexc.hfst -2 .deps/$(LANG1).seg.twol.hfst | hfst-minimise -o $@

$(LANG1).seggen.hfst: .deps/$(LANG1).RL-seg.hfst .deps/$(LANG1).twoc.hfst
	hfst-compose-intersect -1 $< -2 .deps/$(LANG1).twoc.hfst | hfst-fst2fst -w -o $@

.deps/$(LANG1).seg-prefix.bin: $(BASENAME).$(LANG1)-seg-prefix.lsx
	lsx-comp lr $< $@

.deps/$(LANG1).seg-prefix.hfst: .deps/$(LANG1).seg-prefix.bin
	lt-print -H $< | hfst-txt2fst -o $@

.deps/$(LANG1).seggen.hfst: $(LANG1).seggen.hfst
	hfst-fst2fst -t $< -o $@

#$(LANG1).seggen.bin: .deps/$(LANG1).seg-prefix.hfst .deps/$(LANG1).seggen.hfst
#	hfst-concatenate .deps/$(LANG1).seg-prefix.hfst .deps/$(LANG1).seggen.hfst | hfst-minimise | hfst-fst2txt -o .deps/$(LANG1).seggen.att
#	lt-comp -S lr .deps/$(LANG1).seggen.att $(LANG1).seggen.bin

# auto segmenter
.deps/$(LANG1).LR-seg.hfst: .deps/$(LANG1).LR.lexc.hfst .deps/$(LANG1).seg.twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).LR.lexc.hfst -2 .deps/$(LANG1).seg.twol.hfst | hfst-invert | hfst-minimise -o $@

.deps/$(LANG1).revmorph.hfst: $(LANG1).automorf.hfst
	hfst-fst2fst -t $< | hfst-invert -o $@

$(LANG1).autoseg.hfst: .deps/$(LANG1).LR-seg.hfst .deps/$(LANG1).twoc.hfst dev/ortho/$(LANG1)-CYR.spellrelax.hfst .deps/$(LANG1).revmorph.hfst
	hfst-compose-intersect -1 $< -2 .deps/$(LANG1).twoc.hfst | hfst-invert | hfst-compose-intersect -1 - -2 dev/ortho/$(LANG1)-CYR.spellrelax.hfst | hfst-invert | hfst-compose -1 - -2 .deps/$(LANG1).revmorph.hfst | hfst-invert | hfst-fst2fst -w -o $@


###############################################################################
## Debugging transducers (for testvoc)
###############################################################################

debug: .deps/$(LANG1).LR-debug.hfst .deps/$(LANG1).lexc.hfst

.deps/$(LANG1).LR-debug.hfst: $(BASENAME).$(LANG1).lexc .deps/.d
	cat $< | grep -v 'Dir/RL' | grep -v 'Use/Circ' > .deps/$(LANG1).LR-debug.lexc
	hfst-lexc -W .deps/$(LANG1).LR-debug.lexc -o .deps/$(LANG1).LR-debug.lexc.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).LR-debug.lexc.hfst -2 .deps/$(LANG1).twol.hfst -o $@

.deps/$(LANG1).lexc.hfst: .deps/$(LANG1).RL.lexc.hfst
	hfst-fst2fst -w -i $< -o $@

###############################################################################
## Postgeneration
###############################################################################

$(LANG1).autopgen.bin: $(BASENAME).post-$(LANG1).dix
	lt-comp lr $< $@

###############################################################################
## Disambiguation rules
###############################################################################

$(LANG1).rlx.bin: $(BASENAME).$(LANG1).rlx
	cg-comp $< $@

###############################################################################
## Spell checker
###############################################################################

$(LANG1).zhfst: .deps/acceptor.default.hfst .deps/errmodel.default.hfst
	rm -f $@
	zip -j $@ .deps/acceptor.default.hfst .deps/errmodel.default.hfst speller/index.xml

.deps/errmodel.default.hfst: .deps/words.default.hfst .deps/strings.default.hfst
	python dev/editdist.py -v -s -d 1 -e '@0@' -i speller/editdist.default.txt -a .deps/acceptor.default.hfst \
	| hfst-txt2fst  -e '@0@' -o .deps/editdist.default.hfst
	hfst-disjunct .deps/strings.default.hfst .deps/editdist.default.hfst \
	| hfst-minimise | hfst-repeat -f 1 -t 2 -o .deps/editstrings.default.hfst
	hfst-disjunct .deps/words.default.hfst .deps/editstrings.default.hfst \
	| hfst-fst2fst  -f olw -o $@

.deps/words.default.hfst: speller/words.default.txt
	grep -v -e "^#" -e "^$$" $< | hfst-strings2fst  -j -o $@

.deps/strings.default.hfst: speller/strings.default.txt .deps/anystar.hfst
	grep -v -e "^#" -e "^$$" $< | hfst-strings2fst  -j | hfst-concatenate .deps/anystar.hfst - |\
	hfst-concatenate - .deps/anystar.hfst -o $@

.deps/anystar.hfst:
	echo "?*;" | hfst-regexp2fst -S -o $@

.deps/acceptor.default.hfst: $(LANG1).autogen.hfst
	cat $< | hfst-fst2fst -t | hfst-project  --project=lower | hfst-minimise |hfst-fst2fst  -f olw -o $@

###############################################################################
## Spell relax
###############################################################################

dev/ortho/$(LANG1)-CYR.spellrelax.hfst: dev/ortho/$(LANG1)-CYR.spellrelax.twol
	hfst-twolc $< -o $@

###############################################################################
## Distribution
###############################################################################
EXTRA_DIST=$(BASENAME).$(LANG1).lexc \
	   $(BASENAME).$(LANG1).twol \
	   $(BASENAME).$(LANG1).rlx  \
	   $(BASENAME).post-$(LANG1).dix  \
	   modes.xml

###############################################################################
## Installation stuff
###############################################################################
#
#   apertium_kir_dir: This is where the compiled binaries go
#   apertium_kir_srcdir: This is where the source files go

apertium_kirdir=$(prefix)/share/apertium/$(BASENAME)/
apertium_kir_srcdir=$(prefix)/share/apertium/$(BASENAME)/

EXTRA_TARGETS=

#if HAVE_HFSTOSPELL
EXTRA_TARGETS += $(LANG1).zhfst
#endif # HAVE_HFSTOSPELL

apertium_kir_DATA=$(TARGETS_COMMON) $(EXTRA_TARGETS) $(LANG1).prob

pkgconfigdir = $(prefix)/share/pkgconfig
pkgconfig_DATA = $(BASENAME).pc

noinst_DATA=modes/$(LANG1)-morph.mode

install-data-local: install-modes
	test -d $(DESTDIR)$(apertium_kir_srcdir) || mkdir -p $(DESTDIR)$(apertium_kir_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).lexc $(DESTDIR)$(apertium_kir_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).twol $(DESTDIR)$(apertium_kir_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).rlx $(DESTDIR)$(apertium_kir_srcdir)
	$(INSTALL_DATA) $(BASENAME).post-$(LANG1).dix $(DESTDIR)$(apertium_kir_srcdir)

###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON)
clean-local:
	-rm -rf .deps modes

test: all
	apertium-regtest test
