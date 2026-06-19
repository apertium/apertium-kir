# Kyrgyz orthography conversion (transliteration / transcription)

This directory builds finite-state transducers that convert Kyrgyz between the **Cyrillic** script and other scripts/notations:

| Script / notation | twol rules        | lexc acceptor   | composed transducer            |
|-------------------|-------------------|-----------------|--------------------------------|
| Perso-Arabic      | `cyr-ara.twol`    | `cyr-ara.lexc`  | `cyr-ara.hfst` / `cyr-ara.ohfst` |
| Latin             | `cyr-lat.twol`    | `cyr-lat.lexc`  | `cyr-lat.hfst` / `cyr-lat.ohfst` |
| IPA               | `cyr-ipa.twol`    | `cyr-ipa.lexc`  | `cyr-ipa.hfst` / `cyr-ipa.ohfst` |

The approach follows Washington et al., *Multi-script morphological transducers
and transcribers for seven Turkic languages*
(<http://journals.linguisticsociety.org/proceedings/index.php/tu/article/view/4783>).

Each conversion is built by composing a **lexc acceptor** (which enumerates the
Cyrillic input alphabet and expands a few digraphs) with a **twol grammar**
(which performs the actual symbol-level conversion, e.g. `А:A`, `к:q` in
back-vowel contexts). The two layers are joined with
`hfst-compose-intersect`; this is why the lexc keeps Cyrillic on the right-hand
side while the script change happens in the twol.

## Building

These transducers are **not** built by the top-level `make`. Build them here:

```sh
# from the repository root, first build the monolingual transducer deps:
./autogen.sh && make
# then build the orthography transducers:
cd dev/ortho
make
```

`make` produces, among others, the optimised-lookup automata
`cyr-ara.ohfst`, `cyr-lat.ohfst` and `cyr-ipa.ohfst`, plus the
`kir@Cyrl-kir@...` transducers used by `apertium`/`hfst-proc`.

## Using the transducers

### Cyrillic to Latin

```sh
$ echo "тил" | hfst-lookup -q cyr-lat.ohfst
тил	til	3.000000
```

### Cyrillic to Perso-Arabic

Via `hfst-lookup`:

```sh
$ echo "кыргыз" | hfst-lookup -q cyr-ara.ohfst
кыргыз	قىرعىز	6.000000
```

Or via `hfst-proc` on the stream transducer (preserves token boundaries):

```sh
$ hfst-fst2fst -Oo kir@Cyrl-kir@Arab.hfst cyr-ara.hfst
$ echo "кыргыз тили" | hfst-proc kir@Cyrl-kir@Arab.hfst
^кыргыз/قىرعىز$ ^тили/تئلئ/تئلى/تىلئ/تىلى$
```

### Cyrillic to IPA

```sh
$ echo "кыргыз" | hfst-lookup -q cyr-ipa.ohfst
```

## Notes and limitations

* The Perso-Arabic mapping is currently tuned for **accepting** Perso-Arabic
  input (i.e. Arabic→Cyrillic), not for generating it perfectly. Generating
  fully correct Perso-Arabic from Cyrillic needs additional refinement of the
  mapping rules. See `cyr-ara.twol`.
* The Latin grammar resolves several `к/г` ↔ `k/q/g/ğ` back/front-vowel
  alternations (loanwords, onset clusters, word-final position). Remaining
  open cases are listed at the bottom of `cyr-lat.twol`.
* Multichar symbols emitted by a `twol` grammar must also be declared in the
  paired `lexc` file's `Multichar_Symbols` section, otherwise the symbol cannot
  round-trip through the composition.

## Reference

Original discussion and entry points:
<https://github.com/apertium/apertium-kir/issues/13>
