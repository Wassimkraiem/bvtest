from venv import logger

import boto3

from botocore.exceptions import ClientError
from botocore.config import Config
class DynamoDBVideosTable:
    def init(self, dyn_resource, table_name) -> None:
        self.dyn_resource = dyn_resource
        self.table = self.dyn_resource.Table(table_name)
        
    def create_table(self, table_name):
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "video_id", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "uploadDate", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "video_id", "AttributeType": "S"},
                    {"AttributeName": "uploadDate", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
            )
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            print('Table created successfully')
            return self.table

    def upload_video(self,Item : dict):
        try:
            self.table.put_item(
                Item=Item,
                ConditionExpression="attribute_not_exists(video_id)",
            )
        except ClientError as err:
            logger.error(
                "Couldn't add movie %s to table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

        
    
    def get_video(self, video_id):
        try:
            response = self.table.get_item(Key={"video_id": video_id,})
        except ClientError as err:
            logger.error(
                "Couldn't get movie %s from table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Item"]
    
    def delete_table(self):
        try:
            self.table.delete()
            self.table = None
        except ClientError as err:
            logger.error(
                "Couldn't delete table. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
    
    def delete_item(self,video_id):
        try:
            response = self.table.delete_item(
                Key={'video_id': {'S': video_id}} 
            )
            return {'message': 'Item deleted successfully', 'response': response}, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
video_table =  DynamoDBVideosTable()
def initialize_dynamodb(app):
    print("Initializing DynamoDB connection...")

    dyn_resource = boto3.resource(
        'dynamodb',
        region_name="eu-west-2",
        aws_access_key_id='dummyKey',  # Dummy credentials
        aws_secret_access_key='dummySecret', # Dummy credentials
        endpoint_url='http://dynamodb-local:8000',
    )
    try:
        table_description = video_table.create_table('VideoTable')
        print(f"Table description: {table_description}")
    except Exception as e:
        print(f"Error: {e}")
    video_table.init(dyn_resource, 'VideoTable')
    # video_table.delete_table()
    
def list_dynamodb_tables(app):
    dynamodb = boto3.client(
        'dynamodb',
        region_name="eu-west-2",  # Adjust as necessary
        aws_access_key_id="dummyKey",  # Replace with your access key
        aws_secret_access_key="dummySecret",  # Replace with your secret key
        endpoint_url="http://dynamodb-local:8000"  # Use this for DynamoDB Local
    )

    try:
        response = dynamodb.list_tables()
        print("Tables in DynamoDB:", response['TableNames'])
    except Exception as e:
        print(f"Error listing tables: {e}")