Kyrgyz

                            apertium-kir
===============================================================================

This is an Apertium monolingual language package for Kyrgyz. What
you can use this language package for:

* Morphological analysis of Kyrgyz
* Morphological generation of Kyrgyz
* Part-of-speech tagging of Kyrgyz

Requirements
-------------------------------------------------------------------------------

You will need the following software installed:

* lttoolbox (>= 3.3.0)
* apertium (>= 3.3.0)
* vislcg3 (>= 0.9.9.10297)
* hfst (>= 3.8.2)

If this does not make any sense, we recommend you look at: www.apertium.org.

Compiling
-------------------------------------------------------------------------------

Given the requirements being installed, you should be able to just run:

    $ ./configure
    $ make

You can use `./autogen.sh` instead of `./configure` if you're compiling
from source.

If you're doing development, you don't have to install the data, you
can use it directly from this directory.

If you are installing this language package as a prerequisite for an
Apertium translation pair, then do (typically as root / with sudo):

    # make install

You can give a `--prefix` to `./configure` to install as a non-root user,
but make sure to use the same prefix when installing the translation
pair and any other language packages.

Testing
-------------------------------------------------------------------------------

If you are in the source directory after running make, the following
commands should work:

* Morphological analysis:

    $ echo "Бул кыргызча морфологиялык талдоо" | apertium -d . kir-morph
    ^Бул/бул<det><dem>/бул<prn><dem><nom>/бул<prn><dem><nom>+э<cop><aor><p3><pl>/бул<prn><dem><nom>+э<cop><aor><p3><sg>$ ^кыргызча/кыргызча<adv>/кыргызча<n><attr>/кыргызча<n><nom>/кыргызча<n><nom>+э<cop><aor><p3><pl>/кыргызча<n><nom>+э<cop><aor><p3><sg>$ ^морфологиялык/морфологиялык<adj>/морфологиялык<adj>+э<cop><aor><p3><pl>/морфологиялык<adj>+э<cop><aor><p3><sg>$ ^талдоо/талда<v><tv><ger><nom>/талда<v><tv><ger><nom>+э<cop><aor><p3><pl>/талда<v><tv><ger><nom>+э<cop><aor><p3><sg>$^./.<sent>$

* Tagging (analysis + disambiguation):

    $ echo "Бул кыргызча морфологиялык талдоо" | apertium -d . kir-tagger
    ^Бул/бул<det><dem>$ ^кыргызча/кыргызча<adv>$ ^морфологиялык/морфологиялык<adj>$ ^талдоо/талда<v><tv><ger><nom>$^./.<sent>$


* Morphological generation:

    $ echo "^бул<prn><dem><nom>$ ^кыргызча<adv>$ ^морфологиялык<adj>$ ^талда<v><tv><ger><nom>+э<cop><aor><p3><sg>$" | apertium -f none -d . kir-gener
    бул кыргызча морфологиялык талдоо


Files and data
-------------------------------------------------------------------------------

* `apertium-kir.kir.lexc`          - Morphotactic dictionary
* `apertium-kir.kir.twol`          - Morphophonological rules
* `apertium-kir.kir.rlx`           - Constraint Grammar disambiguation rules
* `apertium-kir.post-kir.dix`      - Post-generator
* `kir.prob`                       - Tagger model
* `modes.xml`                      - Translation modes

For more information
-------------------------------------------------------------------------------

* http://wiki.apertium.org/wiki/Installation
* http://wiki.apertium.org/wiki/apertium-kir
* http://wiki.apertium.org/wiki/Using_an_lttoolbox_dictionary

Help and support
-------------------------------------------------------------------------------

If you need help using this language pair or data, you can contact:

* Mailing list: apertium-stuff@lists.sourceforge.net
* IRC: `#apertium` on `irc.freenode.net`

See also the file AUTHORS included in this distribution.
