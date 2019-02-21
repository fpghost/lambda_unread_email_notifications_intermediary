import json
import logging
import sys
import os
from boto3 import client as boto3_client
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


try:
    # The queue to publish the desired requests
    sqs_publish_sns_queue_url = os.environ['MARCEL_PUBLISH_SNS_QUEUE_URL']
    endpoint_url = os.environ['ENDPOINT_URL']
except KeyError:
    logger.error('ERROR: Missing environment variable')
    sys.exit()


sqs_client = boto3_client('sqs', endpoint_url=endpoint_url)


def handler(event, context):
    """
    Consumes from the "responses" queue, parses out the unread count
    and then constructs SNS payload and publishes to "publish sns" SQS queue
    :param event:
    :param context:
    :return:
    """
    for record in event.get('Records', []):
        try:
            logger.info(record['body'])
            json_record_body = json.loads(record['body'])
        except (ValueError, KeyError) as exc:
            return {'statusCode': 500, 'error': str(exc)}
        try:
            unread_count = json_record_body['body']['result_count']
        except KeyError:
            return {'statusCode': 500, 'error': 'unread_count is required'}
        try:
            endpoint_arn = json_record_body['extra_data']['endpoint_arn']
        except KeyError:
            return {'statusCode': 500, 'error': 'endpoint_arn is required'}
        try:
            apns_payload_str = json.dumps({"aps": {"alert": {"body": {"unread_count": unread_count}}}})
            payload = {'default': 'default message', 'APNS': apns_payload_str}
            sqs_msg = {'sns_payload': payload,
                       'endpoint_arn': endpoint_arn}
            logger.info('SQS: Publishing {}'.format(sqs_msg))
            sqs_client.send_message(QueueUrl=sqs_publish_sns_queue_url,
                                    MessageBody=json.dumps(sqs_msg))
            return {
                'statusCode': 200,
                'body': json.dumps({'sqs_msg': sqs_msg})
            }
        except ClientError as exc:
            logger.error(str(exc))
            return {'statusCode': 500, 'error': str(exc)}
