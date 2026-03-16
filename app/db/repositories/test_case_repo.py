from __future__ import annotations

from datetime import datetime
from typing import Any

from bson import ObjectId

from app.db.mongodb import get_database
from app.models.common import PyObjectId
from app.models.test_case import TestCaseCreate, TestCaseInDB


class TestCaseRepository:
    collection_name = "test_cases"

    @property
    def collection(self):
        db = get_database()
        if db is None:
            raise RuntimeError("MongoDB is not connected")
        return db[self.collection_name]

    async def create_one(
        self,
        test_case: TestCaseCreate,
        *,
        project_id: PyObjectId | str | None = None,
    ) -> TestCaseInDB:
        now = datetime.utcnow()
        doc: dict[str, Any] = test_case.model_dump()
        if project_id is not None:
            doc["project_id"] = ObjectId(str(project_id))
        doc["created_at"] = now
        doc["updated_at"] = now
        doc["status"] = "draft"
        res = await self.collection.insert_one(doc)
        doc["_id"] = res.inserted_id
        return TestCaseInDB.model_validate(doc)

    async def create_many(
        self,
        test_cases: list[TestCaseCreate],
        *,
        project_id: PyObjectId | str | None = None,
    ) -> list[TestCaseInDB]:
        if not test_cases:
            return []
        now = datetime.utcnow()
        docs: list[dict[str, Any]] = []
        for tc in test_cases:
            doc: dict[str, Any] = tc.model_dump()
            if project_id is not None:
                doc["project_id"] = ObjectId(str(project_id))
            doc["created_at"] = now
            doc["updated_at"] = now
            doc["status"] = "draft"
            docs.append(doc)

        res = await self.collection.insert_many(docs)
        for doc, _id in zip(docs, res.inserted_ids, strict=False):
            doc["_id"] = _id
        return [TestCaseInDB.model_validate(doc) for doc in docs]

    async def list(
        self,
        *,
        project_id: PyObjectId | str | None = None,
        url: str | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[TestCaseInDB]:
        query: dict[str, Any] = {}
        if project_id is not None:
            query["project_id"] = ObjectId(str(project_id))
        if url is not None:
            query["url"] = url

        cursor = (
            self.collection.find(query)
            .sort("created_at", -1)
            .skip(max(skip, 0))
            .limit(min(max(limit, 1), 500))
        )
        docs = await cursor.to_list(length=None)
        return [TestCaseInDB.model_validate(doc) for doc in docs]

