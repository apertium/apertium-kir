
# Input is two files, one LU per line:
#
# ^айрымаланып/айрымала<v><tv><pass><gna_perf>/айрымала<v><tv><pass><prc_real>$
# ^өнүгүшүн/өнүк<v><tv><ger_pres><px3pl><acc>/өнүк<v><tv><ger_pres><px3sg><acc>$
# ^убакка/убак<n><dat>$
# ^Бордюжа/*Бордюжа$
# ^кытайлыктар/*кытайлыктар$
# ^акысынын/акы<n><px3pl><gen>/акы<n><px3sg><gen>$
# ^атышат/ат<v><tv><aor><p3><pl>/ат<v><tv><coop><aor><p3><pl>/ат<v><tv><coop><aor><p3><sg>/ат<v><tv><coop><prc_irre>/атыш<v><iv><aor><p3><pl>/атыш<v><iv><aor><p3><sg>/атыш<v><iv><prc_irre>/жат<vaux><aor><p3><pl>/жат<vaux><coop><aor><p3><pl>/жат<vaux><coop><aor><p3><sg>/жат<vaux><coop><prc_irre>$
# ^Армения/Армения<np><top><nom>$
# 
# The first file is the TEST file, the second is the REF file

# The program calculates precision, recall and F-score.
# The program also calculates for each line, the analysis diff.

# precision = number of correct analyses / (number of correct analyses + number of incorrect analyses)
# recall = number of correct analyses / (number of correct analyses + number of missing analyses)
# F-score = (precision * recall) / (precision + recall)

