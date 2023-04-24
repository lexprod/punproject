# Pun Project 
The Pun project is a dockerized cloud based pun database platform, which will eventually allow for creating, deleting, tagging, and rating of puns. 

Models:
using ORM I'm going to have at least the following objects:
Users
Puns
Categories

Users and Puns have a many to one relationship
-only one user is an author of a pun
Puns and Categories have a many to many relationship
A bridge table would track User's ratings of puns
There should be functionality to pull up all puns with specific categories
