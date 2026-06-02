from core.pagination import paginate


def test_last_page():

    items = [1, 2, 3, 4, 5]

    result = paginate(
        items,
        cursor=4,
        limit=2
    )

    assert result["data"] == [5]
    assert result["next_cursor"] is None
    assert result["has_more"] is False


def test_empty_page():

    result = paginate(
        [],
        cursor=0,
        limit=5
    )

    assert result["data"] == []
    assert result["has_more"] is False
    assert result["total_count"] == 0


def test_cursor_out_of_range():

    items = [1, 2, 3]

    result = paginate(
        items,
        cursor=100,
        limit=5
    )

    assert result["code"] == "CURSOR_OUT_OF_RANGE"


def test_invalid_limit():

    items = [1, 2, 3]

    result = paginate(
        items,
        cursor=0,
        limit=0
    )

    assert result["code"] == "INVALID_LIMIT"