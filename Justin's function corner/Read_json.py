import json


# Open and read the JSON file
# with open(r'Register_Dictionary_EPM7000.JSON', 'r') as file:
#     data = json.load(file)

# # Print the data
# print(data["Registers"]["3 phase watt total"][0]["Register"])

def Read_data( targetMeter:str, Data_Value):
    #make this a match/case statement
    if targetMeter == 'PQMII':
        with open(r'utilities/Register_Dictionary_PQMII.json', 'r') as file:
            data = json.load(file)
    elif targetMeter == 'EPM7000':
        with open(r'utilities/Register_Dictionary_EPM7000.json', 'r') as file:
            data = json.load(file)

    Value_Holder = []

    x = data["Registers"][Data_Value][0]
    for i in x.values():
        Value_Holder.append(i)

    #change this to return the list of data in the json entry: address, coils, units, etc.
    print(x)
    return x

