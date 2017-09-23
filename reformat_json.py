import csv
import json


def clean_sources(x):
    if x is None:
        return "other"
    else:
        return x.split('.')[0].lower()


def main():
    with open("grammarly_data_exercise.json", "rb") as myfile, open("grammarly_data_csv.csv", "wb") as writefile:
        data = json.loads(myfile.read())

        header = [
            "date",
            "timestamp",
            "utmSource",
            "utmSource_cleaned",
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
                if field != "utmSource_cleaned":
                    result_dict[field] = item[field]

                    if field == "utmSource":
                        result_dict["utmSource_cleaned"] = clean_sources(item[field])

            writer.writerow(result_dict)
        print "LENGTH:", entries


if __name__ == "__main__":
    main()