#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019-2024 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

import argparse
from pathlib import Path
import sys

# fix macOS locale-bug on startup: sets locale to LC_ALL (must be defined!)
import psychopy.locale_setup  # noqa


# NB the PsychoPyApp classes moved to _psychopyApp.py as of version 1.78.00
# to allow for better upgrading possibilities from the mac app bundle. this
# file now used solely as a launcher for the app, not as the app itself.


def main():
    from psychopy.app import startApp, quitApp
    from psychopy.preferences import prefs

    # parser to process input arguments
    argParser = argparse.ArgumentParser(
        prog="PsychoPyApp", description=(
"""Starts the PsychoPy3 application.

Usage:  python PsychoPy.py [options] [file]

Without options or files provided this starts PsychoPy using prefs to
decide on the view(s) to open.  If optional [file] is provided action
depends on the type of the [file]:

 Python script 'file.py' -- opens coder

 Experiment design 'file.psyexp' -- opens builder
 """
        )
    )
    # first argument is always the calling script
    argParser.add_argument("callscript")
    # recognise version query
    argParser.add_argument(
        "--version", "-v", dest="version", action="store_true", help=(
        "Print the current PsychoPy version."
    ))
    # add option to directly run a script
    argParser.add_argument(
        "-x", "--direct", dest="direct", action="store_true", help=(
            "Execute a script using StandAlone python"
        )
    )
    # add options for starting view
    argParser.add_argument(
        "--builder", "-b", dest="startView", const="builder", action="append_const", help=(
            "Open PsychoPy with a Builder window open. Combine with --coder/-c and --runner/-r "
            "to open a specific set of frames."
        )
    )
    argParser.add_argument(
        "--coder", "-c", dest="startView", const="coder", action="append_const", help=(
            "Open PsychoPy with the Coder window open. Combine with --builder/-b and --runner/-r "
            "to open a specific set of frames."
        )
    )
    argParser.add_argument(
        "--runner", "-r", dest="startView", const="runner", action="append_const", help=(
            "Open PsychoPy with the Runner window open. Combine with --coder/-c and --builder/-b "
            "to open a specific set of frames."
        )
    )
    # add option to show config wizard
    argParser.add_argument(
        "--firstrun", dest="firstRun", action="store_true", help=(
            "Launches configuration wizard"
        )
    )
    # add option to hide splash
    argParser.add_argument(
        "--no-splash", dest="showSplash", action="store_false", default=prefs.app['showSplash'], help=(
            "Suppresses splash screen"
        )
    )
    # treat any other args as filepaths
    argParser.add_argument(dest="startFiles", nargs="*", type=Path)

    args = argParser.parse_args(sys.argv)

    # run files directly if requested
    if args.direct:
        from psychopy import core
        import os
        # run all .py scripts from the command line using StandAlone python
        for targetScript in args.startFiles:
            # skip non-py files
            if not targetScript.suffix == ".py":
                continue
            # run file
            core.shellCall([sys.executable, targetScript.absolute()])
        sys.exit()
    # print version info if requested
    if '-v' in sys.argv or '--version' in sys.argv:
        from psychopy import __version__
        msg = ('PsychoPy3, version %s (c)Jonathan Peirce 2018, GNU GPL license'
               % __version__)
        print(msg)
        sys.exit()

    if (sys.platform == 'darwin' and
            ('| packaged by conda-forge |' in sys.version or
             '|Anaconda' in sys.version)):

        # On macOS with Anaconda, GUI applications used to need to be run using
        # `pythonw`. Since we have no way to determine whether this is currently
        # the case, we run this script again -- ensuring we're definitely using
        # pythonw.
        import os
        env = os.environ
        PYTHONW = env.get('PYTHONW', 'False')
        pyw_exe = sys.executable + 'w'

        # Updated 2024.1.6: as of Python 3, `pythonw` and `python` can be used
        # interchangeably for wxPython applications on macOS with GUI support.
        # The defaults and conda-forge channels no longer install python with a
        # framework build (to do so: `conda install python=3.8 python.app`).
        # Therefore `pythonw` often doesn't exist, and we can just use `python`.
        if PYTHONW != 'True' and os.path.isfile(pyw_exe):
            from psychopy import core
            cmd = [pyw_exe] + sys.argv

            stdout, stderr = core.shellCall(cmd,
                                            env=dict(env, PYTHONW='True'),
                                            stderr=True)
            print(stdout, file=sys.stdout)
            print(stderr, file=sys.stderr)
            sys.exit()
        else:
            startApp(
                startView=args.startView, 
                showSplash=args.showSplash, 
                startFiles=args.startFiles,
                firstRun=args.firstRun
            )
    else:
        # start app
        _ = startApp(
            startView=args.startView, 
            showSplash=args.showSplash, 
            startFiles=args.startFiles,
            firstRun=args.firstRun
        )
        quitApp()


if __name__ == '__main__':
    main()