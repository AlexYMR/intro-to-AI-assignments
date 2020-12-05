(define (problem test2)
  (:domain sokorobotto)
  (:objects
    shipment1 - shipment
    order1 - order
    loc1 loc2 loc3 pack1 - location
    robot1 robot2 - robot
    pallette1 pallette2 - pallette
    socks1 book1 book2 - saleitem
    )
  (:init
    (ships shipment1 order1)
    (orders order1 book1)
    (unstarted shipment1)
    (packing-location pack1)
    (available pack1)
    (contains pallette1 book1)
    (contains pallette2 book2)
    (free robot1)
    (connected loc1 loc2)
    (connected loc2 loc1)
    (connected loc2 pack1)
    (connected pack1 loc2)
    (connected loc3 loc1)
    (at pallette1 loc3)
    (at pallette2 loc1)
    (at robot1 loc2)
    (no-robot loc1)
    (no-robot pack1)
    (no-robot loc3)
    (no-pallette pack1)
    (no-pallette loc2)
    )
  (:goal (includes shipment1 book1))
)
