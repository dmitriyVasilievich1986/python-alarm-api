from ..variables.database_config import DB_CONFIG, DB_NAME, TABLE_NAME
import mysql.connector


class MYSQL_Database:
    """класс для работы с базой данных MYSQL
    """

    # region инициализация

    def __init__(self):
        """инициализация БД
        """

        self.db = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.db.cursor()
        self.init_database()
        self.create_table()

    def send_command_to_db(self, command):
        """отправка данных в базу данных,
        через обработчик исключений.

        Args:
            command (str): комманда для отправки

        Returns:
            bool: возвращает булево значение об успехе отправки данных.
        """

        try:
            self.cursor.execute(command)
            return True
        except mysql.connector.Error as err:
            print(err)
        return False

    def init_database(self):
        """инициализируем базу данных
        """

        self.send_command_to_db(
            f'CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET "utf8";'
        )
        self.send_command_to_db(f"USE {DB_NAME}")

    def create_table(self):
        """создаем таблицу сигналов будильника
        """

        self.send_command_to_db(
            f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description VARCHAR(255), time DATETIME NOT NULL);"
        )

    # endregion

    def get_all_alarms(self):
        """отправляет запрос в БД для получения всех будильников

        Returns:
            list: список будильников.
        """

        if self.send_command_to_db(
            f"SELECT id, name, description, time FROM {TABLE_NAME}"
        ):
            return [
                {
                    "id": x[0],
                    "name": x[1],
                    "description": x[2],
                    "time": x[3].strftime("%Y-%m-%d %H:%M"),
                }
                for x in self.cursor.fetchall()
            ]
        return []

    def insert_new_alarm(self, name, time_stamp, description=""):
        """ввод в БД нового будильника

        Args:
            name (str): название будильника
            time_stamp (str): время срабатывания
            description (str, optional): описание будильника.
        """

        if self.send_command_to_db(
            f"insert into {TABLE_NAME} (name, description, time) values ('{name}', '{description}', '{time_stamp}');"
        ):
            self.db.commit()

    def delete_alarm(self, id):
        """удаляем будильник

        Args:
            id (bool): возвращает булево значение о выполнении запроса.
        """
        if self.send_command_to_db(f"DELETE FROM {TABLE_NAME} WHERE id={id}"):
            self.db.commit()


mysql_database = MYSQL_Database()
