#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:59:24 2019

@author: Falcon Lin
"""
# Saving, with a raise


portion_down_payment = 0.25
current_savings = 0
r = 0.04
annual_salary = float(input("Enter annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))
months = 0
while current_savings < total_cost*portion_down_payment:
    if months%6 == 0 and months !=0:
        annual_salary = annual_salary*(1 + semi_annual_raise)
    current_savings += annual_salary*portion_saved/12 + current_savings*r/12
    months += 1
    
    
print("Number of months", months)