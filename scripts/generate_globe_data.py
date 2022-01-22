import csv
import json
import glob
import os

def IsFloat(s):
    try:
        float(s)
    except:
        return False
    else:
        return True

def generate_globe_data(files, outputDir, entriesPerFile):
    data = []
    # Read all cities into data
    for filename in files:
        print("Processing %s" % filename)
        with open(filename, "r") as fp:
            reader = csv.reader(fp, delimiter=";")
            next(reader) # Skip header
            data += [(x[0], x[3], x[4], x[5]) for x in reader]

    # Sanity check
    data = filter(lambda x: IsFloat(x[1]) and IsFloat(x[2]), data)

    # Sort by population
    print("Sorting by population")
    data = sorted(data, key=lambda x: x[3], reverse=True)

    # Strip the population size
    print("Writing")
    data = [x[:3] for x in data]

    index = 0
    while True:
        print("Progress: %d/%d" % (index, (len(data)-1)/entriesPerFile+1))
        start = entriesPerFile*index
        end = min(entriesPerFile*(index+1), len(data))
        obj = {
            "data": data[start:end]
        }

        with open(os.path.join(outputDir, "%03d.json" % index), "w") as fp:
            json.dump(obj, fp)

        if end == len(data):
            break
        index += 1

if __name__ == "__main__":
    generate_globe_data(
        glob.glob("raw-data/*.csv"), 
        # glob.glob("raw-data/cities.csv"),
        "public/globe",
        10_000
    )