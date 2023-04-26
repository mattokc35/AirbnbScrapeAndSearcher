"""
This Program will go through InputParameters.csv line by line and execute a search for the parameters in each line
"""


import subprocess
myFile = open('InputParameters.csv')
text_list = myFile.readlines()[1:]
print("CONDUCTING " + str(len(text_list))+ " SEARCHES")
i = 1
for line in text_list:
    print("\n NEXT SEARCH (Search #" + str(i) + ")\n")
    params = line.split(',')
    location = params[0]
    print(location)
    checkin = params[1]
    checkout = params[2]
    adults = params[3]
    children = params[4]
    infants = params[5]
    pets = params[6]
    my_listing = params[7].strip() #strip gets rid of newline character
    test = subprocess.run(["python3", "search.py", "--location="+location, "--checkin=" + checkin, "--checkout=" + checkout, "--adults=" + adults, "--children=" + children, "--infants=" + infants, "--pets=" + pets, "--my_listing=" + my_listing], capture_output=True, text=True)
    print(test.stdout)
    i+=1

myFile.close()
