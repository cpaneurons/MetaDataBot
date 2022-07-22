import sqlite3


class VisuallyDB:
    """БД предназначенная по визуальной части"""
    # message_id - удаление сообщения "ожидания", когда пользователь прервал операцию или же отправил файл
    def __init__(self):
        try:
            self.base = sqlite3.connect('user_info.db')
            self.cur = self.base.cursor()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS memorization_message(
                    message_id INT,
                    user_id INT
            )""")
            self.base.commit()
        except Exception:
            pass

    def exists_message(self, user_id: int) -> bool:
        self.cur.execute('SELECT message_id FROM memorization_message WHERE user_id = ?', (user_id,))
        return len(self.cur.fetchmany(1)).__bool__()

    def get_message_id(self, user_id: int):
        self.cur.execute('SELECT message_id FROM memorization_message WHERE user_id = ?', (user_id, ))
        return self.cur.fetchmany(1)[0][0]

    def add_message_id(self, user_id: int, message_id: int):
        self.cur.execute('INSERT INTO memorization_message(user_id, message_id) VALUES(?, ?)', (user_id, message_id))
        self.base.commit()

    def delete_all_by_user_id(self, user_id: int):
        self.cur.execute('DELETE FROM memorization_message WHERE user_id = ?', (user_id, ))
        self.base.commit()

    def __del__(self):
        self.cur.close()
        self.base.close()



class FileDb:
    def __init__(self):
        try:
            self.base = sqlite3.connect('user_info.db')
            self.cur = self.base.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS file_db(
                    user_id INT,
                    file_path TEXT,
                    new_file_path TEXT,
                    width_file INT,
                    height_file INT
            )""")
            self.base.commit()
        except Exception:
            pass

    def add_data(self, user_id: int, file_path: str, new_file_path: str, width_file: int, height_file: int):
        self.cur.execute('INSERT INTO file_db(user_id, file_path, new_file_path, width_file, height_file)'
                         'VALUES(?, ?, ?, ?, ?)', (user_id, file_path, new_file_path, width_file, height_file))
        self.base.commit()

    def file_exists(self, user_id):
        self.cur.execute('SELECT user_id FROM file_db WHERE user_id = ?', (user_id, ))
        return len(self.cur.fetchmany(1)).__bool__()

    def delete_all_by_user_id(self, user_id):
        self.cur.execute('DELETE FROM file_db WHERE user_id = ?', (user_id, ))
        self.base.commit()

    def delete_all(self):
        self.cur.execute('DELETE FROM file_db')
        self.base.commit()

    def get_all(self):
        self.cur.execute('SELECT * FROM file_db')
        return self.cur.fetchmany(-1)

    def __del__(self):
        self.cur.close()
        self.base.close()


class UserInfoDB:
    def __init__(self):
        try:
            self.base = sqlite3.connect('user_info.db')
            self.cur = self.base.cursor()

            self.cur.execute("""CREATE TABLE IF NOT EXISTS user(
                    user_id INT,
                    user_name TEXT
            )""")
            self.base.commit()
        except Exception:
            pass

    def exists_user(self, user_id: int) -> bool:
        self.cur.execute('SELECT user_id FROM user WHERE user_id = ?', (user_id,))
        return len(self.cur.fetchmany(1)).__bool__()

    def user_add(self, user_id: int, user_name: int):
        self.cur.execute('INSERT INTO user(user_id, user_name) VALUES(?, ?)', (user_id, user_name))
        self.base.commit()

    def get_number_of_users(self) -> int:
        self.cur.execute('SELECT user_id FROM user')
        users_type = self.cur.fetchall()

        number_of_users = len(users_type)
        return number_of_users

    def __del__(self):
        self.cur.close()
        self.base.close()
