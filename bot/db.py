import psycopg2

import config


class DataBaseManager:
    def __init__(self, database=config.DB_NAME, user=config.DB_USER,
                 password=config.DB_PASSWORD, host=config.DB_HOST):
        self.connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def add_user(self, id_user, first_name, nick_name):
        self.cursor.execute(
            f'''INSERT INTO users (id_user, first_name, nickname) VALUES
            ({id_user}, '{first_name}', '{nick_name}');'''
        )

    def get_user(self, id_user):
        self.cursor.execute(
            f'''SELECT id_user, first_name, nickname FROM users WHERE 
            id_user = {id_user};'''
        )
        return str(self.cursor.fetchone())
