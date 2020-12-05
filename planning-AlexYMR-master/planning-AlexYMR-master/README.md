# Assignment 5 — Planning

## Warehouse Robots!

Welcome to your new job at _BroadLeaf_ (CEO Nosliw R. Nosaj\*).
You've been tasked with helping write the managerial software for the 
new high-tech warehouses located in New Seattle.

The job is pretty straightfoward: _BroadLeaf_ has a number of fancy 
pallet-moving robots that can help out in their warehouses, but they
haven't yet written software to control them. That's where you come
in, given your knowledge of computer science (and the fact that you're
an intern, which means that you're super cheap). You'll be applying
that knowledge on getting these robots to move stock around the 
warehouse.

The robots are capable of picking up pallets and moving them around 
the warehouse. Strong they might be, dextrous they are not. They can
get the pallets to the unloading area, but they need to rely on humans
to take the specific items off of them. This is typical of the real
world, where robots are _really_ good at parts of tasks that humans
fail at, but drop the ball completely when it comes to things like 
fine motor control.

\*The "R" stands for "Robotto."

## Your Task

* Fill in the domain file so that the remote planner can create a plan
to solve each of first five problem definitions.

You have been given _seven_ problem definitions and a skeleton of a 
domain file. The first five are problems that your domain needs to be
able to solve, the sixth and seventh are problems that your domain
should __fail to create a plan for__. This is to help you verify that
you're creating a domain that accounts for things like, e.g., not 
allowing an individual stock item to be in multiple shipments. _There
will be tests like this in our grading setup_. You will get graded on
whether you pass/fail tests that we expect you to.

### The Online Editor

You can find the online .pddl editor [here](
http://editor.planning.domains/#).

* You can upload all of the files that we've distributed using
`File>Load`.
* When you're ready to test, you can click `Solve`, select the domain
and problem definitions that you'd like to use, and then click `Plan`.
The system will run for a bit (for more complicated problems, upwards
of ten seconds) and then give you the results.
* Regularly save your work in GitHub.  Using `File>Save`, download
your work and push it to GitHub.  We will only be grading files
that you have pushed to GitHub

### The Domain File

We've given you a (very sparse) domain file. It contains the domain
name and the relevant PDDL requirements:

```
(define (domain sokorobotto)
  (:requirements :typing)
  (:types  )
  (:predicates  )
)
```

Your job is to add a number of things:

1. The `:types` of all of the objects in your domain.
2. The names of all of your `:predicates`. For the sake of grading, you
need to at a minimum include the predicate `includes`. You'll want a
bunch of intermediate predicates, too, but you can name them whatever
you want. For the record, our domain definition has about fifteen.
3. The bodies of all of these actions, including parameters, pre-conditions, 
and effects.


### Testing Your Work

We've given you a total of seven problem definitions. The first five
are tests that you need to pass. They increase in complexity, so don't
be surprised if initially you pass the first few but not the later 
ones.

The problem5_fail.pddl and problem6_fail.pddl are tests that you __should fail__. 
They're there to validate that your pre-conditions and effects are in good
shape.

You should create many more problem definitions to test your work.  Two of 
these problems that you define you should submit as your tests.  Please
add any two problem files, name them however you would like.  In your
answers.txt file, briefly describe each of these tests.  Your description
should include whether the problem should be solvable (or it should fail)
and what feature is being tested.

Use the scenarios in the slides for inspiration of additional tests
you can write.  Your tests should be validating your representation.  
Think about the preconditions to actions, how they interact with the
effects, and use tests to verify this interaction.  For example, are you
correctly checking whether a path for the robot is available?  A robot
cannot pass through other robots.  How would you check for that?

Tests should not be verfiying that the planner will reject poorly 
defined problems. In other words, failed tests due to invalid syntax,
referencing unknown constants, or the like will not be accepted.
In general, positive test cases are going to be more helpful for this exercise.


## Notes

* Refer to the included slides for more scenarios and definitions for 
each of the predicates.

* You should plan on using all of the predicates listed in the problem files.
While it is possible to develop a domain definition that does not use all of
the predicates, we are asking that you use all of them.

* When is an order complete?  You may want to create a check for when an 
order is complete, and only move a shipment when it is complete. 
However, we don't need to explicitly check for this, and you can move 
shipments from a packing location without this check.
The goal conditions of the problem will be used to determine if the shipment
is complete, and a successful plan will be one in which this condition has
been met.

* Problem 5 fails because `socks1` cannot be in two places at once.  This test
is checking the effects of actions for removing items from pallettes.

* Problem 6 fails because there is a missing `(no-pallette path4)`.  This test
is checking the preconditions for your move action(s).

* For an example domain/problem definition, you can click on `Import`.
There are a ton of old definitions from, e.g., planning competitions.
We looked at the IFC-2011 "barman" problem for guidance on how to 
write our PDDL files. You may find this useful.



## Questions

Include the answers to the following questions in your `answers.txt` file:

1.  How would you define a problem with one way paths?  For example, maybe the warehouse
has a giant ring where all robots move in one direction.  Give an example using five
locations setup in an unidirectional ring.

2.  What is the plan generated for problem0?  Is this the only valid plan?  Could a 
planner find a different plan?  If other valid plans are possible, provide an example
of an alternative plan that is valid.

3. (Extra credit) A common task in robotics is one called "pick-and-place".  The robot 
picks up an object, moves to another location, and places the object down.  This sequence 
of common actions is a natural fit for using an HTN.

Imagine we were solving Sokorobotto problems with an HTN instead of PDDL.  All 
of the actions you have defined are used as operators in the HTN.  You have defined a 
pick-and-place task.  Now define a method for the pick-and-place task using some of your 
PDDL actions you have defined.  You may use the following format for defining your method:

```
by-plane(a, x, y)
	task:	travel(a, x, y)
	precond: long-distance(x,y)
	subtasks:  <buy-ticket(a, a(x), a(y)), travel(a, x, a(x)), fly(a, a(x), a(y)), travel(a, a(y), y)>
```

