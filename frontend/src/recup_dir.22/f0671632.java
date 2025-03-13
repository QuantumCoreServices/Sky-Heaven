he code
      first insists that the class object have a __safe_for_unpickling__
      attribute.  Unlike as for the __safe_for_unpickling__ check in REDUCE,
      it doesn't matter whether this attribute has a true or false value, it
      only matters whether it exists (XXX this is a bug).  If
      __safe_for_unpickling__ doesn't exist, UnpicklingError is raised.

      Else (the class object does have a __safe_for_unpickling__ attr),
      the class object obtained from INST's arguments is applied to the
      argtuple obtained from the stack, and the resulting instance object
      is pushed on the stack.

      NOTE:  checks for __safe_for_unpickling__ went away in Python 2.3.
      NOTE:  the distinction between old-style and new-style classes does
             not make sense in Python 3.
      Ú