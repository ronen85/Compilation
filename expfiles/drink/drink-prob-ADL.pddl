(define (problem drink-prob1)

  (:domain drink-world)

  (:objects cup1 - cup
            person1 person2 - agent)

  (:init
  	(on-table cup1)
  	;(isnt-full cup1)
  	(thirsty person1)
    (thirsty person2)
    (clear person1)
    (clear person2))

  (:goal
  	(and
  		(not(thirsty person1))
     	(not(thirsty person2)))))
