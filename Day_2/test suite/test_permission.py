from core.auth import validate_token
from core.permissions import require_scope


def test_reader_has_read_scope():

    validate_token("reader-token")

    result = require_scope("read")

    assert result is None


def test_reader_cannot_write():

    validate_token("reader-token")

    result = require_scope("write")

    assert result["code"] == "FORBIDDEN"


def test_writer_has_write_scope():

    validate_token("writer-token")

    result = require_scope("write")

    assert result is None