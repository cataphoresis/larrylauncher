# LarryLauncher

LarryLauncher is the multiplatform, user-facing entry point for the Larry
ecosystem. It provides a small BBS-inspired interface and delegates workstation
installation and verification to LarryBootstrap.

## Repository boundary

- **LarryLauncher** owns the user interface, platform entry points, packaging, and launcher releases.
- **LarryBootstrap** owns installation, reconciliation, audit, and verification logic.
- **LarryHelperUSB** defines portable media and may cache releases; it is not a source synchronizer.
- **Larry** remains the Raspberry Pi hardware and firmware repository.

Release archives vendor a versioned LarryBootstrap runtime so they work after
extraction. The vendored runtime is a build output and is not committed here.

Current boundary: this repository implements the Linux launcher and its `v0.2.0`
package builder. The validated Windows launcher/package remains in
`cataphoresis/larrybootstrap` through `windows-v1.0.1`; it has not migrated
here. The macOS launcher directory is still a placeholder.

## Layout

```text
launchers/linux/       Linux entry point
launchers/macos/       placeholder for a future macOS package
launchers/windows/     boundary note; Windows remains in LarryBootstrap
packaging/linux/       Linux release documentation
scripts/               release builders
```

## Build the Linux release

Keep `larrylauncher` and `larrybootstrap` as sibling working copies, then run:

```bash
python3 scripts/package-linux.py --version 0.2.0
```

The builder creates a `.tar.gz` archive and SHA-256 checksum in `dist/` while
preserving executable permissions and LF line endings. No Linux release tag is
currently recorded in this repository; package and validate the artifact before
publishing `v0.2.0`.

## Next implementation steps

1. Build and validate the Linux `v0.2.0` archive against LarryBootstrap commit
   `102f193` or a deliberately selected newer revision.
2. Publish the Linux launcher milestone if validation succeeds.
3. Implement and validate a native macOS package.
4. Decide explicitly whether Windows packaging should migrate from
   LarryBootstrap; do not duplicate two authoritative Windows packages.
