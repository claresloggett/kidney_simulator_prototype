
Proof-of-concept for modular, extensible simulator for kidney allocation process.

The trivial simulator should include:
- initial waitlist, patient arrival list, patient event list, organ arrival list
- patients have only two variables, X and age (at listing).
    - Also have arrival time. Currently no SnapDate - this concept bears thinking about.
- organs have only one variable, Y
- patient status updates can change X
- patients die only of old age - these are incoming status events
- organs are always accepted
- grafts last a finite uniform amount of time
- all graft failures lead to relisting immediately after

Trivial and slightly less trivial experiments with allocation rules:
- organ is allocated to the earliest patient on the waitlist
- OR organ is allocated to the patient in the first 5 that has the X closest to Y
- OR organ is allocated to a patient who's been waiting longer than T, then to matching X

To experiment with state variables:
- organs get another variable, source, with two possible values
- the number of organs from each source allocated to patients above age A must be balanced

To experiment with weeder rules and cutpoints:
- patients are ineligible for low-Y organs if they are high-X or high age
