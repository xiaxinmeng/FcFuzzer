def cleanup():
    try:
        raise OSError
    except OSError as exc:
        raise MyLibError from exc