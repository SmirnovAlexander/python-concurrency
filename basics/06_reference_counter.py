import sys

# declare a variable
some_var = "Educative"

# check reference count
print(sys.getrefcount(some_var))

# create another refrence to someVar
another_var = some_var

# verify the incremented reference count
print(sys.getrefcount(some_var))
