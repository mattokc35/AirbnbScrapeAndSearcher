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
    location = params[0].strip()
    checkin = params[1].strip()
    checkout = params[2].strip()
    adults = params[3].strip()
    children = params[4].strip()
    infants = params[5].strip()
    pets = params[6].strip()
    my_listing = params[7].strip() #strip gets rid of newline character
    test = subprocess.run(["python3", "search.py", "--location="+location, "--checkin=" + checkin, "--checkout=" + checkout, "--adults=" + adults, "--children=" + children, "--infants=" + infants, "--pets=" + pets, "--my_listing=" + my_listing], capture_output=True, text=True)
    print(test.stdout)
    i+=1

myFile.close()
