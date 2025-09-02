Changelog
=========

Unreleased
----------

- fix: lazy-init OpenRouter client to avoid startup failures without `OPENROUTER_API_KEY`.
- fix: knowledge integration now receives string context (from enum) and supports forced fetch when requested.

Notes
-----

- CORS and API-key enforcement are candidates for a follow-up PR.
