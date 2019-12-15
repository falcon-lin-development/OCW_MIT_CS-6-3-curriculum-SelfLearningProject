#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 13:37:51 2019

@author: Falcon Lin
"""
# Finding the right amount to save away


portion_down_payment = 0.25
current_savings = 0
r = 0.04
annual_salary = float(input("Enter annual salary: "))
salary_tem = annual_salary
total_cost = 1000000
semi_annual_raise = .07
months = 36
p_up = 1
p_down = 0
portion_saved = p_down
steps_in_bisection_search = 0
error = 100

while abs(current_savings - portion_down_payment*total_cost) > error and steps_in_bisection_search<20:
    # counting for bisection search steps
    steps_in_bisection_search += 1
    # determine upper and lower bounds
    if current_savings > portion_down_payment*total_cost:
        p_up = portion_saved
    elif current_savings < portion_down_payment*total_cost:
        p_down = portion_saved
    # determine portion saved  
    portion_saved = (p_up + p_down)/2
    # calculate savings
    current_savings = 0
    annual_salary = salary_tem
    for i in range(months):
        if i%6 == 0 and i !=0:
            annual_salary = annual_salary*(1 + semi_annual_raise)
        current_savings += annual_salary*portion_saved/12 + current_savings*r/12
        
if steps_in_bisection_search <= 20  and abs(current_savings - portion_down_payment*total_cost) < error:
    print("Best savings rate:", portion_saved)
    print("Steps in bisection search:", steps_in_bisection_search)
else:
    print("It is not possible to pay the down payment in three years.")