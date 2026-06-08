from core.auth import validate_token


def test_missing_token():

    result = validate_token("")

    assert result["code"] == "UNAUTHORIZED"


def test_invalid_token():

    result = validate_token("bad-token")

    assert result["code"] == "INVALID_TOKEN"


def test_valid_token():

    result = validate_token("reader-token")

    assert result["success"] is True