all: proverbs.conllu udtw23-kir.conllu

%.conllu: %.dep %.seg
	python3 ../scripts/conllise.py -e ../apertium-kir.kir.udx $< $(word 2,$^) > $@

test: kir-proverbs-disam-gold.txt kir-proverbs-disam-input.txt

kir-proverbs-disam-gold.txt: proverbs.dep
	grep -v '^#' $< | sed 's/ #.*//' | sed 's/ @.*//' | python3 apertium-regtest-hashifyCG.py > $@

kir-proverbs-disam-input.txt: proverbs.dep
	grep 'text =' $< | sed 's/# text = //' > $@

count: *.dep
	# Token count:
	grep "\"<" *.dep | wc -l
	# Sentence count:
	grep -r "# *text *=" *.dep | wc -l
