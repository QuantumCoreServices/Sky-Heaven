ring syntax,
    the NSLocalizedString function and the ObjectiveC specific format strings.

    All the tools that manipulate PO files can work with .strings files
    as well, if given the --stringtable-input and/or --stringtable-output
    option. To create a .strings file from a PO or POT file, use
    "msgcat --stringtable-output". To create a PO or POT file from a
    .strings file, use "xgettext".

  - GCC-source:

    xgettext's --language option now supports the value "GCC-source". This
    is like --language=C, except that in this mode, xgettext recognizes the
    special kind of format strings used in the GCC sources and marks them
    as 'gcc-internal-format'.

  - C++ with Qt:

    xgettext has a new option --qt that triggers the recognition and marking
    of Qt format strings.

    msgfmt has a new option --qt that generates binary message catalogs in
    Qt's .qm format.

* Data formats support:

  - Glade:
    xgettext now also supports Glade version 2.

* xgettext has a more reliable detection of format strings.  It now
  recognizes format strings depending on their position, for example as the
  second argument of fprintf(), regardless whether the literal string contains
  format directives.  This behaviour can be customized through the --flag
  option.

* libgettextpo library:

  - New functions for testing the obsolete/fuzzy/*-format flags of a message.
  - New convenience functions for extracting and analyzing the header entry.

* Portability:

  - C format strings with positions, as they arise when a translator needs to
    reorder a sentence, are now supported on all platforms. On those few
    platforms (NetBSD and Woe32) for which the native printf()/fprintf()/...
    functions don't support such format strings, replacements are provided
    through <libintl.h>.

  - A new configuration option --disable-libasprintf allows to build all of
    gettext except libasprintf; this is necessary on platforms for which
    libtool cannot create shared libraries with C++ code.

* Documentation:

  - Complete examples illustrating the use of gettext, including program
    sources, Makefile and autoconf infrastructure, have been added. They
    cover the following programming languages:
      C           (text mode, GNOME)
      C++         (text mode, Qt, KDE, GNOME)
      ObjectiveC  (text mode, GNUstep, GNOME)
      Shell       (text mode)
      Python      (text mode)
      Lisp        (text mode)
      librep      (text mode)
      Smalltalk   (text mode)
      Java        (text mode, AWT, Swing)
      awk         (text mode)
      Pascal      (text mode)
      YCP         (libyui)
      Tcl         (text mode, Tk)
      Perl        (text mode)
      PHP         (text mode)
