import json
import os


# Open and read the JSON file
# with open(r'Register_Dictionary_EPM7000.JSON', 'r') as file:
#     data = json.load(file)

# # Print the data
# print(data["Registers"]["3 phase watt total"][0]["Register"])

def Read_data( targetMeter:str, Data_Value):
    base_path = os.path.dirname(os.path.abspath(__file__))

    if targetMeter == 'PQMII':
        file_path = os.path.join(base_path, 'Register_Dictionary_PQMII.JSON')
    elif targetMeter == 'EPM7000':
        file_path = os.path.join(base_path, 'Register_Dictionary_EPM7000.JSON')
    else:
        raise ValueError(f"Unknown targetMeter: {targetMeter}")


    #make this a match/case statement
    with open(file_path, 'r') as file:
        data = json.load(file)

    Value_Holder = []

    x = data["Registers"][Data_Value][0]
    for i in x.values():
        Value_Holder.append(i)

    #change this to return the list of data in the json entry: address, coils, units, etc.
    print(x)
    return x


Read_data("EPM7000","3 phase watt total")