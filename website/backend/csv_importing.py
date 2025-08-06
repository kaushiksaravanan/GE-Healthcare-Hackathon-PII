import csv
def load_dict_memory(csv_file_path):
    data_dict = {}
    # Read the CSV file
    with open(csv_file_path, mode='r',encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        # Iterate through each row in the CSV
        for row in csv_reader:
            # print(row)
            entity_name = row['ENTITY_NAME'].lower()  # Convert to lowercase
            entity_type = row['ENTITY_TYPE']
            data_dict[entity_name] = '['+entity_type+']'
    return data_dict

data_dict=load_dict_memory('./assets/location.csv')
file_path = './assets/location'
import klepto

# Create a klepto file archive
archive = klepto.archives.file_archive(file_path, cached=False, serialized=True)

# Add data to the archive
archive['data'] = data_dict

# Dump the archive to the file
archive.dump()