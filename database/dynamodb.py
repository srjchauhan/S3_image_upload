import boto3
from config import S3Config, DynamodbConfig
from datetime import datetime


class Dynamodb:
    def __init__(self, isLocal: bool = DynamodbConfig.islocal):
        self.db = boto3.resource('dynamodb', aws_access_key_id=S3Config.aws_access_key_id,
                                 aws_secret_access_key=S3Config.aws_secret_access_key,
                                 region_name=S3Config.region_name)
        if isLocal:
            self.db = boto3.resource('dynamodb', endpoint_url=DynamodbConfig.endpoint_url)
        self._table_name = DynamodbConfig.table_name

    def create_table(
            self,
            table_name: str = None,
            rd_unit: int = 1,
            wr_unit: int = 1,
    ):
        table_name = self._table_name if table_name is None else table_name
        self.db.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'img_name',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'img_name',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': rd_unit,
                'WriteCapacityUnits': wr_unit
            }
        )

    def insert(
            self,
            img_name: str,
            img_url: str,
            img_s3_path: str,
            table_name: str = None
    ):
        table_name = self._table_name if table_name is None else table_name
        try:
            _table = self.db.Table(table_name)
            resp = _table.put_item(
                Item={
                    'img_name': img_name,
                    'img_original_url': img_url,
                    'img_s3_path': img_s3_path,
                    'stored_time': str(datetime.now().timestamp())
                }
            )
            if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True, 'Done'
            else:
                raise Exception('unable to insert data')
        except Exception as e:
            return False, str(e)

    def delete(
            self,
            img_name: str,
            table_name: str = None
    ):
        table_name = self._table_name if table_name is None else table_name
        _table = self.db.Table(table_name)
        try:
            _table.delete_item(
                TableName=table_name,
                Key={
                    'img_name': img_name,
                }
            )
            return True, 'Done'
        except Exception as e:
            return False, str(e)

    def list_all(
            self,
            table_name: str = None
    ):
        table_name = self._table_name if table_name is None else table_name
        _table = self.db.Table(table_name)
        _response = _table.scan()
        data = _response['Items']
        while 'LastEvaluatedKey' in _response:
            _response = _table.scan(ExclusiveStartKey=_response['LastEvaluatedKey'])
            data.extend(_response['Items'])

        return data


if __name__ == "__main__":
    db = Dynamodb()
    try:
        db.create_table()
    except Exception as e:
        print(str(e))
        pass
