#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:44:04 2019

@author: alohahawk
"""

from panda import DataFrame
problemMatrix = [
 [1  , 70 , 173, 181, 39 , 160, 107, 140, 9  , 135],
 [124, 119, 199, 136, 76 , 98 , 133, 143, 136, 194],
 [141, 46 , 115, 185, 165, 13 , 125, 92 , 145, 143],
 [3  , 137, 85 , 44 , 53 , 183, 15 , 152, 118, 6  ],
 [56 , 103, 73 , 42 , 163, 129, 17 , 108, 70 , 68 ],
 [119, 135, 132, 144, 149, 0  , 145, 77 , 5  , 86 ],
 [19 , 99 , 52 , 109, 186, 32 , 175, 184, 71 , 40 ],
 [188, 141, 72 , 84 , 133, 119, 82 , 29 , 50 , 147],
 [63 , 134, 60 , 39 , 142, 178, 186, 156, 149, 150],
 [43 , 135, 3  , 7  , 89 , 82 , 87 , 9  , 157, 62]]

# def turn_str(l):
# 	# if list == None, return ''
# 	if not isinstance(l, list):
# 		return '{0}'.format(l)
#
# 	for index, item in enumerate(l):
# 		l[index] = turn_str(item)
# 	return l

df = DataFrame(problemMatrix)

