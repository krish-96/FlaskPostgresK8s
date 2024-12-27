from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

from FlaskApp.database import get_psql_uri
from FlaskApp.log_configs import logger

_scheduler = BackgroundScheduler()


class Scheduler:
    __instance = None
    __configured = False
    __start = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__configure()
            cls.__configured = True
        return cls.__instance

    def __configure(self):
        if not self.__configured:
            jobstores = {
                'default': SQLAlchemyJobStore(url=get_psql_uri())
            }
            executors = {
                'default': {'type': 'threadpool', 'max_workers': 20},
                'processpool': ProcessPoolExecutor(max_workers=5)
            }
            job_defaults = {
                'coalesce': False,
                'max_instances': 3
            }
            _scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    def __setup_scheduler(self):
        if not _scheduler.running:
            self.__configure()

    def setup_scheduler(self):
        self.__setup_scheduler()

    def shutdown(self):
        _scheduler.shutdown()

    def create_job(self, target, request=None):
        # _scheduler.add_job(target, 'interval', minutes=1, args=request)
        _scheduler.add_job(target, 'interval', seconds=59, args=request)

    def start_jobs(self):
        if not self.__start:
            _scheduler.start()

    def get_jobs(self):
        return _scheduler.get_jobs()

    def get_job(self, job_id):
        return _scheduler.get_job(job_id)

    def remove_job(self, job_id):
        logger.info(f'Removing the scheduler job with id: {job_id}')
        _scheduler.remove_job(job_id)
