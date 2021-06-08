import memleak
import boto3
import ntpath
import json
from botocore.client import Config

def download_file(bucket_name, input_file):
    s3 = boto3.client('s3')
    return_msg = ""

    try:
        s3.download_file(bucket_name, input_file, "/tmp/" + input_file)
    except Exception as e:
        print(e.message)
        return_msg = "Unable to open input file"
    finally:
        return(return_msg)

def save_output_file(bucket_name, output_file):
    s3 = boto3.client('s3')
    output_file_name = ntpath.basename(output_file)

    try:
        s3.upload_file(output_file, bucket_name, output_file_name)
        public_url = "https://"+ bucket_name + ".s3.ca-central-1.amazonaws.com/" + output_file_name
        return(public_url)
    except Exception as e:
        print(e)

def pre_signed_s3_url(file, bucket, expiration):
    s3Client = boto3.client('s3')
    presigned_url = s3Client.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {
            'Bucket': bucket,
            'Key': file
        },
        ExpiresIn = expiration)
    return(presigned_url)

def lambda_handler(event, context):
    OUTPUT_FILE_PATH = "/tmp/"
    result_code = 200
    result_msg = ""
    event_body = json.loads(event['body'])
    output_bucket = 'memleak-output'
    bucket_name = "memleak-upload"

    # Receive bucket and file name
    input_file = event_body["file"]

    print('input_file: ' + input_file)

    # Download file from S3UploadBucket to /tmp
    if input_file is not None:
        result_msg = download_file(bucket_name, input_file)

    if result_msg == "Unable to open input file": result_code = 500

    # Analyze /tmp/input_file.csv for memleak candidates
    try:
        output_file = memleak.Main(OUTPUT_FILE_PATH + input_file)
    except Exception as e:
        print(e)

    # Upload output file to S3OutputBucket
    save_output_file(output_bucket,  output_file)

    # Pre-sign URL to download output file
    output_file_name = ntpath.basename(output_file)
    presigned_url = pre_signed_s3_url(output_file_name, output_bucket, 600)

    return {
        'statusCode': result_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/text'
        },
        'body': presigned_url
    }
