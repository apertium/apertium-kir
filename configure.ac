AC_PREREQ(2.52)

AC_INIT([apertium-tr-az], [0.1.0], [mipasov@gmail.com])
AM_INIT_AUTOMAKE([apertium-tr-az], [0.1.0], no-define)
AC_PROG_LN_S
AC_PROG_AWK

AC_DEFUN([PKG_CHECK_APERTIUM], [
  APERTIUM_VER=0
  PKG_CHECK_MODULES(APERTIUM, apertium-3.2 >= 3.2.0,
  [
      APERTIUM_VER=32
  ],
  [
      PKG_CHECK_MODULES(APERTIUM, apertium-3.1 >= 3.1.0,
      [
          APERTIUM_VER=31
      ],
      [
          PKG_CHECK_MODULES(APERTIUM, apertium-3.0 >= 3.0.0,
          [
              APERTIUM_VER=30
          ])
      ])
  ])
  AC_SUBST(APERTIUM_VER)
])
                          
PKG_CHECK_APERTIUM

#AC_DEFUN([PKG_CHECK_HFST], [
#  HFST_VER=0
#  PKG_CHECK_MODULES(HFST, hfst-3.2 >= 3.2.0,
#  [
#      HFST_VER=32
#  ],
#  [
#      PKG_CHECK_MODULES(HFST, hfst-3.1 >= 3.1.0,
#      [
#          HFST_VER=31
#      ],
#      [
#          PKG_CHECK_MODULES(HFST, hfst-3.0 >= 3.0.0,
#          [
#              HFST_VER=30
#          ])
#      ])
#  ])
#  AC_SUBST(HFST_VER)
#])
#                          
#PKG_CHECK_HFST

AC_PATH_PROG(HFSTCALC, hfst-lexc, no)
if test x$ac_cv_path_HFSTCALC = x
then
  AC_MSG_ERROR([You don't have hfst-calculate installed.])
fi
if test x$ac_cv_path_HFSTCALC = xno
then
  AC_MSG_ERROR([You don't have hfst-calculate installed.])
fi

AC_PATH_PROG(CGCOMP, cg-comp, no)
if test x$ac_cv_path_CGCOMP = x
then
  AC_MSG_ERROR([You don't have cg-comp installed.])
fi
if test x$ac_cv_path_CGPROC = xno
then
  AC_MSG_ERROR([You don't have cg-comp installed.])
fi

AC_PATH_PROG(CGPROC, cg-proc, no)
if test x$ac_cv_path_CGPROC = x
then
  AC_MSG_ERROR([You don't have cg-proc installed.])
fi
if test x$ac_cv_path_CGPROC = xno
then
  AC_MSG_ERROR([You don't have cg-proc installed.])
fi

#AC_OUTPUT([Makefile morph-tr/Makefile])
AC_OUTPUT([Makefile])
