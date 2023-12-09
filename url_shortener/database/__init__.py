from random import randint
from typing import TypeVar, Type, Generic, Callable, Any, Mapping, Union, Optional

import pymongo
from motor.core import (
    AgnosticClient,
    AgnosticDatabase,
    AgnosticCollection,
    AgnosticCursor,
)
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import ReturnDocument
from pymongo.client_session import ClientSession
from pymongo.results import (
    UpdateResult,
    DeleteResult,
    InsertOneResult,
    InsertManyResult,
)
from pymongo.typings import _Pipeline

T = TypeVar("T")


def create_db_client():
    return AsyncIOMotorClient("mongodb://root:w6a12da124BP2@mongo:27017/")


# noinspection PyTypeChecker
class BaseDatabase(Generic[T]):
    def __init__(
        self,
        collection_name: str,
        database_client: AgnosticClient,
        _output_model_or_build_function: Type[T] | Callable[..., T],
    ):
        self.db: AgnosticDatabase = database_client.get_database(name="Database")
        self.collection: AgnosticCollection = self.db.get_collection(
            name=collection_name
        )

        self.output_type: Type[BaseModel] = _output_model_or_build_function

    async def get_one(self, filter_: dict = {}) -> Optional[T]:
        """Get the first instance of T that matches filter_"""
        _o = await self.collection.find_one(filter_)
        if not _o:
            return None
        return self.output_type(**_o)

    async def get_many(self, filter_: dict = {}, limit: int = 10**6) -> list[T]:
        """Get 10**6 instances of T that match filter_"""
        _ol: AgnosticCursor = self.collection.find(filter_)
        _ol: list[dict] = await _ol.to_list(length=limit)
        return [self.output_type(**_o) for _o in _ol]

    async def update_one(
        self, filter_: dict, update_: dict, session: ClientSession = None
    ) -> UpdateResult:
        """Update one that matches filter_ with update_"""
        _u: UpdateResult = await self.collection.update_one(
            filter_, update_, session=session
        )
        return _u

    async def update_many(
        self, filter_: dict, update_: dict, session: ClientSession = None
    ) -> UpdateResult:
        """Update all that match filter_ with update_"""
        _u: UpdateResult = await self.collection.update_many(
            filter_, update_, session=session
        )
        return _u

    async def count(self, filter_: dict) -> int:
        """Count documents. Returns int"""
        _c: int = await self.collection.count_documents(filter_)
        return _c

    async def delete_one(
        self, filter_: dict, session: ClientSession = None
    ) -> DeleteResult:
        """Delete one that matches filter_"""
        _u: DeleteResult = await self.collection.delete_one(filter_, session=session)
        return _u

    async def delete_many(
        self, filter_: dict, session: ClientSession = None
    ) -> DeleteResult:
        """Delete all that matches filter_"""
        _u: DeleteResult = await self.collection.delete_many(filter_, session=session)
        return _u

    async def insert_one(
        self,
        _o: T,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        session: ClientSession = None,
    ) -> InsertOneResult:
        """Insert one"""
        _o: BaseModel
        _i: InsertOneResult = await self.collection.insert_one(
            _o.dict(
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            ),
            session=session,
        )
        return _i

    async def insert_many(
        self,
        _ol: list[T],
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        session: ClientSession = None,
    ) -> InsertManyResult:
        """Insert many"""
        _ol: list[BaseModel]
        _i: InsertManyResult = await self.collection.insert_many(
            [
                _o.dict(
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
                for _o in _ol
            ],
            session=session,
        )
        return _i

    async def exists(self, filter_: dict) -> bool:
        """Check if document(s) that matches filter_ exist"""
        return bool(await self.get_one(filter_))

    async def get_unique_key_value(
        self,
        key: str,
        exclude_values: list[int] = [],
        _generate_function: Callable[[], Any] = lambda: randint(1, 10**5),
    ):
        """Get unique values that not in exclude_values and not in DB"""
        random = _generate_function()
        if await self.get_one({key: random}):
            return await self.get_unique_key_value(key, exclude_values)
        elif random in exclude_values:
            return await self.get_unique_key_value(key, exclude_values)
        else:
            return random

    async def get_one_and_update(
        self,
        filter_: Mapping[str, Any],
        update: Union[Mapping[str, Any], _Pipeline],
        return_updated: bool = False,
        session: ClientSession = None,
    ) -> Optional[T]:
        _o = await self.collection.find_one_and_update(
            filter=filter_,
            update=update,
            return_document=ReturnDocument.BEFORE
            if not return_updated
            else ReturnDocument.AFTER,
            session=session,
        )

        return self.output_type(**_o) if _o else None


class BaseDatabaseID(BaseDatabase[T]):
    def __init__(
        self,
        collection_name: str,
        database_client: AgnosticClient,
        output_type: Type[T],
        id_key: str,
        generate_id_function: Callable[[], Any] = lambda: randint(1, 10**5),
    ):
        super().__init__(collection_name, database_client, output_type)
        self.id_key = id_key
        self.generate_id_function = generate_id_function

    async def get_unused_id(self, exclude_ids: list[int] = []):
        """Get unique ID that not in exclude_ids and not in DB"""
        return await self.get_unique_key_value(
            self.id_key, exclude_ids, self.generate_id_function
        )

    async def get_one_id(self, id_: int | str) -> T | None:
        return await self.get_one({self.id_key: id_})

    async def update_one_id(self, id_: int | str, update_: dict) -> UpdateResult:
        return await self.update_one({self.id_key: id_}, update_)

    async def delete_one_id(self, id_: int | str) -> DeleteResult:
        return await self.delete_one({self.id_key: id_})

    async def exists_id(self, id_: int | str) -> bool:
        return await self.exists({self.id_key: id_})


class BaseDatabaseTime(BaseDatabase[T]):
    def __init__(
        self,
        collection_name: str,
        database_client: AgnosticClient,
        output_type: Type[T],
        time_key: str,
    ):
        super().__init__(collection_name, database_client, output_type)
        self.time_key = time_key

    async def get_by_page(
        self,
        filter_: dict,
        page_n: int,
        page_size: int = 20,
        sort_order: int = pymongo.DESCENDING,
    ) -> list[T]:
        """Get documents by page, sorted by time"""
        _l: AgnosticCursor = self.collection.find(filter_)
        _l = _l.sort([(self.time_key, sort_order)])
        _l = _l.skip(page_n * page_size).limit((page_n * page_size) + page_size)
        _l: list[dict] = await _l.to_list(length=page_size * 100)

        return [self.output_type(**_o) for _o in _l]

    async def get_many_sort_time(
        self, filter_: dict, limit: int = 10**6, sort_order: int = pymongo.DESCENDING
    ) -> list[T]:
        """Get many and sort by time"""
        _l: AgnosticCursor = self.collection.find(filter_)
        _l = _l.sort([(self.time_key, sort_order)])
        _l: list[dict] = await _l.to_list(length=limit)
        return [self.output_type(**_o) for _o in _l]

    # noinspection PyTypeChecker
    async def sum_by_amount_key(self, filter_: dict, amount_key: str = "amount") -> int:
        data: AgnosticCursor = self.collection.aggregate(
            [
                {"$match": filter_},
                {"$group": {"_id": 0, "amount": {"$sum": f"${amount_key}"}}},
            ]
        )
        data: list["dict"] = await data.to_list(1)
        if data:
            return data[0]["amount"]
        return 0
