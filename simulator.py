
# This is the core event loop
# It does not handle any events, but farms them out to event handlers
# It does not have a concept of a "kidney" or "patient": these are defined in config.yml
# It *does* have a concept of state variables, state lists (e.g. waitlist), and event lists
# It *does* have a concept of dates and an effective fixed time granularity of one day

import argparse
import yaml
import json
import pandas as pd
import datetime as dt
import dateutil.parser

from utils import load_module

parser = argparse.ArgumentParser()
parser.add_argument('run_spec', metavar='run-spec', help='run specification file')
parser.add_argument('--master-config', default="config.yml",
                    help='top-level config file')
args = parser.parse_args()
#print("Arguments",args)

# Read master config
with open(args.master_config) as f:
    config = yaml.load(f)
#print(json.dumps(config, indent=2))

# Get modular functions
# Note that event lists have parsers and handlers; state lists only parsers
event_parser = dict()
event_handler = dict()
state_parser = dict()
for listname in config['event_lists'].keys():
    print("Loading parser for event list {} from {}".format(listname, config['event_lists'][listname]['parser']))
    module = load_module('parsers.events.'+listname, config['event_lists'][listname]['parser'])
    event_parser[listname] = module.parser
    print("Loading handler for event {} from {}".format(listname, config['event_lists'][listname]['event_handler']))
    module = load_module('handlers.events.'+listname, config['event_lists'][listname]['event_handler'])
    event_handler[listname] = module.handler
print("Event list parsers:",event_parser.keys())
# Note that state lists do not have event handlers
for listname in config['state_lists'].keys():
    print("Loading parser for state list {} from {}".format(listname, config['state_lists'][listname]['parser']))
    module = load_module('parsers.state.'+listname, config['state_lists'][listname]['parser'])
    state_parser[listname] = module.parser
print("State list parsers:",state_parser.keys())

def setup():
    with open(args.run_spec) as f:
        # NB currently no validation of run spec
        run_spec = yaml.load(f)
    input_files = {'event_lists': {},
                   'state_lists': {}}
    # Use run_spec file paths if provided, otherwise default paths from config.yml
    for listname in config['event_lists']:
        if listname in run_spec:
            input_files['event_lists'][listname] = run_spec[listname]
        else:
            input_files['event_lists'][listname] = config['event_lists'][listname]['default_path']
    for listname in config['state_lists']:
        if listname in run_spec:
            input_files['state_lists'][listname] = run_spec[listname]
        else:
            input_files['state_lists'][listname] = config['state_lists'][listname]['default_path']
    state_lists = {}
    state_variables = {}
    event_lists = {}
    # Use parsers to read lists
    # TODO: after parsing, should validate field names against variable fields from config
    for listname in config['event_lists'].keys():
        filename = input_files['event_lists'][listname]
        event_lists[listname] = event_parser[listname](filename)
    for listname in config['state_lists'].keys():
        filename = input_files['state_lists'][listname]
        state_lists[listname] = state_parser[listname](filename)
    print(event_lists)
    print(state_lists)
    return (state_lists, state_variables, event_lists, run_spec)

def main():
    state_lists, state_variables, event_lists, run_spec = setup()
    # Event loop
    # do we need waitlist to be treated specially - to be a variable?
    # prob no. entire state gets passed in to handlers. they can extract and treat it specially!
    start_date = dateutil.parser.parse(run_spec['start_date'])
    end_date = dateutil.parser.parse(run_spec['end_date'])
    date = start_date
    #timestep = dt.timedelta(days=1)
    # discard any events prior to start date
    events_remaining = sum([len(df) for df in event_lists.values()])
    print("{} events total".format(events_remaining))
    print("Discarding any events prior to {}".format(start_date))
    latest_date = start_date
    for (listname,df) in event_lists.items():
        df.sort_values(by='ArrivalDate', inplace=True)
        event_lists[listname] = df[df['ArrivalDate'] >= start_date]
        if len(df) > 0:
            if df['ArrivalDate'].iloc[-1] > latest_date:
                latest_date = df['ArrivalDate'].iloc[-1]
    after_latest = max(latest_date + dt.timedelta(days=1), end_date + dt.timedelta(days=1))
    # initialise dates
    next_dates = {listname:after_latest for listname in event_lists.keys()}
    for (listname,df) in event_lists.items():
        if len(df) > 0:
            next_dates[listname] = df['ArrivalDate'].iloc[0]
    events_remaining = sum([len(df) for df in event_lists.values()])
    print("{} events total remaining".format(events_remaining))

    # Core event loop
    print("\nBeginning event loop")
    while date < end_date:
        if events_remaining==0:
            break
        print("\nWas at date:",date)
        # Select next event and set date to that date (assert it is >= current date)
        next_event, next_date = min(next_dates.items(), key=lambda x: x[1])
        assert next_date >= date
        # Break if next date is after end_date
        if next_date > end_date:
            break
        print("Date now {} for event {}".format(next_date, next_event))
        date = next_date

        # Get event details
        # Call relevant event handler and pass it:
        # - event details
        # - state variable object, including waitlist. it may modify this
        # - any event lists. It may add to these
        # ... basically entire state?
        event_entity = event_lists[next_event].iloc[0,:]
        print(event_entity)
        event_lists[next_event] = event_lists[next_event].iloc[1:,:]
        if len(event_lists[next_event]) > 0:
            next_dates[next_event] = event_lists[next_event]['ArrivalDate'].iloc[0]
        else:
            next_dates[next_event] = after_latest
        events_remaining -= 1

        event_handler[next_event](date, event_entity, state_lists, state_variables, event_lists)

        # TODO: Log any desired logs

if __name__=="__main__":
    main()
