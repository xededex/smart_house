# from config_data.config import DatabaseConfig
from dataclasses import dataclass
from peewee import *

import os
from config_data.config import Config, load_config
config: Config = load_config()


conn = SqliteDatabase(config.db.database)




class BaseModel(Model):
    class Meta:
        database = conn  # соединение с базой, из шаблона выше

# Определяем модель исполнителя
class AuthorizedUsers(BaseModel):
    id        = AutoField(column_name='id')
    user_id   = IntegerField(column_name='user_id')
    user_name = TextField(column_name="user_name", null=True)
    
    class Meta:
        table_name = 'AuthorizedUsers'


class ApplicationsRegistration(BaseModel):
    id        = AutoField(column_name='id')
    user_id   = IntegerField(column_name='user_id')
    user_name = TextField(column_name="user_name", null=True)
    
    class Meta:
        table_name = 'ApplicationsRegistration'


@dataclass
class DB_API:
    # database: str
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    db_path: str  = os.path.join(BASE_DIR, "test.db")

    conn = SqliteDatabase(db_path, pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64})

    with conn:
        conn.create_tables([AuthorizedUsers, ApplicationsRegistration])

    
    
    
    def already_have_appl(self, user_id) -> int | None:
        try:
            appl = ApplicationsRegistration.get(ApplicationsRegistration.user_id == user_id)
        except Exception as e:
            return None
        else:
            return appl.id
    
    
    
    def create_app_registration(self, user_name, user_id) -> None:
        if self.already_have_appl(user_id) == None:
            appl = ApplicationsRegistration.create(user_name = user_name, user_id = user_id)
            print(appl.id)
            return appl.id
        else:
            return self.already_have_appl(user_id)
    
    def show_all_app_registration(self) -> list[ApplicationsRegistration]:
    
        cur_query = ApplicationsRegistration.select()
        return list(cur_query.dicts().execute())
    
    
    
    def add_user(self, app_registration_id : str) -> ApplicationsRegistration | None:
        try:
            app_reg = ApplicationsRegistration.get(ApplicationsRegistration.id == app_registration_id)
            ApplicationsRegistration.delete_by_id(app_reg.id)
        
            print(app_reg.user_id)
            print(app_reg.user_name)
            if not self.is_registered(app_reg.user_id):
                AuthorizedUsers.create(user_name = app_reg.user_name, user_id = app_reg.user_id)
            
        except Exception as e:
            return None
        else:
            return app_reg
    
    
    
    
    def del_user(self, id : str) -> ApplicationsRegistration | None:
        try:
            app_reg = AuthorizedUsers.get(AuthorizedUsers.id == id)
            print(app_reg)
            AuthorizedUsers.delete_by_id(app_reg.id)
        except Exception as e:
            return None
        else:
            return app_reg.user_id
        
            # print(app_reg.user_id)
            # print(app_reg.user_name)
            # if not self.is_registered(app_reg.user_id):
            #     AuthorizedUsers.create(user_name = app_reg.user_name, user_id = app_reg.user_id)
            

    
    
    
    
    
    def show_all_users(self) -> list[AuthorizedUsers]:
        
        cur_query = AuthorizedUsers.select()
        lst = list(cur_query.dicts().execute())
        if len(lst) == 0:
            return None
        else:
            return lst
             
    
    
    
    def is_registered(self, id: int) -> bool:
        try:
            user = AuthorizedUsers.get(AuthorizedUsers.user_id == id)
        except Exception as e:
            return False
        else:
            return True
        
        
        # query = AuthorizedUsers.select().where(AuthorizedUsers.user_id == id)
        # users = query.dicts().execute()
        print(user.user_id)
        return user     
    
# if __name__ == '__main__':
    

#     db = DB_API("")
#     id_apply = db.create_app_registration("ff99x", 1021596615)
#     db.add_user(id_apply)
    # res = db.is_registered(32)
    
    # print(db.show_all_users())
    # print(res)
    # db.add_user("u")
    # db.show_all_users()
    # print("ewqwq")