import boto3

from app.core.config import settings


class Util:
    def s3upload(self, file, path: str, filename: str):
        """
        :param file: 업로드할 파일
        :param path: bucket 내부 path 지정
        :param filename: 업로드할 파일의 이름
        :return: 업로드한 파일의 url
        """
        paths = [
            "image/artist/",
            "image/user/",
            "image/song/",
            "sound/material/song/",
            "sound/material/accompaniment/",
            "sound/user/sound/",
            "sound/artist/song/",
            "sound/artist/sound/",
        ]
        if path not in paths:
            return {"msg": "file kind isn't right"}
        path += filename
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_CONFIG["ACCESS_KEY_ID"],
                aws_secret_access_key=settings.AWS_CONFIG["SECRET_KEY"],
            )
            region = settings.AWS_CONFIG["REGION"]

            bucket_name = settings.AWS_CONFIG["BUCKET_NAME"]
            s3.upload_fileobj(file, bucket_name, path, ExtraArgs={"ACL": "public-read"})

            url = "https://s3-{}.amazonaws.com/{}/{}".format(region, bucket_name, path)

        except Exception as e:
            return e
        return url