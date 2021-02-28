import pandas as pd
import numpy as np
from sqlalchemy import create_engine, event


class ETL:
    def __init__(self, chunk_size_for_load):
        self.chunk_size_for_load = chunk_size_for_load
        print('ETL initialized')

    def connect_to_db(self, hostname, db_name, username, password):

        connection_str = 'mysql://{username}:{password}@{hostname}/{db_name}?charset=utf8mb4'.format(
            username=username,
            password=password,
            hostname=hostname,
            db_name=db_name
        )

        try:
            self.engine = create_engine(connection_str)

            @event.listens_for(self.engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                if executemany:
                    cursor.fast_executemany = True

            print('DB connection success')
        except:
            print('DB connection failed')

    def extract_users(self, users_path):
        self.users = pd.read_csv(
            users_path, usecols=['u', 'techniques', 'items', 'ratings'],
        )

    def extract_recipes(self, recipes_path):
        self.recipes = pd.read_csv(
            recipes_path, parse_dates=[4], index_col='id',
        )

    def extract_interactions(self, interactions_path):
        self.interactions = pd.read_csv(
            interactions_path, parse_dates=[2],
        )

    def transform_users(self, users_ids_files):
        '''Transform 'u' column into 'user_id' column, and drop na rows. '''

        users_ids = pd.DataFrame()

        for users_ids_file in users_ids_files:
            aux_df = pd.read_csv(users_ids_file, usecols=['user_id', 'u'])
            users_ids = pd.concat([users_ids, aux_df])

        users_ids.drop_duplicates(inplace=True)

        def get_user_id(u):
            try:
                return users_ids.user_id[users_ids.u == u].values[0]
            except:
                return np.nan

        self.users['id'] = self.users.u.apply(get_user_id)
        self.users.set_index('id', inplace=True)
        self.users.drop(['u'], axis=1, inplace=True)
        self.users.dropna(inplace=True)

    def transform_recipes(self):
        '''
        Remove na rows and derivable columns
        '''
        self.recipes.drop(['n_steps', 'n_ingredients'],  axis=1, inplace=True)
        self.recipes.dropna(inplace=True)

    def transform_interactions(self):
        '''
        Filter only 'interactions' with valid relationships to 'user_id'
        and 'recipe_id', and drop na rows.
        '''

        self.interactions = self.interactions[
            self.interactions.user_id.isin(self.users.index) &
            self.interactions.recipe_id.isin(self.recipes.index)]

        self.interactions.dropna(inplace=True)

    def load_users(self):
        print('Loading users')

        for start_idx in range(0, len(self.users), self.chunk_size_for_load):
            end_idx = start_idx + self.chunk_size_for_load
            df = self.users.iloc[start_idx:end_idx]

            try:
                df.to_sql(
                    'users',
                    con=self.engine,
                    if_exists='append',
                    index_label='id',
                    method='multi'
                )
                print('users loaded from: ', start_idx, 'to:', end_idx)
            except:
                print('error')

    def load_recipes(self):
        print('Loading recipes')

        for start_idx in range(0, len(self.recipes), self.chunk_size_for_load):
            end_idx = start_idx + self.chunk_size_for_load
            df = self.recipes.iloc[start_idx:end_idx]

            try:
                df.to_sql(
                    'recipes',
                    con=self.engine,
                    if_exists='append',
                    index_label='id',
                    method='multi'
                )
                print('recipes loaded from: ', start_idx, 'to:', end_idx)
            except:
                print('error')

    def load_interactions(self):
        print('Loading interactions')

        for start_idx in range(0, len(self.interactions), self.chunk_size_for_load):
            end_idx = start_idx + self.chunk_size_for_load
            df = self.interactions.iloc[start_idx:end_idx]

            try:
                df.to_sql(
                    'interactions',
                    con=self.engine,
                    if_exists='append',
                    index_label='id',
                    method='multi'
                )
                print('interactions loaded from: ', start_idx, 'to:', end_idx)
            except:
                print('error')
