# storage.py
from abc import ABC, abstractmethod
import sqlite3

from fastapi import HTTPException, status

from schemas import NewTrip, SavedTrip


class BaseStorageTrip(ABC):
    @abstractmethod
    def create_trip(self, new_trip: NewTrip):
        pass

    @abstractmethod
    def get_trip(self, _id: int):
        pass

    @abstractmethod
    def get_trips(self, limit: int = 10):
        pass

    @abstractmethod
    def update_trip_price(self, _id: int, new_price: float):
        pass

    @abstractmethod
    def delete_trip(self, _id: int):
        pass


class StorageSQLite(BaseStorageTrip):

    def _create_table(self):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                CREATE TABLE IF NOT EXISTS {self.trip_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    destination TEXT,
                    price REAL,
                    image TEXT,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            cursor.execute(query)

    def __init__(self, database_name: str):
        self.database_name = database_name
        self.trip_table_name = 'trips'
        self._create_table()

    def create_trip(self, new_trip: NewTrip) -> SavedTrip:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            values = (new_trip.title, new_trip.destination, new_trip.price, new_trip.image, new_trip.description)
            query = f"""
                INSERT INTO {self.trip_table_name} (title, destination, price, image, description)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, values)
        return self._get_latest_trip()

    def _get_latest_trip(self) -> SavedTrip:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, destination, price, image, description, created_at
                FROM {self.trip_table_name}
                ORDER BY id DESC
                LIMIT 1
            """
            result: tuple = cursor.execute(query).fetchone()
            id, title, destination, price, image, description, created_at = result
            return SavedTrip(
                id=id, title=title, destination=destination, price=price, image=image, description=description, created_at=created_at
            )

    def get_trip(self, _id: int) -> SavedTrip:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, destination, price, image, description, created_at
                FROM {self.trip_table_name}
                WHERE id = {_id}
            """
            result: tuple = cursor.execute(query).fetchone()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'No trip found with id {_id}'
                )
            id, title, destination, price, image, description, created_at = result
            return SavedTrip(
                id=id, title=title, destination=destination, price=price, image=image, description=description, created_at=created_at
            )

    def get_trips(self, limit: int = 10, q: str = '') -> list[SavedTrip]:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, destination, price, image, description, created_at
                FROM {self.trip_table_name}
                WHERE title LIKE '%{q}%' OR destination LIKE '%{q}%'
                ORDER BY id DESC
                LIMIT {limit}
            """
            data: list[tuple] = cursor.execute(query).fetchall()

        return [
            SavedTrip(
                id=id, title=title, destination=destination, price=price, image=image, description=description, created_at=created_at
            )
            for (id, title, destination, price, image, description, created_at) in data
        ]

    def update_trip_price(self, _id: int, new_price: float) -> SavedTrip:
        self.get_trip(_id)

        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                        UPDATE {self.trip_table_name}
                        SET price = ?
                        WHERE id = ?
            """
            cursor.execute(query, (new_price, _id))
        return self.get_trip(_id)

    def delete_trip(self, _id: int):
        self.get_trip(_id)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                        DELETE FROM {self.trip_table_name}
                        WHERE id = ?
            """
            cursor.execute(query, (_id,))
        return True


storage = StorageSQLite('trips_db.sqlite')

