from rest_framework.response import Response


def base_api_response(result=False, result_code=200, data=None, message=None):
    """API Response format"""
    if message is None:
        if result_code == 500:
            message = 'internal server error'
        elif result_code == 400:
            message = 'bad request'
        if result:
            message = 'success'

    response = {
        'result': result,
        'message': message,
        'data': data
    }

    return Response(status=result_code, data=response)
