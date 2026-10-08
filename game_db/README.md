this project is to build out a db that can be accessed through python that holds information for the wake game. all specific data related to players, environment and turns is be held in the db. this is a learning environment to understand SQL querries and db design methodologies. 

DB TABLES:

player table
player id | name | score
p001      | tim  | 1000

character table
character id | name  | player id | str | dex | con | int | wis | wake | max_wake
c001         | rambo | p001      | 3   | 3   | 5   | 5   | 9   | 70   | 100  

item table
item id | name    | type       | weight | value
it001   | coffee  | single_use | 5      | 10
it002   | stapler | multi_use  | 10     | 50

inventory table
inventory id | character id | item id
in001        | c001         | it001
in002        | c001         | it001

