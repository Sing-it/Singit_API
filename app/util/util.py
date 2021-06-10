import boto3

from app.core.config import settings


class Util:
    def s3upload(self, file, filename):
        """
        :param file: 업로드할 파일
        :param filename: 업로드할 파일의 이름
        :return: 업로드한 파일의 s3 경로
        """
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_CONFIG["ACCESS_KEY_ID"],
                aws_secret_access_key=settings.AWS_CONFIG["SECRET_KEY"],
            )
            region = settings.AWS_CONFIG["REGION"]

            bucket_name = settings.AWS_CONFIG["BUCKET_NAME"]
            s3.upload_fileobj(
                file, bucket_name, filename, ExtraArgs={"ACL": "public-read"}
            )

            url = "https://s3-{}.amazonaws.com/{}/{}".format(
                region, bucket_name, filename
            )

        except Exception as e:
            return e
        return url
