
Proof-of-concept for modular, extensible simulator for kidney allocation process.

This is an architecture prototype - only trivial event handlers have been written, not realistic ones, and some kinds of events are not yet defined. It has not yet been optimised for speed. A realistic simulator will need more complex event handlers and parsers to be useful.

Run with

`python simulator.py example/run_spec.yml`


The motivating architecture here is that it is easy to define new types of events, entities, variables, and event handlers.

The core simulator, `simulator.py`, is as generic as possible. It does not have any concept of a kidney or a patient, or of various kinds of events. These are all defined in `config.yml`, along with event handlers.

Concepts which are hard-coded into the core simulator are:
- dates: events occur in chronological order
- event lists, as lists of events to be processed (the core event loop does not care what the events are)
- state lists, as lists of entities to be maintained as part of the current state (the core event loop does not care what the entities are). The waitlist is an example.
- state variables, as other variables to be maintained as part of the current state

Event handlers are responsible for updating state lists and state variables, and possibly also updating event lists, in response to events.
