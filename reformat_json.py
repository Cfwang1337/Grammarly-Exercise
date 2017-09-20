import csv
import json


with open("grammarly_data_exercise.json", "rb") as myfile, open("grammarly_data_csv.csv", "wb") as writefile:
    data = json.loads(myfile.read())

    header = [
        "date",
        "timestamp",
        "utmSource",
        "uid",
        "isFirst"
    ]

    writer = csv.DictWriter(writefile, fieldnames=header)
    writer.writeheader()
    entries = 0
    for item in data:
        entries += 1
        result_dict = {}
        for field in header:
            result_dict[field] = item[field]
        writer.writerow(result_dict)
    print "LENGTH:", entries