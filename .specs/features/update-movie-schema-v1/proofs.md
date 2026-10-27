# update-movie-schema-v1 proofs

**HEAD**: 62bd9a0
**Tree**: dirty - .agents/skills/definitions-manager/, resume.txt
**Result**: 5 pass, 0 fail; mutations 0 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `pytest tests/unit/test_upstream.py` | 2 | 2 | pass |
| C2 | `pytest tests/unit/test_upstream.py` | 2 | 2 | pass |
| C3 | `pytest` | 2 | 2 | pass |
| Build | `pytest` | - | - | pass |
| Build | `python3 -m ruff check it_mdb_api/ definitions/ tests/` | - | - | pass |
