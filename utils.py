import json
import csv

def clean_relations():
    relations_by_ids = []
    with open('harry_potter/relations.csv', newline='') as f:
        reader = csv.reader(f)
        relations_by_ids = list(reader)
    with open('harry_potter/clean_characters.json') as json_file:
        data = json.load(json_file)
        character_by_ids = {}
        for character in data:
            character_by_ids[character['id']] = character
        relations = []
        for relation in relations_by_ids:
            if relation[0] in character_by_ids and relation[1] in character_by_ids:
                relations.append((character_by_ids[relation[0]]['Name'], character_by_ids[relation[1]]['Name'], relation[2]))
        with open('harry_potter/cleanRelations.csv','w') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['name1','name2', 'relation'])
            for row in relations:
                csv_out.writerow(row)

def clean_characters_data():
    # Get ids
    characters_by_name = {}
    with open('harry_potter/characters.csv', newline='') as f:
        reader = csv.reader(f)
        id_name = list(reader)
        for character in id_name[1:]:
            characters_by_name[character[1].lower()] = character
    with open('harry_potter/characters.json') as json_file:
        data = json.load(json_file)
        for character in data:
            # Add id
            if character['Name'].lower() in characters_by_name:
                character['id'] = characters_by_name[character['Name'].lower()][0]

            # Remove uneeded keys
            character.pop('Link', None)
            character.pop('Descr', None)

            # Split for some extra data
            if character['School'] != 'Unknown' and 'Hogwarts' in character['School']:
                splitted_school = character['School'].split(' - ')
                if len(splitted_school) == 2:
                    character['School'], character['house'] = splitted_school
                else:
                    character['School'], character['house'] = splitted_school[0], 'Unknown'
        # Take only characters with id
        data = [character for character in data if "id" in character]
        # remove duplications
        data = [i for n, i in enumerate(data) if i not in data[n + 1:]]
        with open('harry_potter/clean_characters.json', 'w') as data_file:
            data = json.dump(data, data_file)
clean_relations()