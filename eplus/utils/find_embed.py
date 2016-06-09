# -*- encoding: UTF-8 -*-

embed = None


if not embed:
    try:
        from IPython import embed
    except ImportError:
        pass


if not embed:
    try:
        # old IPython
        from IPython.Shell import IPShell

        def embed():
            shell = IPShell(argv=[])
            shell.mainloop()
    except ImportError:
        pass


if not embed:
    try:
        from bpython import embed
    except ImportError:
        pass


if not embed:
    from code import interact as embed

