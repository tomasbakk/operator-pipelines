from datetime import datetime
from typing import Any, Dict

import pytest
from operatorcert.static_tests.community.validations import (
    validate_capabilities,
    validate_categories,
    validate_icon,
    validate_links,
    validate_list_of_strings,
    validate_maintainers,
    validate_semver,
    validate_timestamp,
    validate_list_of_dicts,
)


@pytest.mark.parametrize(
    "value, expected",
    [("", False), (1, False), ("Full Lifecycle", True)],
    indirect=False,
    ids=[
        "Empty",
        "Invalid type",
        "Valid value",
    ],
)
def test_validate_capabilities(value: Any, expected: bool) -> None:
    assert validate_capabilities(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("", False),
        (1, False),
        ("Networking", True),
        ("Networking,Storage", True),
        ("Networking,foo", False),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Invalid type",
        "Valid single value",
        "Multiple valid values",
        "Mixed valid and invalid values",
    ],
)
def test_validate_categories(value: Any, expected: bool) -> None:
    assert validate_categories(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("", False),
        (1, False),
        ("2023-08-17T12:00:00Z", True),
        (datetime.now(), True),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Invalid type",
        "Valid string value",
        "Valid datetime value",
    ],
)
def test_validate_timestamp(value: Any, expected: bool) -> None:
    assert validate_timestamp(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("", False),
        (1, False),
        ("1.0.0", True),
        ("1.2.3.4", False),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Invalid type",
        "Valid semver value",
        "Invalid semver value",
    ],
)
def test_validate_semver(value: Any, expected: bool) -> None:
    assert validate_semver(value) == expected


@pytest.mark.parametrize(
    "value, schema, expected",
    [
        ("", {}, False),
        (1, {}, False),
        ([], {}, True),
        ([{"foo": "bar"}], {"foo": str}, True),
        ([{"foo": 1}], {"foo": str}, False),
        ([{"foo": "bar"}], {"foo": str, "bar": str}, False),
        ([1], {"foo": str}, False),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Invalid type",
        "Empty list",
        "Valid list",
        "Invalid field type",
        "Missing field",
        "Invalid item type",
    ],
)
def test_validate_list_of_dicts(
    value: Any, schema: Dict[str, Any], expected: bool
) -> None:
    assert validate_list_of_dicts(value, schema) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ([], False),
        ([{"base64data": "Zm9v", "mediatype": "image/png"}], True),
        ([{"base64data": "", "mediatype": "image/png"}], False),
        ([{"base64data": "foobar", "mediatype": "image/png"}], False),
        ([{"base64data": "Zm9v", "mediatype": "text/plain"}], False),
        ([{"base64data": "Zm^v", "mediatype": "image/png"}], False),
        ([{"base64data": " Zm\n9v\n", "mediatype": "image/png"}], True),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Valid icon",
        "Empty base64data",
        "Invalid base64data",
        "Invalid mediatype",
        "Invalid characters in base64data",
        "Whitespace in base64data",
    ],
)
def test_validate_icon(value: Any, expected: bool) -> None:
    assert validate_icon(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ([], False),
        ([{"name": "foo", "email": "foo@bar.com"}], True),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Valid",
    ],
)
def test_validate_maintainers(value: Any, expected: Any) -> None:
    assert validate_maintainers(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ([], False),
        ([{"name": "foo", "url": "https://foo.com/"}], True),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Valid",
    ],
)
def test_validate_links(value: Any, expected: bool) -> None:
    assert validate_links(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ([], False),
        (["foo"], True),
        ([1], False),
    ],
    indirect=False,
    ids=[
        "Empty",
        "Valid",
        "Invalid element type",
    ],
)
def test_validate_list_of_strings(value: Any, expected: bool) -> None:
    assert validate_list_of_strings(value) == expected
