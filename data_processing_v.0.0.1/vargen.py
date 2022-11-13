# created by @oscars47 and @ghirsch123 summer 2022, updated fall 2022
# creates a class called Variable that computes each of the 23 indices for each lightcurve object passed through
# if max(mag_err) exceeds 5, then return null for each value and include "bad" flag; remove all obejcts that have bad flag in final df