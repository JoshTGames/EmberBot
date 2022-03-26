import json;

def AppendFile(fileName, dictionaryName, data):
    with open(fileName, "r+") as f:
        loadData = json.load(f);
        loadData[dictionaryName].append(data);
        f.seek(0);
        return json.dump(loadData, f, indent= 4);

def ReadFile(fileName):
    with open(fileName, 'r') as f:
        data = f.read();
        return json.loads(data);

print(ReadFile("Birthdays.json"));