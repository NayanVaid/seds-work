# Week 2 — The Sandbox

Cellular automata with falling sand and water.


## Brief

This is a simple sand and water sim made using pygame and numpy.

## Question 1

Swap grid starts as a copy of the grid rather than filled with zeroes because the rules
write a cell only when it is moving. If a cell does not move it will be not written in the copy grid hence 
it will disappear from the sim.

## Question 2

When randomised column order is replaced with a left to right scan the sand pile becomes lopsided and makes a cone
at 45 deg. This is because the left most cell will always be processed first and it will occupy the left diagonal
and the cycle would continue making a cone.
