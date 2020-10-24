import pytest


def test_list_pushes_zero(list_pushes, pb_api):
    result = list_pushes()
    assert result.output == "\n"


def test_list_pushes_one(list_pushes, pb_api, data_regression):
    data = pb_api.new_push(sender_name="Test Case", type="text")
    result = list_pushes()
    data_regression.check(result.output)


def test_list_pushes_one_with_attrs(list_pushes, pb_api, data_regression):
    data = pb_api.new_push(
        sender_name="Test Case", type="text", title="my title", body="test note"
    )
    result = list_pushes()
    data_regression.check(result.output)


def test_list_pushes_all(list_pushes, pb_api, data_regression):
    # text
    pb_api.new_push(
        sender_name="Test Case",
        sender_email="test@test.com",
        type="text",
        title="test note",
        body="test case",
    )

    # file
    pb_api.new_push(
        sender_name="Test Case",
        sender_email="test@test.com",
        type="file",
        file_type="txt",
        file_name="burrito.txt",
        file_url="https://dev/burrito.txt",
    )

    # link
    pb_api.new_push(
        sender_name="Test Case",
        sender_email="test@test.com",
        type="text",
        title="test note",
        body="test case",
        url="https://google.com",
    )

    # dummy. Will be ignored
    pb_api.new_push(sender_name="Test Case", type="text", title="my title")

    result = list_pushes(["-c", "3"])
    data_regression.check(result.output)
