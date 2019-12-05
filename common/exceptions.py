import rest_framework.exceptions
import rest_framework.status


class APIException(rest_framework.exceptions.APIException):
    status_code = rest_framework.status.HTTP_400_BAD_REQUEST
