# SPDX-License-Identifier: MIT
"""idutils custom scheme for AICID — persistent identifiers for AI agents.

Normative spec: https://aicid.net/docs/identifier

Canonical form: ``AICID-dddd-dddd-dddd-dddX`` — 15 digits plus an ISO 7064
MOD 11-2 check character (``X`` for 10), ORCID-shaped by design.

Registers itself in idutils via the ``idutils.custom_schemes`` entry point::

    [project.entry-points."idutils.custom_schemes"]
    aicid = "idutils_aicid:aicid_scheme"
"""
from __future__ import annotations

import re
from typing import Any

AICID_URLS = ["https://aicid.net/", "http://aicid.net/", "https://www.aicid.net/"]

_AICID_RE = re.compile(r"^AICID-(\d{4})-(\d{4})-(\d{4})-(\d{3}[0-9X])$")


def _strip_prefix(val: str) -> str:
    """Remove URL prefix (incl. ``/agents/``) and uppercase."""
    val = val.strip().upper()
    for url in AICID_URLS:
        prefix = url.upper()
        if val.startswith(prefix):
            val = val.removeprefix(prefix)
            break
    return val.removeprefix("AGENTS/")


def _check_character(digits15: str) -> str:
    """ISO 7064 MOD 11-2 check character for a 15-digit string."""
    total = 0
    for ch in digits15:
        total = (total + int(ch)) * 2
    result = (12 - total % 11) % 11
    return "X" if result == 10 else str(result)


def is_aicid(val: str) -> bool:
    """Test if argument is an AICID identifier (or aicid.net URL)."""
    if not isinstance(val, str):
        return False
    match = _AICID_RE.match(_strip_prefix(val))
    if not match:
        return False
    core = "".join(match.groups())
    return _check_character(core[:15]) == core[15]


def normalize_aicid(val: str) -> str:
    """Normalize an AICID identifier to canonical ``AICID-dddd-dddd-dddd-dddX``."""
    match = _AICID_RE.match(_strip_prefix(val))
    if not match:
        raise ValueError(f"Not a valid AICID identifier: {val!r}")
    core = "".join(match.groups())
    if _check_character(core[:15]) != core[15]:
        raise ValueError(f"Invalid AICID check character: {val!r}")
    return f"AICID-{core[0:4]}-{core[4:8]}-{core[8:12]}-{core[12:16]}"


def aicid_scheme() -> dict[str, Any]:
    """Return the idutils custom-scheme config for ``aicid``."""
    return {
        "validator": is_aicid,
        "normalizer": normalize_aicid,
        # an aicid.net URL is otherwise just a URL
        "filter": ["url"],
        "url_generator": lambda url_scheme, pid: f"https://aicid.net/agents/{pid}",
    }
