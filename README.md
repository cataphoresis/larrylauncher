# LarryLauncher

LarryLauncher is the multiplatform, user-facing entry point for the Larry ecosystem. It provides a small BBS-inspired interface and delegates workstation installation and verification to LarryBootstrap.

## Repository boundary

- **LarryLauncher** owns the user interface, platform entry points, packaging, and launcher releases.
- **LarryBootstrap** owns installation, reconciliation, audit, and verification logic.
- **LarryHelperUSB** defines portable media and may cache releases; it is not a source synchronizer.
- **Larry** remains the Raspberry Pi hardware and firmware repository.

Release archives vendor a versioned LarryBootstrap runtime so they work after extraction. The vendored runtime is a build output and is not committed here.

## Layout

```text
launchers/linux/       Linux entry point
launchers/macos/       reserved for the macOS entry point
launchers/windows/     reserved for the Windows entry point
packaging/linux/       Linux release documentation
scripts/               release builders
```

## Build the Linux release

Keep `larrylauncher` and `larrybootstrap` as sibling working copies, then run:

```bash
python3 scripts/package-linux.py --version 0.2.0
```

The builder creates a `.tar.gz` archive and SHA-256 checksum in `dist/` while preserving executable permissions and LF line endings.
