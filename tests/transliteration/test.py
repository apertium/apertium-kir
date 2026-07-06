#!/usr/bin/env python3
# coding=utf-8
#
# Transliteration test for apertium-kir orthography transducers.
#
# Checks that the compiled Cyrillic->Latin and Cyrillic->Perso-Arabic
# transducers (built in dev/ortho/) produce the expected output for a set
# of words. A pair passes if the expected output appears anywhere among the
# transducer's outputs for that input (the Perso-Arabic mapping is
# intentionally ambiguous in places, see issue #13).
#
# USAGE:
#   python3 test.py                  # uses ./translit.tsv, transducers in ../../dev/ortho
#   python3 test.py <tsv> <orthodir>
#
# Requires the `hfst-lookup` binary on PATH.

import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

tsv = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "translit.tsv")
ortho = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "..", "dev", "ortho")

TRANSDUCERS = {
    "lat": os.path.join(ortho, "cyr-lat.ohfst"),
    "ara": os.path.join(ortho, "cyr-ara.ohfst"),
}


def lookup(transducer, word):
    """Return the set of output strings hfst-lookup gives for `word`."""
    proc = subprocess.run(
        ["hfst-lookup", "-q", transducer],
        input=(word + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    outs = set()
    for line in proc.stdout.decode("utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        cols = line.split("\t")
        if len(cols) >= 2 and cols[1] != "+?":
            outs.add(cols[1])
    return outs


def main():
    for name, path in TRANSDUCERS.items():
        if not os.path.exists(path):
            sys.stderr.write(
                "ERROR: transducer not found: %s\n"
                "       Build it first: (cd dev/ortho && make)\n" % path
            )
            return 2

    total = 0
    passed = 0
    with open(tsv, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) != 3:
                sys.stderr.write("Skipping malformed line: %r\n" % raw)
                continue
            script, src, expected = cols
            if script not in TRANSDUCERS:
                sys.stderr.write("Unknown script %r in line: %r\n" % (script, raw))
                continue
            total += 1
            outs = lookup(TRANSDUCERS[script], src)
            if expected in outs:
                passed += 1
                print("+\t%s\t%s\t%s" % (script, src, expected))
            else:
                got = ", ".join(sorted(outs)) if outs else "(no output)"
                print("-\t%s\t%s\texpected=%s\tgot=%s" % (script, src, expected, got))

    print("\nPASS:\t%d/%d" % (passed, total))
    return 0 if passed == total and total > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
