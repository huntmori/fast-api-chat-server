import json

class BaseResponse:
    result: bool
    error: bool
    message: str
    data: object

    def __init__(self, result: bool, error: bool, message: str, data: object):
        self.result = result
        self.error = error
        self.message = message
        self.data = data

    @staticmethod
    def error(message: str) -> dict:
        return BaseResponse(
            result=False,
            error=True,
            message=message,
            data=None
        ).to_dict()

    @staticmethod
    def success(message: str, data: object) -> dict:
        return BaseResponse(
            result=True,
            error=False,
            message=message,
            data=data
        ).to_dict()

    def to_dict(self) -> dict:
        return {
            "result": self.result,
            "error": self.error,
            "message": self.message,
            "data": self.data
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
