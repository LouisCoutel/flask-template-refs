""" Class for storing template references pointing to their full name as recognized by Jinja """
from pathlib import Path
class TemplateRefs():
    """ Stores references """
    test_1 = 'test_1.jinja'
    test_2 = 'level_2/test_2.jinja'
    level_2_test_1 = 'level_2/test_1.jinja'
    level_3_test_2 = 'level_2/level_3/test_2.jinja'
    level_3_test_1 = 'level_2/level_3/test_1.jinja'
    bp_test = 'bp_test.jinja'
refs = TemplateRefs()