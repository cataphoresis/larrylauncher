# LarryLauncher Linux v0.2.0

Planned first packaged Linux release of the multiplatform LarryLauncher. The
builder exists, but this repository does not yet record a published `v0.2.0`
tag; validate the generated archive before treating these notes as released.

## Included

- Linux launcher with Install, Verify, Audit, Reports, and Exit actions
- bundled LarryBootstrap Linux runtime
- executable permissions and LF line endings
- SHA-256 checksum

## Boundaries

- LarryLauncher owns this release and its interface.
- LarryBootstrap remains authoritative for installation and audit logic.
- LarryHelperUSB may cache the archive but remains a separate portable-media project.
- The Raspberry Pi `Larry` repository is unchanged.
