from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Mapping

import certifi
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from cars_api.schemas2 import CarCreateSchema, CarPatchSchema, CarSavedSchema
from cars_api.settings2 import settings


class BaseStorage(ABC):
    @abstractmethod
    def create_car(self, car: CarCreateSchema) -> CarSavedSchema:
        pass

    @abstractmethod
    def get_car(self, car_id: str) -> CarSavedSchema:
        pass

    @abstractmethod
    def get_cars(self, q: str = "", page: int = 1) -> list[CarSavedSchema]:
        pass

    @abstractmethod
    def delete_car(self, car_id: str) -> None:
        pass

    @abstractmethod
    def patch_car(self, car_id: str, new_car_data: CarPatchSchema) -> CarSavedSchema:
        pass

    @abstractmethod
    def put_car(self, car_id: str, car: CarCreateSchema) -> CarSavedSchema:
        pass


class MongoDBStorage(BaseStorage):
    def __init__(self):
        client = MongoClient(
            settings.MONGO_URI,
            server_api=ServerApi("1"),
            tlsCAFile=certifi.where(),
        )
        db = client[settings.MONGO_DB]
        self.collection = db[settings.MONGO_COLLECTION]

    def create_car(self, car: CarCreateSchema) -> CarSavedSchema:
        car_dict = car.model_dump()
        car_dict["created_at"] = datetime.now()

        saved_car_in_db = self.collection.insert_one(car_dict)
        saved_car = self.get_car(str(saved_car_in_db.inserted_id))

        return saved_car

    def get_car(self, car_id: str) -> CarSavedSchema:
        car = self.collection.find_one(self._get_object_id_query(car_id))

        if not car:
            raise HTTPException(
                detail=f"Car with id={car_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return self.transform_car(car)

    def get_cars(self, q: str = "", page: int = 1) -> list[CarSavedSchema]:
        query = {}

        if q:
            query_words = [word.lower() for word in q.split() if len(word) > 1]

            if query_words:
                query_words_dicts = [
                    {"brand": {"$regex": word, "$options": "i"}}
                    for word in query_words
                ]
                query = {
                    "$and": query_words_dicts,
                }

        skip = (page - 1) * settings.PAGE_SIZE
        cars = self.collection.find(query).limit(settings.PAGE_SIZE).skip(skip)

        saved_cars = []
        for car in cars:
            saved_cars.append(self.transform_car(car))

        return saved_cars

    def delete_car(self, car_id: str) -> None:
        self.get_car(car_id)
        self.collection.delete_one(self._get_object_id_query(car_id))

    def patch_car(self, car_id: str, new_car_data: CarPatchSchema) -> CarSavedSchema:
        update_data = new_car_data.model_dump(exclude_none=True)

        if not update_data:
            return self.get_car(car_id)

        result = self.collection.update_one(
            self._get_object_id_query(car_id),
            {"$set": update_data},
        )

        if not result.raw_result["n"]:
            raise HTTPException(
                detail=f"Car with id={car_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return self.get_car(car_id)

    def put_car(self, car_id: str, car: CarCreateSchema) -> CarSavedSchema:
        old_car = self.get_car(car_id)
        car_dict = car.model_dump()
        car_dict["created_at"] = old_car.created_at

        result = self.collection.replace_one(
            self._get_object_id_query(car_id),
            car_dict,
        )

        if not result.raw_result["n"]:
            raise HTTPException(
                detail=f"Car with id={car_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return self.get_car(car_id)

    def _get_object_id_query(self, car_id: str) -> dict[str, ObjectId]:
        try:
            query = {"_id": ObjectId(car_id)}
            return query
        except InvalidId:
            raise HTTPException(
                detail=f"Invalid car id {car_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def transform_car(self, car: Mapping[str, Any]) -> CarSavedSchema:
        return CarSavedSchema(
            id=str(car["_id"]),
            brand=car["brand"],
            model=car["model"],
            year=car["year"],
            price=car["price"],
            color=car["color"],
            is_available=car["is_available"],
            created_at=car["created_at"],
        )


storage: BaseStorage = MongoDBStorage()
