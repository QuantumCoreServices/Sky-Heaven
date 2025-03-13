
    is always safe to call stop() even if a retry is not pending.

    The retry callback, user_data and notify_interval may be specified
    in either the class init() or in the start() method for convenience.

    If notify_interval is set a 'pending_retry' signal will be emitted
    every time the notification interval elapses, this provides a
    countdown till the next retry attempt.

    The signature of the retry callback is: callback(retry_obj, user_data)

    The signature of the pending_retry signal handler is: callback(retry_obj, seconds_pending, user_data)

    The signature of the retry interval function is: interval(retry_obj, user_data)
    Úpending_retryNc