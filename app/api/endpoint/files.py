from typing import Any
from fastapi import APIRouter, Response, UploadFile, File
from datetime import datetime
from calendar import timegm

from app.util.asset_storage import s3upload

router = APIRouter()


@router.post("")
async def upload_file(kind: str, file: UploadFile = File(...)) -> Any:
    """
    파일 업로드
    :param file: 업로드할 파일
    :param kind: 업로드할 파일의 종류
    :return: 업로드한 파일의 s3 주소
    """
    path = kind.replace("-", "/") + "/"
    filename = path[-1] + "_" + str(timegm(datetime.utcnow().utctimetuple())) + ".png"
    obj_url = await s3upload(file, path, filename)
    return Response(obj_url, status_code=201)
