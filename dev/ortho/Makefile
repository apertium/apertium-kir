all: kir-ARA.autogen.hfst kir-MULTI.automorf.hfst

cyr-ara: cyr-ara.ohfst

# create full transcription transducer from lexc and twol transducers
cyr-ara.hfst: cyr-ara.twol.hfst cyr-ara.lexc.hfst
	hfst-compose-intersect -1 cyr-ara.lexc.hfst -2 cyr-ara.twol.hfst -o cyr-ara.hfst

# create transcription transducer optimised-lookup format
cyr-ara.ohfst: cyr-ara.hfst
	hfst-fst2fst -w -i $< -o $@

kir-ARA.spellrelax.hfst: kir-ARA.spellrelax.twol
	hfst-twolc $< -o $@

# create a transducer that generates Arabic script from 
# - Cyrillic-to-Arabic transcription transducer
# - Kazakh Cyrillic generation transducer
# оазис<n><px2sg><frm><gen>:ءوازيسىڭىزدىڭ
kir-ARA.autogen.hfst: cyr-ara.hfst ../../.deps/kir.RL.hfst
	hfst-compose -1 ../../.deps/kir.RL.hfst -2 $< -o $@

# Буддизм<n><dat>+шы<emph>:بۋدديزمگەشى
kir-ARA.REVautomorf.hfst: cyr-ara.hfst ../../.deps/kir.LR.hfst
	hfst-compose -1 ../../.deps/kir.LR.hfst -2 $< -o kir-ARA.REVautomorf.hfst

# بۋدديزمگەشى:Буддизм<n><dat>+шы<emph>
kir-ARA.automorf.hfst: kir-ARA.REVautomorf.hfst
	hfst-invert $< -o $@

# оазис<n><px2sg><frm><gen>:ءوازيسىڭىزدىڭ
#kaz-ARA.autogen.hfstol: kaz-ARA.autogen.hfst
#	hfst-fst2fst -w -i $< -o $@

# create a transducer that analyses Cyrillic and Arabic scipts from
# - Kazakh analysis transducer + error model
#    лукума<n><attr>:лукума
# - Kazakh Arabic reversed analyser
#    оазис<n><px2sg><frm><gen>:ءوازيسىڭىزدىڭ
#kir-MULTI.automorf.hfst: kir-ARA.REVautomorf.hfst ../../.deps/kir.LR.hfst ../../.deps/kir.LR.err.hfst kir-ARA.spellrelax.hfst
#	hfst-union -1 ../../.deps/kir.LR.hfst -2 ../../.deps/kir.LR.err.hfst | hfst-union -1 - -2 kir-ARA.REVautomorf.hfst | hfst-compose-intersect -1 - -2 kir-ARA.spellrelax.hfst | hfst-invert | hfst-fst2fst -w -o $@
kir-MULTI.automorf.hfst: kir-ARA.REVautomorf.hfst ../../.deps/kir.LR.hfst kir-ARA.spellrelax.hfst
	hfst-union -1 ../../.deps/kir.LR.hfst -2 kir-ARA.REVautomorf.hfst | hfst-compose-intersect -1 - -2 kir-ARA.spellrelax.hfst | hfst-invert | hfst-fst2fst -w -o $@

kir-MULTI.automorf.hfstol: kir-MULTI.automorf.hfst
	hfst-fst2fst -w -o $< $@

cyr-ara.lexc.hfst: cyr-ara.lexc
	hfst-lexc $< -o $@

cyr-ara.twol.hfst: cyr-ara.twol
	hfst-twolc $< -o $@

clean:
	rm -rf *.ohfst *.hfst
