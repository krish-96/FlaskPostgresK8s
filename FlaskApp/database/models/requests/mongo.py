from flask_restx import fields

# Model for creating a collection
create_collection_model = {
    "model_name": "CollectionCreate",
    "model_definition": {
        "collectionName": fields.List(
            fields.String, required=True, description="Name of the collection"
        )
    }
}

# Model for inserting data into a collection
# insert_data_in_collection_model = {
#     "model_name": "InsertData",
#     "model_definition": {
#         "collectionName": fields.String(required=True, description="Name of the collection"),
#         "data": fields.List(
#             fields.Nested(
#                 {
#                     "key": fields.String(required=True, description="Key to check in MongoDB"),
#                     "value": fields.Raw(required=True, description="Value to check for the key"),
#                 }
#             ),
#             required=True,
#             description="List of key-value pairs to insert"
#         )
#     }
# }
insert_data_in_collection_model = {
    "model_name": "InsertData",
    "model_definition": {
        "collectionName": fields.String(required=True, description="Name of the collection"),
        "data": fields.String(required=True, description="It will be executed in the database as it is")
    }
}

# Model for deleting data from a collection
delete_data_in_collection_model = {
    "model_name": "DeleteData",
    "model_definition": {
        "collectionName": fields.String(required=True, description="Name of the collection"),
        "data": fields.List(
            fields.Nested(
                {
                    "key": fields.String(required=True, description="Key to check in MongoDB"),
                    "value": fields.Raw(required=True, description="Value to check for the key"),
                }
            ),
            required=True,
            description="List of key-value pairs to match and delete"
        )
    }
}
