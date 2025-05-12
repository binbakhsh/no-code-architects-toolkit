def upload_to_s3(file_path, s3_url, access_key, secret_key, bucket_name, region):
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    client = session.client(
        's3',
        endpoint_url=s3_url,
        verify=os.environ.get("S3_VERIFY_SSL", "true").lower() == "true"
    )

    try:
        # Upload the file to the specified S3 bucket
        with open(file_path, 'rb') as data:
            client.upload_fileobj(data, bucket_name, os.path.basename(file_path), ExtraArgs={'ACL': 'public-read'})

        # URL encode the filename for the URL
        encoded_filename = quote(os.path.basename(file_path))
        file_url = f"{s3_url}/{bucket_name}/{encoded_filename}"
        return file_url
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise
