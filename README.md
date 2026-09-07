# Kiro IDE Hands-on — Training Week

Participant-facing GitHub Pages site for the Kiro IDE intermediate hands-on.

## Local build

```bash
python tools/build_starter_zip.py
python -m pip install --requirement requirements.txt
mkdocs build --strict
mkdocs serve
```

The public site contains only participant-safe material. Facilitator notes and solution files remain in the internal source repository.
