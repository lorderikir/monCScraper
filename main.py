import requests
import csv
import json
import os
import math

################################
# function unitInterperter()
# arg: @unit, @faculty
# unit: the unit object
# faculty: managing faculty
# author: lorderikir
################################
def unitInterperter(unit, faculty):
    address = "http://api.monplan.tech:3000/units/"

    try:
        me = unit['type']
        notJSON = True
    except TypeError:
        #not a JSON object
        notJSON = False
    print(unit, notJSON)

    if isinstance(unit, list):
        #it an array, so optional
        options = ""
        for i in range(0, len(unit)-1):
            options += unit[i] + ","
        options += unit[-1]
        output = {"UnitCode": "Choose One", "UnitName": options, "SCABand": 0, "CreditPoints": 0, "Faculty": faculty}
    elif(unit == "Elective"):
        #ouput is an elective
        output = {"UnitCode": "Free Elective", "UnitName": "Choose from any faculty", "SCABand": 0, "CreditPoints": 0, "Faculty": "Faculty of All"}
    elif(notJSON == True):
        #its an JSON object:
        output = {"UnitCode": unit['type'], "UnitName": "", "SCABand": 0, "CreditPoints": 0, "Faculty": unit['faculty']}
    else:
        #assume its a normal unit, so do an API call
        try:
            # attempt to get a response from the API
            targetURL = address + str(unit)
            r = requests.get(targetURL)
            output = r.json()
        except:
            # in the event of Response 404, Builds a Custom Unit which States Cannot Fetch Data
            output = {"UnitCode": unit, "UnitName": "Cannot Fetch Data", "SCABand": 0, "CreditPoints": 0, "Faculty": ""}

    return output

def readme(code):
    file_name = "final_output/" + code
    with open(file_name, "w") as json_file:
        print(code)
        input_file = open("output/" + code, "r")
        data = json.loads(input_file.read())
        input_file.close()

        teachingPeriods = data['teachingPeriods']
        code = data['courseCode']
        courseName = data['courseName']
        courseType = data['courseType']
        faculty = data['faculty']
        courseAOS = data['courseAOS']

        output = {"courseCode": code, "courseName": courseName, "courseAOS": courseAOS, "faculty": faculty, "courseType": courseType, "teachingPeriods": []}


        for i in range(0, len(teachingPeriods)):
            currentTeachingPeriod = teachingPeriods[i]
            units = currentTeachingPeriod["units"]
            currentYear = currentTeachingPeriod["year"]
            currenTP = currentTeachingPeriod["code"]
            numberOfUnits = len(units)
            teachingPeriodObj = {"code": currenTP, "year": currentYear, "numberOfUnits": numberOfUnits, "units": []}
            for j in range(0, numberOfUnits):
                currentUnit = unitInterperter(units[j], faculty)
                teachingPeriodObj["units"].append(currentUnit)
            output["teachingPeriods"].append(teachingPeriodObj)



        json_file.write(json.dumps(output, indent=4, sort_keys=True))

if __name__ == "__main__":
    if not os.path.exists("final_output"):
        os.makedirs("final_output")

    for filename in os.listdir("output"):
        if filename.endswith(".json"):
            readme(filename)

#readme("E3003-0")
