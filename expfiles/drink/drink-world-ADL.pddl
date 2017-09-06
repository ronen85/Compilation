(define (domain drink-world)

	(:requirements
    	:typing :negative-preconditions)

	(:types cup agent)

 	(:constants )


	(:predicates
	      (thirsty ?a - agent)
	      ;(isnt-thirsty ?a - agent)
	      (hold-cup ?a - agent ?c - cup)
	      ;(isnt-hold-cup ?a - agent ?c - cup)
	      (clear ?a - agent)
	      ;(isnt-clear ?a - agent)
	      (on-table ?c - cup)
	      ;(isnt-on-table ?c - cup)
	      (full ?c - cup)
	      ;(isnt-full ?c - cup)
        )

		(:functions
				(amount1 ?c - cup))

  	(:durative-action take-cup
  		;;pref start = {clear ?a}
  		;;prew start = {on-table ?c}
  		;;add start = {}
  		;;del start = {clear ?a, on-table ?c, isnt-hold-cup ?a ?c}
  		;;inv = {}
  		;;pref end = {}
  		;;add end = {isnt-clear ?a, isnt-on-table ?c, hold-cup ?a ?c}
  		;;del end = {}
  		:parameters (?a - agent ?c - cup)
  		:duration (= ?duration 1)
  		:condition
  			(and
  				(at start (clear ?a)) ;;pref start
  				(at start (on-table ?c))) ;;prew
  		:effect
  			(and
  				(at start (not (clear ?a)))
          ;(at end (isnt-clear ?a))
  				(at start (not (on-table ?c)))
  				;(at end (isnt-on-table ?c))
  				(at end (hold-cup ?a ?c))
  				;(at start (not (isnt-hold-cup ?a ?c)))
          ))

  	(:durative-action return-cup
  		;;pref start = {hold-cup ?a ?c, isnt-full}
  		;;prew start = {}
  		;;add start = {}
  		;;del start = {hold-cup ?a ?c}
  		;;inv = {}
  		;;pref end = {}
  		;;add end = {isnt-hold-cup ?a ?c, on-table ?c, clear ?a}
  		;;del end = {isnt-on-table ?c, isnt-clear ?a}
  		:parameters (?a - agent ?c - cup)
  		:duration (= ?duration 1)
  		:condition
  			(and
  				(at start (hold-cup ?a ?c))
					(at start (not (full ?c))))
  		:effect
  			(and
  				(at start (not (hold-cup ?a ?c)))
  				;(at end (isnt-hold-cup ?a ?c))
  				(at end (on-table ?c))
  				;(at end (not (isnt-on-table ?c)))
  				(at end (clear ?a))
  				;(at end (not (isnt-clear ?a)))
          ))

  	(:durative-action drink-cup
  		;;pref start = {hold-cup ?a ?c, full ?c, thirsty ?a}
  		;;prew start = {}
  		;;add start = {}
  		;;del start = {full ?c, thirsty ?a}
  		;;inv = {hold-cup ?a ?c}
  		;;pref end = {hold-cup ?a ?c}
  		;;add end = {isnt-full ?c, isnt-thirsty ?a}
  		;;del end = {}
  		:parameters (?a - agent ?c - cup)
  		:duration (= ?duration 1)
  		:condition
  			(and
  				(at start (hold-cup ?a ?c))
  				(over all (hold-cup ?a ?c))
  				(at end (hold-cup ?a ?c))
  				(at start (full ?c))
  				(at start (thirsty ?a)))
  		:effect
  			(and
  				(at start (not (full ?c)))
  				;(at end (isnt-full ?c))
  				(at end (not (thirsty ?a)))
  				;(at end (isnt-thirsty ?a))
          ))

    (:action adl_test
      :parameters (?a - agent ?c - cup)
      :precondition
        (and
          (not (hold-cup ?a ?c))
          (thirsty ?a))
      :effect
        (and
          (full ?c)
          (thirsty ?a)
          (not (on-table ?c))
          ))

  	(:durative-action fill-cup
  		;;pref start = {hold-cup ?a ?c, isnt-full ?c}
  		;;prew start = {}
  		;;add start = {}
  		;;del start = {isnt-full ?c}
  		;;inv = {hold-cup ?a ?c}
  		;;pref end = {hold-cup ?a ?c}
  		;;add end = {full ?c}
  		;;del end = {}
  		:parameters (?a - agent ?c - cup)
  		:duration (= ?duration 1)
  		:condition
  			(and
  				(at start (hold-cup ?a ?c))
  				(over all (hold-cup ?a ?c))
  				(at end (hold-cup ?a ?c))
          (at start (not (full ?c))))
  				;(at start (isnt-full ?c)))
  		:effect
  			(and
  				;(at start (not (isnt-full ?c)))
  				(at end (full ?c)))
        ))
