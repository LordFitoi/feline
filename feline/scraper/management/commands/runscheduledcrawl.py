import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from scraper import settings as scraper_settings
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scraper.spiders.jobposts import JobPostSpider

from twisted.internet import reactor


class ScraperScheduleHandler:
    logger = logging.getLogger(__name__)

    def __init__(self, scheduler, settings=None, time_zone=settings.TIME_ZONE):
        self.scheduler = scheduler(timezone=time_zone)
        self.scheduler.add_jobstore(DjangoJobStore(), "default")

        self.settings = Settings()
        self.settings.setmodule(settings)
        self.crawler = CrawlerRunner(settings=self.settings)

    def add_job(self, callback, trigger, *args):
        callback_id = str(callback.__name__)
        
        self.scheduler.add_job(
            callback,
            trigger = trigger, 
            id = callback_id,
            max_instances = 1,
            replace_existing = True,
            args=[*args]
        )

        self.logger.info(f"Added job '{callback_id}'.")

    @staticmethod
    @util.close_old_connections
    def cleanup_job_entries(max_age=604_800):
        """
        This job deletes APScheduler job execution entries older than `max_age` from the database.
        It helps to prevent the database from filling up with old historical records that are no
        longer useful.
        
        :param max_age: The maximum length of time to retain historical job execution records.
                        Defaults to 7 days.
        """
        DjangoJobExecution.objects.delete_old_job_executions(max_age)

    @staticmethod
    def task(crawler):
        """
        This is the job that will be called by the scheduler when it fired.
        """
        d = crawler.crawl(JobPostSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def start(self, **kwargs):
        self.add_job(self.task, CronTrigger(**kwargs), self.crawler)
        self.add_job(self.cleanup_job_entries, CronTrigger(
            day_of_week="mon", hour="00", minute="00"))
    
        try:
            self.logger.info("Starting scheduler...")
            self.scheduler.start()

        except KeyboardInterrupt:
            self.logger.info("Stopping scheduler...")
            self.scheduler.shutdown()
            self.logger.info("Scheduler shut down successfully!")


class Command(BaseCommand):
    help = "Daily extract job posts info from different pages"
    arguments = {
        "-d": {
            "dest": "day",
            "type": str,
            "choices": ["sun", "mon", "tue", "wen", "thu", "fri", "sat", "*"],
            "help": """
                The exact day of the week. Value format (str): sun, mon, tue, wen, thu, fri, sat.
                If you write *, the task will run every day.""",
            "default": "*"
        },
        "-H": {
            "dest": "hour",
            "type": int,
            "help": """
                The exact hour of the day. Value format (int): 0 - 23.
                If you write *, the task will run every hour.""",
            "default": "0"
        },
        "-m": {
            "dest": "minute",
            "type": int,
            "help": """
                The exact minute of the hour. Value format (int): 0 - 59.
                If you write *, the task will run every minute.""",
            "required": False
        },
    }

    def add_arguments(self, parser):
        for argument_name, kwargs in self.arguments.items():
            parser.add_argument(argument_name, **kwargs)

    def handle(self, *args, **options):
        scheduler_handler = ScraperScheduleHandler(BlockingScheduler, scraper_settings)
        scheduler_handler.start(
            day_of_week = options.get("day"),
            hour = options.get("hour"),
            minute = options.get("minute")
        )
