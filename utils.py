
import importlib.util

# this is a bit horrible in python 3.6, so wrap it in a function
def load_module(module_name, path):
    """
    Load a module from an arbitrary python file.
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

#ppl = load_module('ppl', 'parse_patient_lists.py')
# does not work #from ppl import parse_patient_lists
#waitlist = ppl.parse_patient_lists('waitlist.txt')
#print(waitlist)
