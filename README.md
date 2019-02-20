# Updating code

1. `cd venv/lib/python3.6/site-packages`, and zip up the dependencies as
`zip -r9 ../../../../function.zip .`
2. Change dir back to root of repo, and add `app.py` etc
`zip -g function.zip app.py`
3. Update the lambda function: `aws lambda update-function-code --function-name UnreadEmailNotificationsIntermediary --zip-file fileb://function.zip`

# Testing it

`aws lambda invoke --function-name UnreadEmailNotificationsIntermediary output.txt`

Make sure that in the lambda console the handler is set as `app.handler`