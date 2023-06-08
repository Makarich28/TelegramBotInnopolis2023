import os
if not os.path.exists("Привет"):
     os.makedirs("Hi")

with open('cat1.jpg', 'w') as file:
    file.write("hello_world")
