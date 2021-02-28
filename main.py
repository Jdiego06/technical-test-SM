from etl import ETL
import json


users_path = './data/PP_users.csv'
recipes_path = './data/RAW_recipes.csv'
interactions_path = './data/RAW_interactions.csv'

users_ids_paths = [
    './data/interactions_train.csv',
    './data/interactions_test.csv',
    './data/interactions_validation.csv'
]

with open('config.json') as config_json:
    config = json.load(config_json)


etl = ETL()
etl.connect_to_db(config['hostname'], config['db_name'],
                  config['username'], config['password'])


print('Extracting data...')
etl.extract_users(users_path)
etl.extract_recipes(recipes_path)
etl.extract_interactions(interactions_path)

print('Transforming data...')
etl.transform_users(users_ids_paths)
etl.transform_recipes()
etl.transform_interactions()

print('Loading data...')
etl.load_users()
etl.load_recipes()
etl.load_interactions()
