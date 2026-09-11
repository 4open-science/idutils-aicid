# idutils-aicid

[idutils](https://github.com/inveniosoftware/idutils) custom scheme for
**AICID** — persistent identifiers for AI agents that contribute to research
(<https://aicid.net>).

Once installed, `idutils` understands the `aicid` scheme everywhere:
detection, validation, normalization, and URL generation, with zero upstream
changes.

## Usage

```python
import idutils
import idutils_aicid  # registering the entry point is enough; importing is optional

idutils.is_aicid("AICID-5282-9748-4313-4513")              # via entry point...
idutils_aicid.is_aicid("AICID-5282-9748-4313-4513")        # ...or directly
idutils.detect_identifier_schemes("https://aicid.net/agents/AICID-5282-9748-4313-4513")
# ['aicid']
idutils.normalize_pid("AICID-5282-9748-4313-4513", "aicid")
# 'AICID-5282-9748-4313-4513'
idutils.to_url("AICID-5282-9748-4313-4513", "aicid")
# 'https://aicid.net/agents/AICID-5282-9748-4313-4513'
```

## InvenioRDM

In your instance's `invenio.cfg`:

```python
from idutils_aicid import is_aicid
from invenio_rdm_records.config import RDM_RECORDS_PERSONORG_SCHEMES

RDM_RECORDS_PERSONORG_SCHEMES = {
    **RDM_RECORDS_PERSONORG_SCHEMES,
    "aicid": {"label": _("AICID"), "validator": is_aicid, "datacite": "AICID"},
}
```

Creators then accept `{"scheme": "aicid", "identifier": "AICID-…"}`, and the
DataCite serializer emits `nameIdentifierScheme="AICID"`.

## Identifier format

Normative spec: <https://aicid.net/docs/identifier>.
`AICID-dddd-dddd-dddd-dddX` — 15 digits plus an ISO 7064 MOD 11-2 check
character, ORCID-shaped by design.

## License

MIT
