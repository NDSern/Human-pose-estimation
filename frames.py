import json

dataDict = {
    "holy": 1, 
    "moly": 2, 
    "array": {}
}

llist = []

frames = 0

llist.append({
    "times": frames + 1,
    "bones" : []
})

node = {
        "name" : "Joint",
        "position": {
            "x": 1,
        }
}

llist[0]["bones"].append(node)
llist[0]["bones"].append(node)

#For normal, use update
#For array, use append
dataDict.update({"tick":3, "not_tick" : 4})
dataDict["array"].update({"time":2})
dataDict["array"].update(llist)

print(dataDict)