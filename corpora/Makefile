all: proverbs.conllu

proverbs.conllu: proverbs.dep proverbs.seg
	python3 ../scripts/conllise.py ../apertium-kir.kir.udx proverbs.dep proverbs.seg > $@

test: kir-proverbs-disam-gold.txt kir-proverbs-disam-input.txt

kir-proverbs-disam-gold.txt: proverbs.dep
	grep -v '^#' $< | sed 's/ #.*//' | sed 's/ @.*//' > $@

kir-proverbs-disam-input.txt: proverbs.dep
	grep 'text =' $< | sed 's/# text = //' > $@
