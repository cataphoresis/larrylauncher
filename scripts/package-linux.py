#!/usr/bin/env python3
"""Build a Linux LarryLauncher archive with a pinned LarryBootstrap runtime."""

from __future__ import annotations

import argparse
import hashlib
import io
import re
import subprocess
import tarfile
from pathlib import Path, PurePosixPath

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[.-][0-9A-Za-z.-]+)?$")
ROOT = Path(__file__).resolve().parents[1]


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.2.0")
    parser.add_argument("--bootstrap-root", type=Path, default=ROOT.parent / "larrybootstrap")
    parser.add_argument("--output-directory", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    if not VERSION_RE.fullmatch(args.version):
        parser.error("version must be a semantic version such as 0.2.0")
    return args


def add(archive: tarfile.TarFile, source: Path, destination: PurePosixPath, executable: bool = False) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Required file is missing: {source}")
    data = source.read_bytes().replace(b"\r\n", b"\n")
    info = tarfile.TarInfo(str(destination))
    info.size, info.mode, info.mtime = len(data), (0o755 if executable else 0o644), 0
    archive.addfile(info, io.BytesIO(data))


def git_revision(repository: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", "HEAD"], text=True
    ).strip()


def build(version: str, bootstrap: Path, output: Path) -> tuple[Path, Path]:
    bootstrap = bootstrap.resolve()
    package = f"LarryLauncher-Linux-v{version}"
    output.mkdir(parents=True, exist_ok=True)
    archive_path = output.resolve() / f"{package}.tar.gz"
    checksum_path = Path(f"{archive_path}.sha256")
    prefix = PurePosixPath(package)

    with tarfile.open(archive_path, "w:gz", format=tarfile.PAX_FORMAT) as archive:
        add(archive, ROOT / "launchers/linux/launcher.sh", prefix / "larry-launcher", True)
        add(archive, ROOT / "packaging/linux/README-LINUX.md", prefix / "README.md")
        add(archive, ROOT / "packaging/linux/RELEASE_NOTES.md", prefix / "RELEASE_NOTES.md")

        runtime_files = [bootstrap / "bootstrap.sh", bootstrap / "common/profiles/standard.json"]
        runtime_files.extend(sorted((bootstrap / "platforms/linux").rglob("*")))
        for source in runtime_files:
            if not source.is_file() or source.name == ".gitkeep":
                continue
            relative = source.relative_to(bootstrap)
            if any(part in {"logs", "reports"} for part in relative.parts):
                continue
            add(
                archive,
                source,
                prefix / "runtime/larrybootstrap" / PurePosixPath(relative.as_posix()),
                source.suffix == ".sh",
            )

        manifest = (
            f"LarryLauncher-Version: {version}\n"
            f"LarryBootstrap-Commit: {git_revision(bootstrap)}\n"
        ).encode("ascii")
        info = tarfile.TarInfo(str(prefix / "BUILD-MANIFEST.txt"))
        info.size, info.mode, info.mtime = len(manifest), 0o644, 0
        archive.addfile(info, io.BytesIO(manifest))

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path.write_text(f"{digest}  {archive_path.name}\n", encoding="ascii", newline="\n")
    return archive_path, checksum_path


def main() -> None:
    args = arguments()
    archive, checksum = build(args.version, args.bootstrap_root, args.output_directory)
    print(f"Created {archive}")
    print(f"Created {checksum}")


if __name__ == "__main__":
    main()
