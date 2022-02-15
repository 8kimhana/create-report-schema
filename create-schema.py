#!/usr/local/bin/python3
import sys
import pandas as pd
import numpy as np
import json
import easygui

def main():
    decideFileExtension(easygui.fileopenbox(msg= 'Select the file (either .csv with id, name, and description headers or .txt with just ids)'))
    return None

def decideFileExtension(input):
    if(input.lower().endswith('.txt')):
        formatInputTxt(input)
    elif(input.lower().endswith('.csv')):
        formatInputCsv(input)
    else:
        raise BaseException('This filetype is not supported')

def formatInputTxt(input):
    data = np.genfromtxt(input, dtype=('str'), delimiter=",")
    df = pd.DataFrame(data=data)
    df = df.rename(columns = {0:"id"})
    setUpObj = setUp()
    df["name"] = df["id"]
    df["description"] = ""
    df["type"] = "string"
    for index, row in df.iterrows():
        if("date" in row["name"].lower()):
            row["type"] = "Date"
    for prop in setUpObj['extraProperties']:
        df[prop['propertyName']] = prop['propertyValue']
    userInputTypesForRows(df)
    compileAndPrintJSON(setUpObj, df)

def formatInputCsv(input):
    df = pd.read_csv(input)
    df["type"] = "string"
    for index, row in df.iterrows():
        if("date" in row["name"].lower()):
            row["type"] = "Date"
    setUpObj = setUp()
    for prop in setUpObj['extraProperties']:
        df[prop['propertyName']] = prop['propertyValue']
    userInputTypesForRows(df)
    compileAndPrintJSON(setUpObj, df)

def setUp():
    type = checkIfDimensionsOrMetrics()
    jsonObj = createJSONStart(type)
    extraProperties = getExtraProperties()
    d = dict()
    d["type"] = type
    d["jsonObj"] = jsonObj
    d["extraProperties"] = extraProperties
    return d

def compileAndPrintJSON(setUpObj, df):
    jsonResult = df.to_json(orient="records")
    jsonParsed = json.loads(jsonResult)
    setUpObj['jsonObj'][setUpObj['type']]=(jsonParsed)
    jsonOutput = easygui.msgbox(msg=(json.dumps(setUpObj['jsonObj'], indent=4)),title='',ok_button='Close')
    print(jsonOutput)

def userInputTypesForRows(df):
    output = easygui.ynbox(msg= 'Would you like to assign types to each of the rows yourself? If not all types will be of type string except dates which will have the Date type')
    if(output):
        for index, row in df.iterrows():
            message = "What type would you like {} to be".format(row["name"])
            type = easygui.enterbox(message,title='', default='')
            row["type"] = type
    return

def getExtraProperties():
    properties = []
    checkForExtraProperties(properties)
    return properties

def checkForExtraProperties(properties):
    output = easygui.ynbox(msg= 'Would you like to add another property to these objects')
    if(output):
        propertyName = easygui.enterbox(msg='Please type the name of the property',title='', default='data-')
        propertyValue = easygui.enterbox(msg='If you would like them to have a standard value enter that here, if you want them empty leave it blank',title='', default='')
        if(bool(propertyValue)):
            if("true" in propertyValue.lower()):
                propertyValue = True
            elif ("false" in propertyValue.lower()):
                propertyValue = False
        properties.append({
            "propertyName":propertyName,
            "propertyValue":propertyValue
        })
        checkForExtraProperties(properties)
    else:
        return

def checkIfDimensionsOrMetrics():
    output = easygui.indexbox(msg= 'Please select whether these are dimensions or metrics', title='', choices=['dimensions','metrics'])
    if(output == 0):
        return "dimensions"
    if(output == 1):
        return "metrics"
    else:
        return

def createJSONStart(type):
    startJson = {}
    startJson[type] = []
    return startJson





if __name__ == "__main__":
   main()