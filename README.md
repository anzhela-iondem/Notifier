# Notifier APP 
### Summary
The App is designed to get the POST request and, based on the "event_type" value of the request, to send a message either to the defined Slack channel or to the provided email address.

### Requirements
Python 3.9.1 and upper versions.\
External libraries: 
- email-validator==1.3.0 
- Flask==2.2.2 
- py3dns==3.2.1
- python-dotenv==0.21.0 
- requests==2.28.1 
- slack-sdk==3.18.3 
- slackclient==2.9.4 

### POST Request Structure
Body content type: Application/json \
Json body ex.: \
{ \
  "event_type": "new_publication", \
  "body": "Hi,\nThere is a new publication.", \
  "to": "angelaiondem@yahoo.com"\
} \
The "event_type" value is string and can have only two values: "new_publication" or "approved_publication". \
The "body" value must be not an empty string. \
The "to" is mandatory when the "event_type" value is equal to "approved_publication" otherwise it can be None.


### .env file
.env file location should be in the main Notifier folder. \
It must include the following keys with their values: 
- SMTP_HOST
- SMTP_PORT
- EMAIL_USERNAME
- EMAIL_APP_PASS
- FROM_EMAIL
- SLACK_TOKEN
