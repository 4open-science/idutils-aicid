# SPDX-License-Identifier: MIT
"""Tests for idutils-aicid."""
from __future__ import annotations

import pytest

from idutils_aicid import is_aicid, normalize_aicid

VALID = "AICID-5282-9748-4313-4513"  # example from the AICID docs


class TestValidator:
    @pytest.mark.parametrize(
        "val",
        [
            VALID,
            "aicid-5282-9748-4313-4513",  # lowercase
            f"https://aicid.net/{VALID}",
            f"https://aicid.net/agents/{VALID}",
            f"  {VALID}  ",  # whitespace
            "AICID-0000-0000-0000-0001",  # check char 1 for all-zero digits
            "AICID-0000-0000-0000-001X",  # check char X
        ],
    )
    def test_valid(self, val: str) -> None:
        assert is_aicid(val)

    @pytest.mark.parametrize(
        "val",
        [
            "AICID-5282-9748-4313-4514",  # wrong check char
            "AICID-0000-0000-0000-0000",  # wrong check char
            "5282-9748-4313-4513",  # no prefix
            "AICID-5282-9748-4313",  # too short
            "AICID-5282-9748-4313-4513-1",  # too long
            "AICID-5282-97a8-4313-4513",  # non-digit
            "AICID-5282974843134513",  # unhyphenated is not canonical grammar
            "ORCID-5282-9748-4313-4513",  # other scheme
            "",
            None,
            5282974843134513,
        ],
    )
    def test_invalid(self, val) -> None:
        assert not is_aicid(val)


class TestNormalizer:
    def test_canonical_passthrough(self) -> None:
        assert normalize_aicid(VALID) == VALID

    def test_lowercase(self) -> None:
        assert normalize_aicid(VALID.lower()) == VALID

    def test_url(self) -> None:
        assert normalize_aicid(f"https://aicid.net/agents/{VALID}") == VALID

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError):
            normalize_aicid("AICID-0000-0000-0000-0000")


class TestIdutilsIntegration:
    """The entry point makes idutils scheme-aware; requires the package installed."""

    def test_detect(self) -> None:
        import idutils

        assert "aicid" in idutils.detect_identifier_schemes(VALID)
        schemes = idutils.detect_identifier_schemes(f"https://aicid.net/agents/{VALID}")
        assert "aicid" in schemes
        assert "url" not in schemes  # filtered out

    def test_normalize_pid(self) -> None:
        import idutils

        assert idutils.normalize_pid(VALID, "aicid") == VALID
        assert idutils.normalize_pid(VALID.lower(), "aicid") == VALID

    def test_to_url(self) -> None:
        import idutils

        assert idutils.to_url(VALID, "aicid") == f"https://aicid.net/agents/{VALID}"
