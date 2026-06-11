from pathlib import Path

EXTS = {".md", ".yml", ".yaml", ".json", ".tsx", ".ts", ".html", ".css", ".toml", ".py"}
SKIP = {".git", ".venv", "node_modules", "site", "dist", "build", ".next", "__pycache__"}
REPS = [
    ("Pokala HealthOps API", "Pokala HealthOps API"),
    ("Pokala HealthOps", "Pokala HealthOps"),
    ("pokala-healthops-web", "pokala-healthops-web"),
    ("No-PHI Healthcare Interface Operations API", "No-PHI Healthcare Interface Operations API"),
    ("No-PHI Healthcare Interface Operations Platform", "No-PHI Healthcare Interface Operations Platform"),
    ("no-PHI Healthcare Interface Operations Platform", "no-PHI Healthcare Interface Operations Platform"),
    ("Healthcare Interface Operations Platform", "Healthcare Interface Operations Platform"),
    ("Healthcare Interface Operations", "Healthcare Interface Operations"),
    ("Local-first no-PHI Healthcare Interface Operations command center", "No-PHI Healthcare Interface Operations Platform"),
    ("name = \"openhip-command-center\"", "name = \"pokala-healthops\""),
    ("description = \"Local-first no-PHI Healthcare Interface Operations command center\"", "description = \"No-PHI Healthcare Interface Operations Platform\""),
]

changed = []
for path in Path(".").rglob("*"):
    if not path.is_file():
        continue
    if any(part in SKIP for part in path.parts):
        continue
    if path.suffix.lower() not in EXTS:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    new = text
    for old, fresh in REPS:
        new = new.replace(old, fresh)
    if new != text:
        path.write_text(new, encoding="utf-8")
        changed.append(str(path))
print("Updated files:")
for item in changed:
    print(" - " + item)
