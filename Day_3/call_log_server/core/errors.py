from schemas.call_schemas import BaseResponse

def error_response(error: str,code: str,suggestion: str,response_class):
    return response_class(
        success=False,
        error=error,
        code=code,
        suggestion=suggestion
    )