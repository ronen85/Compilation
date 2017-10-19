(define (problem DLOG-5-5-10)
	(:domain driverlog)
	(:objects
	driver1 - driver
	driver2 - driver
	truck1 - truck
	truck2 - truck
	package1 - obj
	package2 - obj
	package3 - obj
	s1 - location
	s2 - location
	s3 - location
	s4 - location
	p1-2 - location
	p2-3 - location
	p1-3 - location
	p1-4 - location
	)
	(:init
	(at driver1 s1)
	(at driver2 s4)
	(at truck1 s2)
	(empty truck1)
	(at truck2 s3)
	(empty truck2)
	(at package1 s3)
	(at package2 s4)
	(at package3 s4)
	(path s1 p1-2)
	(path p1-2 s1)
	(path s2 p1-2)
	(path p1-2 s2)
	(path s2 p2-3)
	(path p2-3 s2)
	(path s3 p2-3)
	(path p2-3 s3)
	(path s1 p1-3)
	(path p1-3 s1)
	(path s3 p1-3)
	(path p1-3 s3)
	(path s1 p1-4)
	(path p1-4 s1)
	(path s4 p1-4)
	(path p1-4 s4)
	(link s1 s2)
	(link s2 s1)
	(link s2 s3)
	(link s3 s2)
	(link s3 s4)
	(link s4 s3)
)
	(:goal (and
	(at driver2 s1)
	(at truck2 s1)
	))

)
