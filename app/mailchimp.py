import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from app.config import settings

mailchimp_client = MailchimpMarketing.Client()
mailchimp_client.set_config({
    "api_key": settings.MAILCHIMP_API_KEY,
    "server":  settings.MAILCHIMP_SERVER_PREFIX
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