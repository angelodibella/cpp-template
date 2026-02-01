#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable


# Directories we never want to copy into a new project
DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    "build",
}

# File extensions we should not attempt to text-rewrite
BINARY_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".xz",
    ".bz2",
    ".7z",
    ".a",
    ".so",
    ".dylib",
    ".dll",
    ".exe",
    ".o",
    ".obj",
}


TEXT_EXTS = {
    # source / build scripts
    ".cpp",
    ".cc",
    ".cxx",
    ".c",
    ".hpp",
    ".hh",
    ".hxx",
    ".h",
    ".mpp",
    ".ixx",
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".txt",
    ".md",
    ".rst",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".json",
    # meson / ninja / make
    ".build",
    ".wrap",
    ".mk",
    # docs
    ".in",
}


def is_cpp_identifier(name: str) -> bool:
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) is not None


def should_copy(path: Path, ignore_dirs: set[str]) -> bool:
    parts = set(path.parts)
    if parts & ignore_dirs:
        return False
    return True


def copy_template(src_root: Path, dst_root: Path, ignore_dirs: set[str]) -> None:
    if dst_root.exists():
        raise FileExistsError(f"Destination already exists: {dst_root}")

    def ignore_func(directory: str, names: list[str]) -> set[str]:
        d = Path(directory)
        ignored: set[str] = set()
        for n in names:
            p = d / n
            if p.is_dir() and n in ignore_dirs:
                ignored.add(n)
        return ignored

    shutil.copytree(src_root, dst_root, ignore=ignore_func)


def all_paths_bottom_up(root: Path, ignore_dirs: set[str]) -> list[Path]:
    # Bottom-up: rename children before parents to avoid breaking traversal. :contentReference[oaicite:2]{index=2}
    paths: list[Path] = []
    for p in root.rglob("*"):
        if not should_copy(p, ignore_dirs):
            continue
        paths.append(p)
    paths.sort(key=lambda x: len(x.as_posix()), reverse=True)
    return paths


def rename_paths(root: Path, old: str, old_ns: str, new: str) -> None:
    # Rename files/dirs containing template/template_ in their *names*
    ignore_dirs = DEFAULT_IGNORE_DIRS
    for p in all_paths_bottom_up(root, ignore_dirs):
        new_name = p.name.replace(old_ns, new).replace(old, new)
        if new_name != p.name:
            p.rename(p.with_name(new_name))


def is_text_file(path: Path) -> bool:
    if path.suffix in BINARY_EXTS:
        return False
    if path.suffix in TEXT_EXTS:
        return True
    # Allow dotfiles like .clang-format / .clang-tidy
    if path.name.startswith(".") and path.suffix == "":
        return True
    # Heuristic: treat unknown as text only if small-ish and decodable
    return False


def rewrite_file(path: Path, replacements: list[tuple[str, str]]) -> None:
    try:
        data = path.read_bytes()
    except Exception:
        return

    # Try UTF-8 first, fall back (avoid crashing on odd files)
    try:
        text = data.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        try:
            text = data.decode("latin-1")
            encoding = "latin-1"
        except Exception:
            return

    new_text = text
    for a, b in replacements:
        new_text = new_text.replace(a, b)

    if new_text != text:
        path.write_text(new_text, encoding=encoding)


def rewrite_contents(root: Path, old: str, old_ns: str, new: str) -> None:
    ignore_dirs = DEFAULT_IGNORE_DIRS
    # Replace template_ first, then template (so template_ doesn't become <new>_).
    reps = [(old_ns, new), (old, new)]
    for p in root.rglob("*"):
        if not should_copy(p, ignore_dirs):
            continue
        if p.is_file() and is_text_file(p):
            rewrite_file(p, reps)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Install the C++ Meson template into a new project directory by renaming all 'template'/'template_' occurrences."
    )
    ap.add_argument(
        "name",
        help="New project name (also used for namespace, include dir, library name). Must be a valid C++ identifier by default.",
    )
    ap.add_argument(
        "destination",
        nargs="?",
        default=None,
        help="Destination directory (default: ./<name>)",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Allow names that are not valid C++ identifiers (may break namespace/includes).",
    )
    ap.add_argument(
        "--src", default=".", help="Template source root (default: current directory)"
    )
    args = ap.parse_args(argv)

    new_name = args.name
    if not args.force and not is_cpp_identifier(new_name):
        print(
            f"error: '{new_name}' is not a valid C++ identifier (namespace/include dir).",
            file=sys.stderr,
        )
        print(
            "Use a name like: myproject, my_project, MyProject — or pass --force.",
            file=sys.stderr,
        )
        return 2

    src_root = Path(args.src).resolve()
    dst_root = Path(args.destination or new_name).resolve()

    # sanity: src should look like template repo root
    if not (src_root / "meson.build").exists():
        print(
            f"error: {src_root} does not look like a Meson project root (meson.build not found).",
            file=sys.stderr,
        )
        return 2

    copy_template(src_root, dst_root, DEFAULT_IGNORE_DIRS)

    # Rename on disk first, then rewrite file contents
    rename_paths(dst_root, old="template", old_ns="template_", new=new_name)
    rewrite_contents(dst_root, old="template", old_ns="template_", new=new_name)

    print(f"Installed project to: {dst_root}")
    print("Next:")
    print(f"  cd {dst_root}")
    print("  make build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
