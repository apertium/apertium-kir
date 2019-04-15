"""Input CG3 output and gloss analyses with words from a bidix."""
import sys
import re
from collections import defaultdict


def get_pair(line):
    while "<b/>" in line:
        line = line.replace("<b/>", " ")
    feature = re.compile('<s n="([^"]*)"/>')
    leftside, rightside = line.partition("</l>")[0], line.partition("</l>")[2]
    left, right = re.search('<l>([^<]*)<', line).group(1), re.search('<r>([^<]*)<', line).group(1)
    leftfeats, rightfeats = re.findall(feature, leftside), re.findall(feature, rightside)
    return left, leftfeats, right, rightfeats


def glossify(dix, cg, left_tur=True):
    leftdic, rightdic = defaultdict(list), defaultdict(list)
    for line in open(dix):
        try:
            left, leftfeats, right, rightfeats = get_pair(line)
        except AttributeError:
            continue
        leftdic[left].append((leftfeats, right))
        rightdic[right].append((rightfeats, left))
    cg_out = []
    analysis = re.compile(';?\t"(.*)"(.*)')
    for line in open(cg):
        m = re.match(analysis, line)
        if m:
            feats = m.group(2).strip().split(" ")
            if "guio" in feats or "cm" in feats or "cm" in feats:
                cg_out.append(line.strip("\n"))
                continue
            glosses = []
            if left_tur:
                entries = rightdic[m.group(1)]
            else:
                entries = leftdic[m.group(1)]
            for entry in entries:
                if set(entry[0]) <= set(feats):
                    glosses.append(entry[1])
            if len(glosses) > 0:
                gloss = " " + " ".join(["<tur:" + w + ">" for w in sorted(glosses)])
                line = line.strip("\n") + gloss
                cg_out.append(line)
            else:
                cg_out.append(line.strip("\n"))
        else:
            cg_out.append(line.strip("\n"))
    return cg_out


if __name__ == "__main__":
    dixname, cgname = sys.argv[1], sys.argv[2]
    out = glossify(dixname, cgname)
    for line in out:
        print(line)


