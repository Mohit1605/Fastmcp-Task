import pytest

from core.validators import validate_tool_annotations


def test_invalid_annotation_combination():

    annotations = {
        "destructiveHint": True,
        "idempotentHint": True
    }

    with pytest.raises(RuntimeError):

        validate_tool_annotations(
            tool_name="bad_tool",
            annotations=annotations
        )