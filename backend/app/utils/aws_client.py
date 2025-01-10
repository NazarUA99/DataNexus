import json
import boto3
from botocore.exceptions import ClientError
from secrets import token_urlsafe
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

from sqlmodel import create_engine

class AWSClient:
    def __init__(self, secret_id):
        self.secret_id = secret_id
        self.session = boto3.session.Session()
        logger.info(f"session is {self.session}")
        logger.info(self.session.available_profiles)
        self.client = self.session.client(
            service_name='secretsmanager'
        )

    def get_aws_secret(self):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=self.secret_id
            )
        except ClientError as e:
            logger.error(f"Error getting secret: {e}")
            raise e
        return get_secret_value_response['SecretString']

    def generate_secret(self):
        bits = 32
        key = token_urlsafe(bits)
        logger.info(f"generated key: {key}")

    def get_engine(self):
        db_props = json.loads(self.get_aws_secret(self.secret_id))
        logger.info(f"found DB props for : {db_props['db_name']}")
        main_db_connection_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(db_props['username'], db_props['password'], db_props['host'], db_props['port'], db_props['db_name'])
        return create_engine(main_db_connection_str)