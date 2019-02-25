This reads messages from the `MARCEL_RESPONSES_QUEUE_URL` SQS queue. For each
it parses the `unread_count`, `user_pk`, `endpoint_arn`. It uses these to construct and
SNS APNS payload for sending a push notification to the device with the `endpoint_arn`.
This message it publishes to the `MARCEL_PUBLISH_SNS_QUEUE_URL` SQS queue.


This is a specific lambda function, which is part of the chain of lambda functions
responsible for periodically sending the user a push notification with their unread
email count (See also [here](https://github.com/MarcelForArt/lambda_unread_email_notifications))


# Updating code

1. `cd venv/lib/python3.6/site-packages`, and zip up the dependencies as
`zip -r9 ../../../../function.zip .`
2. Change dir back to root of repo, and add `app.py` etc
`zip -g function.zip app.py`
3. Update the lambda function: `aws lambda update-function-code --function-name UnreadEmailNotificationsIntermediary --zip-file fileb://function.zip`

# Testing it

`aws lambda invoke --function-name UnreadEmailNotificationsIntermediary output.txt`

Make sure that in the lambda console the handler is set as `app.handler`