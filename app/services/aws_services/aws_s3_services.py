import logging

import boto3
from botocore.exceptions import ClientError


class AwsS3Service(object):
    def __init__(self, region=None):
        try:
            self.s3_resource = boto3.resource('s3')
            if region is None:
                self.s3_client = boto3.client('s3')
            else:
                self.s3_client = boto3.client('s3', region_name=region)
        except ClientError as e:
            logging.error(e)
            raise e

    def create_bucket(self, bucket_name, region=None, **kwargs):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name,
                                             CreateBucketConfiguration=location)
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def upload_file(self, file_name, bucket, object_name=None, extra_args=None, callback=None, config=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :type str
        :param bucket: Bucket to upload to
        :type str
        :param object_name: S3 object name. If not specified then file_name is used
        :type  str
        :param extra_args: Extra arguments that may be passed to the client operation.
        :type dict
        :param callback: A method which takes a number of bytes transferred to be periodically called during the upload.
        :type function
        :param config: The transfer configuration to be used when performing the transfer.
        :type boto3.s3.transfer.TransferConfig
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=extra_args,
                                                  Callback=callback,
                                                  Config=config)
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def download_file(self, bucket, object_name, file_name=None, extra_args=None, callback=None, config=None):
        """Download a file from an S3 bucket

        :param bucket: Bucket to download from
        :type bucket: str
        :param object_name: S3 object name. If not specified then file_name is used
        :type  object_name: str
        :param file_name: File to upload. If not specified then object_name is used
        :type file_name: str
        :param extra_args: Extra arguments that may be passed to the client operation.
        :type extra_args: dict
        :param callback: A method which takes a number of bytes transferred to be periodically called during the upload.
        :type callback: function
        :param config: The transfer configuration to be used when performing the transfer.
        :type config: boto3.s3.transfer.TransferConfig
        :return: True if file was download, else False
        """

        # If S3 object_name was not specified, use file_name
        if file_name is None:
            file_name = object_name.split('/')[-1]

        # Download the file
        try:
            response = self.s3_client.download_file(bucket, object_name, file_name,
                                                    ExtraArgs=extra_args,
                                                    Callback=callback,
                                                    Config=config)
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def generate_presigned_post(self, bucket, object_name, fields=None, conditions=None, expiresin=3600):
        """

        :param bucket: Bucket to upload to
        :type bucket: str
        :param object_name: S3 object name.
        :type object_name: str
        :param fields: A dictionary of prefilled form fields to build on top of. Elements that may be
                    included are acl, Cache-Control, Content-Type, Content-Disposition, Content-Encoding,
                    Expires, success_action_redirect, redirect, success_action_status, and x-amz-meta-.
                    Note that if a particular element is included in the fields dictionary it will not
                    be automatically added to the conditions list. You must specify a condition for the
                    element as well.
        :type fields: dict
        :param conditions: A list of conditions to include in the policy. Each element can be either a list
                    or a structure
        :type: conditions: dict
        :param expiresin: The number of seconds the presigned post is valid for.
        :type expiresin: The number of seconds the presigned post is valid for.
        :return:
        """
        try:
            response = self.s3_client.generate_presigned_post(bucket, object_name, Fields=fields, Conditions=conditions,
                                                              ExpiresIn=expiresin)
            return response
        except ClientError as e:
            logging.error(e)
            return None

    def generate_presigned_url(self, bucket, object_name, fields=None, conditions=None, expiresin=3600):
        """

        :param bucket: Bucket to upload to
        :type bucket: str
        :param object_name: S3 object name.
        :type object_name: str
        :param fields: A dictionary of prefilled form fields to build on top of. Elements that may be
                    included are acl, Cache-Control, Content-Type, Content-Disposition, Content-Encoding,
                    Expires, success_action_redirect, redirect, success_action_status, and x-amz-meta-.
                    Note that if a particular element is included in the fields dictionary it will not
                    be automatically added to the conditions list. You must specify a condition for the
                    element as well.
        :type fields: dict
        :param conditions: A list of conditions to include in the policy. Each element can be either a list
                    or a structure
        :type: conditions: dict
        :param expiresin: The number of seconds the presigned post is valid for.
        :type expiresin: The number of seconds the presigned post is valid for.
        :return:
        """
        try:
            response = self.s3_client.generate_presigned_post(bucket, object_name, Fields=fields, Conditions=conditions,
                                                              ExpiresIn=expiresin)
            return response
        except ClientError as e:
            logging.error(e)
            return None

    def create_presigned_url(self, bucket_name, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': bucket_name,
                                                                     'Key': object_name},
                                                             ExpiresIn=expiration)

            # The response contains the presigned URL
            return response
        except ClientError as e:
            logging.error(e)
            return None

    def get_bucket_cors(self, bucket_name):
        """Retrieve the CORS configuration rules of an Amazon S3 bucket

        :param bucket_name: string
        :return: List of the bucket's CORS configuration rules. If no CORS
        configuration exists, return empty list. If error, return None.
        """

        # Retrieve the CORS configuration
        try:
            response = self.s3_client.get_bucket_cors(Bucket=bucket_name)
            return response['CORSRules']
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
                return []
            else:
                # AllAccessDisabled error == bucket not found
                logging.error(e)
                return None

    def set_bucket_cors(self, bucket_name, cors_configuration):
        """Set the CORS configuration rules of an Amazon S3 bucket

        :param bucket_name: string
        :param cors_configuration: cors configuration.
            cors_configuration = {
                'CORSRules': [{
                    'AllowedHeaders': ['Authorization'],
                    'AllowedMethods': ['GET', 'PUT'],
                    'AllowedOrigins': ['*'],
                    'ExposeHeaders': ['GET', 'PUT'],
                    'MaxAgeSeconds': 3000
                }]
            }
        :return: True if set bucket CORS success, else False
        """

        # Retrieve the CORS configuration
        try:
            response = self.s3_client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def get_object(self, bucket_name, key, **kwargs):
        try:
            response = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=key,
                **kwargs
            )
            return response
        except ClientError as e:
            logging.error(e)
            return None

    def copy_object(self, bucket_name, src_key, key, **kwargs):
        try:
            copysource = {'Bucket': bucket_name, 'Key': src_key}
            response = self.s3_resource.meta.client.copy(copysource, bucket_name, key, **kwargs)
            return response
        except ClientError as e:
            logging.exception(e)
            return None
