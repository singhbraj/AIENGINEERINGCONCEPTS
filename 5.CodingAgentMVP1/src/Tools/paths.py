from fnmatch import fnmatch
from pathlib import Path

BLOCKED_PATHS_PATTERNS = [

".env",
".env.*",
".pem",
".key",
".secret",
".git",
".git/**",
"*.log",
"*.p12"
]


def normalize_path(path: str) -> str:
    normalized_path = Path(path).as_posix()
    if normalized_path.startswith("/"):
        normalized_path = normalized_path[2:]
    return normalized_path

def is_blocked_path(path: str) -> bool:
    normalized_path = normalize_path(path)
    return any(fnmatch(normalized_path, pattern) for pattern in BLOCKED_PATHS_PATTERNS)

def resolve_work_path(path: str) -> Path:
    work_dir = get_work_dir()
    work_dir.mkdir(parents=True, exist_ok=True)
    candidate = (work_dir / path).resolve()

    try:
        candidate.relative_to(work_dir)
    except ValueError as e:
        raise ValueError(f"Path escapes work directory: {path} - {e}")
    return candidate
