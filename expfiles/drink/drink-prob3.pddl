(define (problem drink-prob1)

  (:domain drink-world)

  (:objects cup1 - cup
            person1 person2 - agent)

  (:init
  	(on-table cup1)
  	(isnt-full cup1)
  	(thirsty person1)
    (thirsty person2)
    (clear person1)
    (clear person2))

  (:goal
  	(and
  		(isnt-thirsty person1)
     	(isnt-thirsty person2)
      (on-table cup1)))) ; this is a social law
