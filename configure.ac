AC_PREREQ(2.52)

AC_INIT([Apertium Kyrgyz], [0.1.1], [apertium-stuff@lists.sourceforge.net], [apertium-kir], [https://wiki.apertium.org/wiki/Apertium-kir])
AM_INIT_AUTOMAKE
AC_PROG_AWK

dnl Find a Python interpreter for the speller helper (dev/editdist.py),
dnl which now runs under both Python 2 and 3. Prefer python3, then a
dnl generic python, then python2. Can be overridden with PYTHON=... .
AC_ARG_VAR([PYTHON], [Python interpreter to use for build helper scripts])
AC_PATH_PROGS([PYTHON], [python3 python python2], [python])

dnl HFST support
AH_TEMPLATE(HAVE_HFSTOSPELL, [Have HFSTOSPELL])
AC_ARG_ENABLE(ospell, AC_HELP_STRING([--enable-ospell],
        [enable HFST spellchecking backend]),
        [hfstospell=${enableval}], [hfstospell=no])
dnl must be AS_IF for some aclocals to pick PKG_CHECK_MODULES somehow.
dnl AC_PROVIDE_IFELSE doesn't work on mac?
AS_IF([test x$hfstospell = xyes], [
      PKG_CHECK_MODULES([HFSTOSPELL], [hfstospell >= 0.2])
          AC_DEFINE(HAVE_HFSTOSPELL, 1)
          CXXFLAGS="$CXXFLAGS $HFSTOSPELL_CFLAGS"
        ])
AM_CONDITIONAL([HAVE_HFSTOSPELL], [test x$hfstospell = xyes])

PKG_CHECK_MODULES(APERTIUM, apertium >= 3.6.1)
PKG_CHECK_MODULES(LTTOOLBOX, lttoolbox >= 3.5.1)
PKG_CHECK_MODULES(CG3, cg3 >= 1.3.0)
PKG_CHECK_MODULES(HFST, hfst >= 3.15.0)

PKG_CHECK_MODULES(REGTEST, apertium-regtest >= 0.0.1, [],
                  [AC_MSG_WARN([Running tests requires apertium-regtest])])

AP_MKINCLUDE

AC_OUTPUT([Makefile apertium-kir.pc])
