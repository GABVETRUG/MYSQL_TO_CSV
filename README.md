# MYSQL_TO_CSV

This is a simple script with helps anyone who's interested in exporting huge tables from MySQL DB. 

Features:

- low memory usage
- tab list available (you can export a list of tables through pipeline)
- Progress bar 
- Improved export with huge datasets
- easy to maintain
- works with newest versions of MySQL


What do you need?

- a config file, in order to avoid mispelling at the input stage (preferably in the same python script's directory) 
- a tab list, separed by a ' , '
- A drink


An example:

# config file:

Name: config.txt
Content: localhost, root, yourpass, yourdb

# Tabs list

employee, orders, stock, clients
