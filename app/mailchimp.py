import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv

load_dotenv()

MAILCHIMP_API_KEY       = os.environ.get("MAILCHIMP_API_KEY")
MAILCHIMP_SERVER_PREFIX = os.environ.get("MAILCHIMP_SERVER_PREFIX")

mailchimp_client = MailchimpMarketing.Client()
mailchimp_client.set_config({
    "api_key": MAILCHIMP_API_KEY,
    "server":  MAILCHIMP_SERVER_PREFIX
    })

def create_audience(body):
    try:
      response = mailchimp_client.lists.create_list(body)
      print("Response: {}".format(response))
    except ApiClientError as error:
      print("An exception occurred: {}".format(error.text))

def create_contact(list_id, member_info):
    try:
        response = mailchimp_client.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))