from flask_restx import Api

api: Api = Api(
    doc="/",  # Default value for the swagger, it can be changed to any value
    version="4.0.0",
    title="FlaskPostgresqlMongo",
    description="This application built with Flask as backend with Postgresql and Mongo db",
)
