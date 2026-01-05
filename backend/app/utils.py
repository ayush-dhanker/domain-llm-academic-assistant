# from pathlib import Path

# PROJECT_ROOT = Path(__file__).resolve().parents[2]


# def project_path(*parts):
#     return PROJECT_ROOT.joinpath(*parts)


from pathlib import Path


def _find_project_root() -> Path:
    """
    Find repo root by walking upward until we see 'data' and 'backend' folders.
    Works both locally and inside Docker (/app).
    """
    p = Path(__file__).resolve()
    for candidate in [p] + list(p.parents):
        if (candidate / "data").exists() and (candidate / "backend").exists():
            return candidate
        # Docker case: code is copied to /app/app and data to /app/data
        if (candidate / "data").exists() and (candidate / "app").exists():
            return candidate
    # Fallback: assume /app in Docker or parent of this file
    return p.parents[1]


PROJECT_ROOT = _find_project_root()


def project_path(*parts):
    return PROJECT_ROOT.joinpath(*parts)
