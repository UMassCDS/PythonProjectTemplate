# Avoid RuntimeWarnings about double imports when executing scripts, see https://stackoverflow.com/questions/43393764/python-3-6-project-structure-leads-to-runtimewarning
import sys

if not "-m" in sys.argv:
    from . import corpus_counter_script
    from . import word_count
    from . import utils

