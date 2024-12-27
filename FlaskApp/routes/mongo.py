from flask import request
from flask_restx import Resource

from FlaskApp.restx import api
from FlaskApp.log_configs import logger
from FlaskApp.request_handlers import MongoHandler
from FlaskApp.database import get_mongo_connection
from FlaskApp.database.models.requests import (
    get_restx_model,
    create_collection_model,
    insert_data_in_collection_model,
    delete_data_in_collection_model
)

mongo_ns = api.namespace("api/mongo", description="A namespace for Mongo db endpoints")

SUCCESS_STATUS = 200
FAILED_STATUS = 400
COLLECTION_NAME_REQUIRED = "Collection name is required"

# Create the flask_restx models
create_collection_model = get_restx_model(mongo_ns, create_collection_model)
insert_data_model = get_restx_model(mongo_ns, insert_data_in_collection_model)
delete_data_model = get_restx_model(mongo_ns, delete_data_in_collection_model)


@mongo_ns.route("/list-collection")
class ListCollections(Resource):
    def get(self):
        try:
            logger.info("Listing collections received request")
            mongo_con = get_mongo_connection()
            collections = mongo_con.list_collections()
            results = [col.get('name') for col in collections] if collections else collections
            logger.info("Collections are fetched, sending the response")
            return dict(status="Success", collections=results), SUCCESS_STATUS
        except Exception as col_err:
            logger.error(f"Exception occurred while fetching the collections, Exception: {col_err}")
            return dict(status='failed', message="Failed to fetch the collections"), FAILED_STATUS


@mongo_ns.route("/create-collection")
class CreateCollection(Resource):

    @mongo_ns.expect(create_collection_model)
    def post(self):
        try:
            logger.info("Creating the collections received from request")
            payload = request.get_json(silent=True, force=True)
            collection_name = payload.get("collectionName")
            if not collection_name:
                return dict(message=COLLECTION_NAME_REQUIRED), FAILED_STATUS
            collection_names = collection_name if isinstance(collection_name, list) else [collection_name]
            resp = MongoHandler().create_collections(collection_names)
            if not resp:
                return dict(message="Failed to create the collections"), FAILED_STATUS
            collections_created, collections_failed = resp if isinstance(resp, tuple) else tuple([], [])
            message = "Created the collection successfully"
            logger.info("Collections are created, sending the response")
            return dict(message=message, collections_created=collections_created, collections_failed=collections_failed)
        except Exception as e:
            logger.error(f"Exception occurred while creating the collections, Exception: {e}")
            return dict(message="Failed to create the collections"), FAILED_STATUS


@mongo_ns.route("/delete-collection")
class DeleteCollection(Resource):

    @mongo_ns.expect(create_collection_model)
    def post(self):
        try:
            logger.info("Deleting the collections received in request")
            payload = request.get_json(silent=True, force=True)
            collection_name = payload.get("collectionName")
            if not collection_name:
                return dict(message=COLLECTION_NAME_REQUIRED), FAILED_STATUS
            collection_names = collection_name if isinstance(collection_name, list) else [collection_name]
            resp = MongoHandler().delete_collections(collection_names)
            if not resp:
                return dict(message="Failed to delete the collections"), FAILED_STATUS
            collections_deleted, collections_failed = resp if isinstance(resp, tuple) else tuple([], [])

            message, status = "Deleted the collection successfully", SUCCESS_STATUS
            if not collections_deleted:
                message, status = "Failed to delete the collections.", FAILED_STATUS
            logger.info("Collections are deleted, sending the response")
            return dict(message=message, collections_deleted=collections_deleted,
                        delete_collections_failed=collections_failed), status
        except Exception as e:
            logger.error(f"Exception occurred while deleting the collections, Exception: {e}")
            return dict(message="Failed to delete the collections"), FAILED_STATUS


@mongo_ns.route("/insert-data")
class InsertData(Resource):

    # @mongo_ns.expect(insert_data_model)
    def post(self):
        try:
            logger.info("Inserting the data in the given collection")
            payload = request.get_json(silent=True, force=True)
            collection_name = payload.get("collectionName")
            data = payload.get("data")
            print(f"data:==> {data}")
            if not collection_name:
                return dict(message=COLLECTION_NAME_REQUIRED), FAILED_STATUS
            resp = MongoHandler().insert_data(collection_name=collection_name, data=data)
            if not resp:
                return dict(message="Failed to insert the data into the given collection"), FAILED_STATUS
            message = "Inserted the data into the given collection successfully"
            logger.info("Data inserted successfully, sending the response")
            return dict(message=message), SUCCESS_STATUS
        except Exception as e:
            logger.error(f"Exception occurred while inserting the collections, Exception: {e}")
            return dict(message="Failed to create the collections"), FAILED_STATUS


@mongo_ns.route("/get-data")
class GetData(Resource):

    # @mongo_ns.expect(insert_data_model)
    def get(self):
        try:
            logger.info("Request received to fetch the data")
            payload = request.get_json(silent=True, force=True)
            collection_name = payload.get("collectionName")
            filter_data = payload.get("filterData")
            if not collection_name:
                return dict(message=COLLECTION_NAME_REQUIRED), FAILED_STATUS
            resp = MongoHandler().get_data(collection_name=collection_name, filters_data=filter_data)
            if resp is None:
                return dict(message="Failed to fetch the data from the given collection"), FAILED_STATUS
            final_response = []
            for i in resp:
                if "_id" in i:
                    i["id"] = str(i["_id"])
                    del i['_id']
                final_response.append(i)
            logger.info("Data fetched successfully, sending the response")
            return dict(message="Fetching the data from the given collection is successful",
                        data=final_response), SUCCESS_STATUS
        except Exception as e:
            logger.error(f"Exception occurred while fetching the data, Exception: {e}")
            return dict(message="Failed to fetch the data"), FAILED_STATUS


@mongo_ns.route("/delete-data")
class DeleteData(Resource):

    # @mongo_ns.expect(delete_data_model)
    def post(self):
        try:
            logger.info("Deleting the matching data in the given collection")
            payload = request.get_json(silent=True, force=True)
            collection_name = payload.get("collectionName")
            filters = payload.get("filters")
            if not collection_name:
                return dict(message=COLLECTION_NAME_REQUIRED), FAILED_STATUS
            resp = MongoHandler().delete_data(collection_name=collection_name, filters_data=filters)
            if not resp:
                return dict(message="Failed to delete the data with the given filters"), FAILED_STATUS
            message = "Deleted the data matching the filters"
            logger.info("Data deleted successfully, sending the response")
            return dict(message=message), SUCCESS_STATUS
        except Exception as e:
            logger.error(f"Exception occurred while deleting the data, Exception: {e}")
            return dict(message="Failed to delete the data"), FAILED_STATUS
