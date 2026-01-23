class ResponseModel:
    def __init__(self, status="SUCCESS", statusCode=200, message=None, data=None):
        self.status = status
        self.statusCode = statusCode
        self.message = message
        self.data = data

