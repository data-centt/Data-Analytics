import pandas as pd
import json
import os


def process_file(path):
    if path.endswith(".csv"):
        data = pd.read_csv(path)
    elif path.endswith(("xlsx", "xls")):
        data = pd.read_excel(path)
    else:
        raise ValueError("File not compatible, please reassess or upload a new file")

    json_data = data.to_dict(orient="records")
    return json_data


def save_json(json_data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def main():
    file_path = input("Enter file name: ")
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist")
        return

    json_data = process_file(file_path)
    output_path = input("Name of json file: ") + ".json"
    save_json(json_data, output_path)
    print("File has been saved successfully")


if __name__ == "__main__":
    main()
