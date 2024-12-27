from FlaskApp.log_configs import logger
from FlaskApp.scheduler_configs import Scheduler
from .mongo_db import MongoHandler


class SchedulerJobs(object):
    def __init__(self):
        self.scheduler = Scheduler()

    @staticmethod
    def export_data_to_mongodb():
        try:
            logger.info("exporting data to mongodb...")
            print(f'Records Fetched: {MongoHandler().get_data(collection_name="test")}')
        except Exception as export_err:
            logger.error(f"Exception occurred while exporting the data to MongoDB, Exception: {export_err}")

    def add_scheduler_basic_jobs(self):
        logger.info("Removing the existing Scheduler jobs...")
        if sc_jobs := self.scheduler.get_jobs():
            jobs_to_delete = ['SchedulerJobs.export_data_to_mongodb']
            for job in sc_jobs:
                if job.name in jobs_to_delete:
                    self.scheduler.remove_job(job.id)
        logger.info("Adding Scheduler jobs...")
        self.scheduler.create_job(self.export_data_to_mongodb)
