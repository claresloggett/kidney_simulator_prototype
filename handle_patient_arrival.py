
import pandas as pd

def handler(date, patient, state_lists, state_variables, event_lists):
    """
    Trivial event handler: add patient to waitlist
    """
    print("Patient arrival handler called")
    print("Patient {} arrived".format(patient['ID']))
    assert date==patient['ArrivalDate']
    waitlist = state_lists['waitlist']
    waitlist = waitlist.append(patient, ignore_index=True)
    # Alternatively we could return and replace the state, functional-style, but this seems slow
    state_lists['waitlist'] = waitlist
    print(waitlist)
