import json

# Open and read the JSON file
# with open(r'Register_Dictionary_EPM7000.JSON', 'r') as file:
#     data = json.load(file)

# # Print the data
# print(data["Registers"]["3 phase watt total"][0]["Register"])

def Read_data(Meter_Type,Data_Value):
    if Meter_Type == "PQMII":
        with open(r'Register_Dictionary_PQMII.JSON', 'r') as file:
            data = json.load(file)
    elif Meter_Type == "EPM7000":
        with open(r'Register_Dictionary_EPM7000.JSON', 'r') as file:
            data = json.load(file)

    Value_Holder = []

    x = data["Registers"][Data_Value][0]
    for i in x:
        Value_Holder.append(i)
    print(Value_Holder)
    register = "placeholder"
    return register

Read_data("EPM7000","3 phase watt total")