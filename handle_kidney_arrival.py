
import pandas as pd

def handler(date, organ, state_lists, state_variables, event_lists):
    """
    Trivial event handler: remove top patient from waitlist if there are any.
    This patient is cured forever. Hooray!
    """
    print("Kidney arrival event handler called")
    assert date==organ['ArrivalDate']
    waitlist = state_lists['waitlist']
    if len(waitlist) > 0:
        waitlist = waitlist.iloc[1:,:]
    else:
        print("No available patients, discarding kidney.")
    state_lists['waitlist'] = waitlist
    print(waitlist)
