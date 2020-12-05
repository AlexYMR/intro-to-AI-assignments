# Assignment 3—Search

## Back Story

You and Willie have co-founded a meal trading startup called BigByte. The company allows people to send their meal to 
someone else in trade for either a meal or an I-Owe-You.  The company consists of two people, you and Willie, both 
alumni of Fandom College. Of the two, you take care of the software engineering and Willie does the delivery by bicycle.


BigByte's target customers are all based around the Fandom campus.  Many of the customers will be clustered near a 
small set of buildings, but pathways between buildings can have a heavily fluctuating number of people on them.  To 
deliver the food quickly and efficiently, you may need to avoid pathways that have too many people.  Willie has asked 
you to come up with a route planning system to find the best routes for his deliveries.

All major map services are expensive and your start-up begins its services in a week, so you'll have to come up with 
something yourself and do it fast. Fortunately, the campus is easily navigable using a few landmark buildings, and you 
only need to tell Willie how to best reach one landmark from another. You have a printed map of the campus and data 
from a foot traffic survey maintained by College Archive. For you, that means you only need to write one more piece of 
software before the launch: an implementation of the **A\* algorithm** that finds the best way to travel between any pair of 
landmark buildings on campus.



## Task Parameters

A diagram explaining the relative position of landmark buildings of the Fandom College campus is shown below. 

<img src="map.png" width="60%">

Your A\* algorithm will calculate fastest route between any pairs of the landmarks. 
You will be given two routing maps as inputs. The first map specifies the straight-line distance 
between two landmarks (Willie measured the printed map and did the data entry); 
we will refer to this as the **distance map**. The second map is based on the data from the Archive traffic survey. 
It specifies the expected time it takes a driver to go from one landmark to a neighboring landmark; 
we will refer to this as the **time map**. 
The data in the distance map is used as the heuristics, the h(n) in your A\*.  The time map is used to calculate the 
path cost, the g(n) in your A\*.  Note that g(n) is the total path cost up to n, but the time map only gives you the 
time to travel between pairs of points.  You will still need to calculate the total path cost.

When passed to your A\* implementation, both the distance map and the time map are stored in the 
same format (a Python dictionary). The following is an example time map.

```python
time_map1 = {
	'Big Ben':{'Big Ben':None, 'Big Cannon Hall':20, 'College Column':None, 'Hackathon Laboratory':30, 'Library':None, 'Multicultural Center':None, 'Stagger Hall':None},
	'Big Cannon Hall':{'Big Ben':15, 'Big Cannon Hall':None, 'College Column':None, 'Hackathon Laboratory':None, 'Library':100, 'Multicultural Center':None, 'Stagger Hall':80},
	'College Column':{'Big Ben':None, 'Big Cannon Hall':None, 'College Column':None, 'Hackathon Laboratory':50, 'Library':None, 'Multicultural Center':100, 'Stagger Hall':100},
	'Hackathon Laboratory':{'Big Ben':30, 'Big Cannon Hall':None, 'College Column':50, 'Hackathon Laboratory':None, 'Library':None, 'Multicultural Center':None, 'Stagger Hall':30},
	'Library':{'Big Ben':None, 'Big Cannon Hall':90, 'College Column':None, 'Hackathon Laboratory':None, 'Library':None, 'Multicultural Center':None, 'Stagger Hall':20},
	'Multicultural Center':{'Big Ben':None, 'Big Cannon Hall':None, 'College Column':90, 'Hackathon Laboratory':None, 'Library':None, 'Multicultural Center':None, 'Stagger Hall':40},
	'Stagger Hall':{'Big Ben':None, 'Big Cannon Hall':80, 'College Column':90, 'Hackathon Laboratory':30, 'Library':20, 'Multicultural Center':30, 'Stagger Hall':None}
}
```

In this example, the traffic time between Big Ben and Big Cannon Hall is `20`. `None` indicates that there is no path which 
directly connects the two landmarks. Off-road biking is prohibited by campus law, so Willie must only take the 
roads marked on the diagram above. Combining this legal requirement and with the volatile traffic patterns of the Fandom
College campus, it is certain that the distance map can only be used as a heuristic for the A\* algorithm. 
It is also noteworthy that the time it takes traveling in one direction is not necessarily the same for traveling in the
other direction. 


## Assignment Deliverable

For this assignment, you must implement the function `a_star_search(dis_map, time_map, start, end)` in `student_code.py`. 
The function must return a path from landmark `start` to landmark `end`. 

Here are a few things to consider:
* Use the _graph search_ version of the algorithm.
* Use the provided `expand` function to get the list of successors.
* The result of your `a_star_search` function must be a list of strings. Each string contains _only_ the name of a landmark. The order of the strings in the list denotes the order in which the landmarks are reached along the path.
* The result list should _begin_ with the name of the `start` landmark and _terminate_ with the name of the `end` landmark. (Thus, the path from `A` to `A` is the list `[A]`).
* The cost of a path between two connected landmarks is the total expected traffic time that must be spent travelling all landmarks in the order specified by the path.
* If two landmarks have the same value for f(n), use alphabetical ordering of the names to determine priority.  In other words, if Big Ben and Library have the same f(n) value, then Big Ben should be popped off the queue before Library.  

Furthermore, all of your code should be in `student_code.py`. Please adhere to this constraint as you develop your solution. 

Additionally, you should feel invited to use Python modules for your data structures, but you need to implement A\* yourself.

### Testing

The provided tests provide one set of heuristics and two sets of costs for the edges in the graph.  You are welcome to 
use either of these in your tests or create new ones.  There may seem like there are a large number of possible test 
cases just be considering different combinations of start and end points.  However, make sure that you are actually
testing your implementation in a way that the other tests do not.  Be sure to describe your test and make it clear how 
it is unique. 

### Questions

In `answers.txt`, provide the answers to the following questions:

1. Using `dis_map` and `time_map2`, what is the longest route (in terms of time to get from start to end) that your 
code will return?  In other words, the route from Big Cannon Hall to Hackathon Library is 60.  This is not the longest 
route that your code should be able to return.  What is?

2. The provided heuristics are consistent.  Give an example of how you could change one of the values to make it 
inconsistent.  What effect does that have on how your code works? 