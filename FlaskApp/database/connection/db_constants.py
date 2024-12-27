# Database URI's
psql_uri = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
# username and password in the mongo uri must be percent-encoded
mongo_uri = "mongodb://{user}:{password}" \
        "@{host}:{port}/?" \
        "authSource={authentication_database}" \
        "&authMechanism=SCRAM-SHA-256"
