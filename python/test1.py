#!/bin/env python
def test1():
	a=[1,7,3,2,9,6,8]
	for i in range(0,len(a)):
		a1=a[:]
		del a1[i]
		for j in range(0,len(a1)):
			a2=a1[:]
			del a2[j]
			for k in range(0,len(a2)):
				print a[i],a1[j],a2[k]
test1()

