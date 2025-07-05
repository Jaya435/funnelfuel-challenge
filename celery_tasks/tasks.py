import os

from celery import shared_task

from task_manager.logger import create_logger

# Extract the filename without extension
filename = os.path.splitext(os.path.basename(__file__))[0]

logger = create_logger(logger_name=filename)

# @shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3},
#              name='campaign:get_campaign_task')
# def get_campaign_task(self, campaign: str):
#     campaign = campaigns.get_all_campaign(campaign)
#     return campaign

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3},
             name='campaign:create_campaign_task', rate_limit="40/m")
def create_campaign_task(self):
    logger.info("Calling third part DSP app and creating a submitting a campaign")