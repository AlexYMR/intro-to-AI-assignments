(define (domain sokorobotto)
  (:requirements :typing)
  (:types  
    shipment
    order
    location
    robot
    pallette
    saleitem
    robot pallette - object
  )
  (:predicates 
    (includes ?s - shipment ?i - saleitem)
    (ships ?s - shipment ?o - order)
    (orders ?o - order ?i - saleitem)
    (unstarted ?s - shipment)
    (started ?s - shipment ?l - location)
    (packing-location ?l - location)
    (available ?l - location)
    (contains ?p - pallette ?i - saleitem)
    (free ?r - robot)
    (connected ?x ?y - location)
    (at ?obj - object ?l - location)
    (no-robot ?l - location) 
    (no-pallette ?l - location)  
    (carrying-pallette ?r - robot ?p - pallette)
  )

  ; moveWithPallet: robot moves w/ pallet (carries it along its location as well)
  (:action moveWithPallet
      :parameters (?r - robot ?p - pallette ?from ?to - location)
      :precondition (and
        (at ?r ?from)
        (connected ?from ?to)
        (no-robot ?to)
        (no-pallette ?to)
        ; (at ?p - pallette ?from - location) (lift does this)
        (carrying-pallette ?r ?p)
      )
      :effect (and 
        (not(no-robot ?to)) ; needed?
        (not(at ?r ?from))
        (at ?r ?to)
        (no-robot ?from)
      )
  )

  ; move: robot moves (w/o) pallet
  (:action move
      :parameters (?r - robot ?from ?to - location)
      :precondition (and
        (free ?r) ;forces use of moveWithPallet otherwise
        (at ?r ?from)
        (connected ?from ?to)
        (no-robot ?to)
      )
      :effect (and 
        (not(no-robot ?to)) ; needed?
        (not(at ?r ?from))
        (at ?r ?to)
        (no-robot ?from)
      )
  )
  
  ; lift: when under pallet, robot lifts it
  (:action lift
      :parameters (?r - robot ?p - pallette ?x - location)
      :precondition (and
        (at ?r ?x)
        (at ?p ?x)
      )
      :effect (and
        (not (at ?p ?x)) ;clean up here to avoid messiness when dropping pallet
        (not(free ?r))
        (no-pallette ?x) ;clean up here
        (carrying-pallette ?r ?p) ; needed?
      )
  )
  
  ; drop: robot drops pallet
  (:action drop
      :parameters (?r - robot ?p - pallette ?x - location)
      :precondition (and
        (at ?r ?x)
        (carrying-pallette ?r ?p)
      )
      :effect (and 
        (not(carrying-pallette ?r ?p))
        (not(no-pallette ?x)) ; needed?
        (free ?r)
        (at ?p ?x)
      )
  )

  ; start_shipment: makes packing location unavailable | marks shipment as started
  (:action start_shipment
      :parameters (?p - pallette ?x - location ?i - saleitem ?s - shipment ?o - order)
      :precondition (and
        (unstarted ?s)
        (packing-location ?x)
        (available ?x)
        (at ?p ?x)
        (orders ?o ?i) ; make sure order calls for saleitem
        (ships ?s ?o) ; make sure shipment is tied to this order
        (contains ?p ?i)
      )
      :effect (and 
        (not(available ?x))
        (started ?s ?x)
      )
  )

  ; pause_shipment: makes packing locations available again so that they can be used for other shipments
  (:action pause_shipment
      :parameters (?p - pallette ?x - location ?i - saleitem ?s - shipment ?o - order)
      :precondition (and
        (started ?s ?x)
        (packing-location ?x)
        (at ?p ?x)
      )
      :effect (and 
        (available ?x)
        (not(started ?s ?x))
        (unstarted ?s)
      )
  )

  ; deposit: put saleitems into shipment
  (:action deposit
      :parameters (?p - pallette ?x - location ?i - saleitem ?s - shipment ?o - order)
      :precondition (and
        (at ?p ?x)
        (contains ?p ?i)
        ;the saleitem is tied to the order
        ;the order is tied to the shipment
        ;and the shipment is tied to the packing station (implicitly via started predicate)
        (orders ?o ?i)
        (ships ?s ?o)
        (started ?s ?x)
      )
      :effect (and
        (not(contains ?p ?i))
        (includes ?s ?i)
      )
  )

  ; NEEDED ACTIONS:
  ; none

  ; CONSIDER:
  ; [X] you must check somewhere whether a pallet has a saleitem (contains)
  ; [X] robots cannot teleport, and they cannot pass through other robots (check for this in move action)
  ; [X] how do you make sure it chooses moveWithPallet instead of move? >> made (free ?r) a prerequisite of move
  ; [X] change "unstarted" to "started" (another predicate)
  ; [X] remove "available" when shipment is being packed at packing location
  ; [X] can you have negative statements in the preconditions? (yes, but better habit to maybe not)s

)
