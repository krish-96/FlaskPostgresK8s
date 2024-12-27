from bson import ObjectId
from typing import List, Dict, Optional, Tuple

from FlaskApp.log_configs import logger
from FlaskApp.database import get_mongo_connection, get_mongo_client, get_mongo_db_name


class MongoClientWrapper:
    def __init__(self):
        self.mongo_con = None

    def __enter__(self):
        if not self.mongo_con:
            self.mongo_con = get_mongo_connection()
        logger.debug("MongoDB connection opened.")
        return self.mongo_con

    def __exit__(self, exc_type, exc_value, trace):
        if self.mongo_con:
            self.mongo_con.close()
            logger.debug("MongoDB connection closed.")


class MongoHandler:
    def __init__(self):
        super().__init__()
        self.mongo_con = get_mongo_connection()

    def get_collections(self, collection_name=None):
        try:
            logger.info("Fetching the collections")
            available_collections = self.mongo_con.list_collection_names()
            logger.debug(f"db list_collection_names: {available_collections}")
            if collection_name:
                if collection_name not in available_collections:
                    raise ValueError("Given Collection Name is not available!")
                logger.debug("Given Collection is available!")
                return self.mongo_con.get_collection(collection_name)
            return available_collections
        except Exception as col_err:
            logger.error(f"Failed to fetch the collection, Exception: {col_err}")
            return False

    def create_collections(self, collection_names: List):
        try:
            logger.info("Creating the collections")
            collections_created = []
            collections_failed = []
            for collection_name in collection_names:
                try:
                    created_collection = self.mongo_con.create_collection(collection_name)
                    if created_collection.name == collection_name:
                        collections_created.append(collection_name)
                    else:
                        collections_failed.append(collection_name)
                except Exception as create_err:
                    collections_failed.append(str(create_err))
            logger.debug("Creating the collections is successful")
            return collections_created, collections_failed
        except Exception as col_err:
            logger.error(f"Failed to create the collections, Exception: {col_err}")
            return False

    def delete_collections(self, collection_names: List):
        try:
            logger.info("Deleting the collections")
            collections_deleted = []
            collections_failed = []
            for collection_name in collection_names:
                if collection_name not in self.get_collections():
                    collections_failed.append({'collection': collection_name, "reason": "Collection not found"})
                    continue
                try:
                    self.mongo_con.drop_collection(collection_name)
                    collections_deleted.append(collection_name)
                except:
                    collections_failed.append(collection_name)
            logger.debug("Deleting the collections is successful")
            return collections_deleted, collections_failed
        except Exception as col_err:
            logger.error(f"Failed to Delete the collections, Exception: {col_err}")
            return False
    def get_data(self, collection_name: str, filters_data=None) -> Optional[List[Dict]]:
        try:
            logger.info(f"Fetching data for data from the collection {collection_name}")
            logger.debug(f"Filter data: {filters_data}")
            collection = self.get_collections(collection_name)
            if filters_data and isinstance(filters_data, dict):
                if "id" in filters_data:
                    filters_data["_id"] = ObjectId(filters_data["id"])
                    del filters_data["id"]
                data = collection.find(filters_data).to_list()
            else:
                data = collection.find().to_list()
            logger.info(f"Fetching data for data from the collection {collection_name}")
            return data
        except Exception as e:
            logger.error(f"Error fetching data from {collection_name}: {e}")
            return None

    def insert_data(self, data: Optional[Dict | List[Dict] | Tuple[Dict, Dict]], collection_name: str) -> bool:
        try:
            if not isinstance(data, (dict, list, tuple)):
                logger.error(f"Failed to insert the data, expected dict or list of dicts but got {type(data)}")
                raise TypeError("data must be a dict or list of dicts!")
            data = [data] if isinstance(data, dict) else data
            if not data:
                logger.info(f"Failed to insert the given data into the collection: {collection_name}")
                return False
            collection = self.get_collections(collection_name=collection_name)
            print(f"collection: => {collection}")
            if collection in [False, None]:
                logger.info(f"Failed to insert the given data, Collection {collection_name} is not available")
                return False
            self.get_collections(collection_name=collection_name).insert_many(data)
            logger.info(f"Inserted the given data into the collection: {collection_name}")
            return True

        except Exception as col_err:
            logger.error(f"Failed to insert the data into the given collection: {collection_name}, Exception: {col_err}")
            return False

    def delete_data(self, filters_data: Dict, collection_name: str) -> bool:
        try:
            if not isinstance(filters_data, dict):
                logger.error(f"Failed to insert the data, expected dict or list of dicts but got {type(data)}")
                raise TypeError("data must be a dict or list of dicts!")
            # collection = self.get_collections(collection_name=collection_name)
            # print(f"collection: => {collection}")
            # if collection in [False, None]:
            #     logger.info(f"Failed to insert the given data, Collection {collection_name} is not available")
            #     return False
            # self.get_collections(collection_name=collection_name).insert_many(data)
            logger.info(f"Inserted the given data into the collection: {collection_name}")
            return True

        except Exception as col_err:
            logger.error(f"Failed to insert the data into the given collection: {collection_name}, Exception: {col_err}")
            return False

    def execute_query(self, data: Optional[Dict | List[Dict] | Tuple[Dict, Dict]], collection_name: str) -> bool:
        try:
            if not (collection_name and data):
                raise Exception("Collection name or data is not provided!")
            data = data if isinstance(data, (list, tuple)) else [data]
            if not data:
                logger.info(f"Failed to insert the given data into the collection: {collection_name}")
                return False
            return self.insert_data(collection_name=collection_name, data=data)
        except Exception as col_err:
            logger.error(f"Failed to delete the collection, Exception: {col_err}")
            return False
