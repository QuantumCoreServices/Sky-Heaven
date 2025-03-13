 logic seems identical,
      except that no __safe_for_unpickling__ check is done (XXX this is
      a bug).  See INST for the gory details.

      NOTE:  In Python 2.3, INST and OBJ are identical except for how they
      get the class object.  That was always the intent; the implementations
      had diverged for accidental reasons.
      Ú