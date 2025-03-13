ction data are
    loaded and stored when the class is initialized. The transaction is run by
    calling the `run()` method, after the transaction is created (but before it is
    performed), the `post_transaction()` method needs to be called to verify no
    extra packages were pulled in and also to fix the reasons.
    Ú